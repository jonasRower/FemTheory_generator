# tento modul posouvá text nahoru, tim ze pridava style="top:-30px", style="top:-45px" apod...

import zamenZnaky
import re
import copy

class posunText:

    def __init__(self, obsahHtml, prvniAPosledniIndexPole, pounOdecti, posunVychozi):

        self.pounOdecti = pounOdecti
        self.posunVychozi = posunVychozi

        seznamRadkuPTd = self.vratSeznamIndexuRadkuPTd(obsahHtml)
        seznamRadku = self.vratSloupecZPole2D(seznamRadkuPTd, 0)
        obsahHtmlBezTop = self.odeberStyleZeVsechRadku(obsahHtml, seznamRadku)




        #else:

        if(prvniAPosledniIndexPole != None):

            seznamRadku2D = self.vratSeznamIdClass(obsahHtml, seznamRadku)
            seznamRadku2D = self.nahradClassSZaIdExp(seznamRadkuPTd, seznamRadku2D)

            # zjisti ktere indexy radku patri ke kterym paragrafum
            # podle toho take zjistuje o kolik ma posunout

            # pouzije jiz naprogramovanou tridu
            ziskejIndexyRadku = zamenZnaky.precislovani(None, None, False)
            indexyRadku2 = ziskejIndexyRadku.priradKIndexumRadkuJejichCislaParag(seznamRadku, prvniAPosledniIndexPole)

            radkyPodleParagRozdel = self.rozdelRadkyPodleParagrafu(seznamRadkuPTd, indexyRadku2)

            if(pounOdecti != None):

                posunPoleTot2D = self.dopocitejPosunProVsechnyRadky(radkyPodleParagRozdel)
                posunPoleTot = self.vratPouzePlatneRadkyPoleTot(seznamRadku2D, posunPoleTot2D)
                seznamRadku = self.vylucNeplatnePolozkySeznamRadku(seznamRadku, seznamRadku2D)
                obsahHtmlTop = self.vlozPosunDoVsechRadku(obsahHtmlBezTop, seznamRadku, posunPoleTot)

                # pokud je nastavena 0, pak odstrani "top" ve style
                if (pounOdecti == 0):
                    obsahHtmlTop = self.odeberTop0Px(obsahHtmlTop, seznamRadku, ' style="top:0px;"')
                    obsahHtmlTop = self.odeberTop0Px(obsahHtmlTop, seznamRadku, 'top:0px; ')

                self.obsahHtmlTop = obsahHtmlTop

            else:
                # vraci, pokud se vola pridejReference
                self.radkyPodleParagRozdel = radkyPodleParagRozdel

        else:
            # pokud je None, pak se nevola pro posun textu, ale pro odstraneni style (pouzije se "def getObsahHtmlBezTop(self):")
            self.obsahHtmlBezTop = obsahHtmlBezTop
            self.seznamRadkuPTd = seznamRadkuPTd


    def getObsahHtmlTop(self):
        return(self.obsahHtmlTop)

    def getObsahHtmlBezTop(self):
        return(self.obsahHtmlBezTop)

    def getRadkyPodleParagRozdel(self):
        return(self.radkyPodleParagRozdel)

    def getSeznamRadkuPTd(self):
        return(self.seznamRadkuPTd)


    # indexy radku s class='"znaky"' se neuvazuji pro tento script
    # proto se vyluuji s prepsanim na -1
    def vylucNeplatnePolozkySeznamRadku(self, seznamRadku, seznamRadku2D):

        for i in range(len(seznamRadku2D)):
            classS = seznamRadku2D[i][1]

            if(classS == 'class="znaky"'):
                seznamRadku[i] = -1

        return(seznamRadku)


    # na radku <p> je class="s2_4" a id="exp-1" soucasne
    # pokud se tedy jedna o radek <p>, pak ponechavam pouze id="exp-1"
    def nahradClassSZaIdExp(self, seznamRadkuPTd, seznamRadku2D):

        for i in range(len(seznamRadku2D)):
            classS = seznamRadku2D[i][1]

            if(classS == 'class="s?_?"'):
                classS1 = seznamRadku2D[i-1][1]
                radekPTd = seznamRadkuPTd[i]
                pTd = radekPTd[1]
                if(pTd == 'p'):
                    if(classS1 == 'class="sloupce?'):
                        seznamRadku2D[i][1] = 'id="exp-?'
                    if (classS1 == '<button'):
                        seznamRadku2D[i][1] = 'id="exp-?'

        return(seznamRadku2D)



    def vratPouzePlatneRadkyPoleTot(self, seznamRadku2D, posunPoleTot2D):

        posunPoleTot = []
        hledejOdIndexu = 0

        for i in range(len(seznamRadku2D)):
            radekPole = seznamRadku2D[i]
            idClassStr = radekPole[1]

            if(idClassStr != 'class="znaky"'):
                indexRadku = self.vyhledjRadekClassId(posunPoleTot2D, idClassStr, hledejOdIndexu)

                if (hledejOdIndexu == 62):
                    print("")

                # pokud nenajde nic, pak se pravdepodobne jedna o pripad prohozenych buttonu
                # v tom pripade se data opravuji zde:
                if(indexRadku == ''):
                    hledejOdIndexu = self.vratHledejOdIndexu(posunPoleTot2D, hledejOdIndexu)
                    indexRadku = self.vyhledjRadekClassId(posunPoleTot2D, idClassStr, hledejOdIndexu)
                    print("")


                radekPosun = posunPoleTot2D[indexRadku]
                posun = radekPosun[0]
                posunPoleTot.append(posun)

                # ulozi do dalsiho cyklu
                hledejOdIndexu = indexRadku + 1

        return(posunPoleTot)


    # obcas muze mit problem vyhledat spravna data
    # neni dulezite se tim zabyvat, jelikoz button a sloupce? maji stejny top, takze je jedno co se najde
    # i proto oprava chyby se resi zjednodusene zde
    def vratHledejOdIndexu(self, posunPoleTot2D, hledejOdIndexu):

        for i in range(len(posunPoleTot2D)):
            i1 = hledejOdIndexu - i - 1
            radekPole = posunPoleTot2D[i1]
            polPole = radekPole[1]
            if(polPole != '<button'):
                hledejOdIndexu = i1
                break

        return(hledejOdIndexu)



    def vyhledjRadekClassId(self, seznamRadku2D, idClassStrExp, hledejOdIndexu):

        indexRadku = ''

        for i in range(len(seznamRadku2D)):
            i1 = i + hledejOdIndexu

            # aby nedosel mimo rozsah pole
            if (i1 + 1 > len(seznamRadku2D)):
                break

            radekPole = seznamRadku2D[i1]
            idClassStr = radekPole[1]
            if(idClassStr == idClassStrExp):
                indexRadku = i1
                break

        return(indexRadku)


    # vrati pole vsech id nebo class podle kterych pozna, na ktere radky ma zapisovat
    def vratSeznamIdClass(self, obsahHtml, seznamRadku):

        poleIDExp = self.vratSeznamIndexuRadkuSeSubstringem(obsahHtml, 'id="exp-?')
        poleSloupce = self.vratSeznamIndexuRadkuSeSubstringem(obsahHtml, 'class="sloupce?')
        poleS = self.vratSeznamIndexuRadkuSeSubstringem(obsahHtml, 'class="s?_?"')
        button = self.vratSeznamIndexuRadkuSeSubstringem(obsahHtml, '<button')
        znaky = self.vratSeznamIndexuRadkuSeSubstringem(obsahHtml, 'class="znaky"')

        seznamRadku2D = self.vytvorPole2D(seznamRadku)
        seznamRadku2D = self.doplnDoSeznamuRadkuIdClass(seznamRadku2D, poleIDExp, 'id="exp-?',0)
        seznamRadku2D = self.doplnDoSeznamuRadkuIdClass(seznamRadku2D, button, '<button', 0)
        seznamRadku2D = self.doplnDoSeznamuRadkuIdClass(seznamRadku2D, znaky, 'class="znaky"', 0)
        seznamRadku2D = self.doplnDoSeznamuRadkuIdClass(seznamRadku2D, poleSloupce, 'class="sloupce?', 1)
        seznamRadku2D = self.doplnDoSeznamuRadkuIdClass(seznamRadku2D, poleS, 'class="s?_?"',-1)
        seznamRadku2D = self.doplnDoSeznamuRadkuIdClass(seznamRadku2D, poleSloupce, 'class="sloupce?', 2)


        # prohodi radky button
        seznamRadku2D = self.prohodPoradiSPolozkouButtonAll(seznamRadku2D)

        return(seznamRadku2D)


    def prohodPoradiSPolozkouButtonAll(self, seznamRadku2D):

        prvniAPosledniIndexyButtPole = self.vratPoleSPrvnimiAPoslednimiIndexyRadku(seznamRadku2D)
        for i in range(len(prvniAPosledniIndexyButtPole)):
            prvniAPosledniIndexyButt = prvniAPosledniIndexyButtPole[i]
            seznamRadku2D = self.prohodPoradiSPolozkouButton(seznamRadku2D, prvniAPosledniIndexyButt)

        return(seznamRadku2D)


    def vratPoleSPrvnimiAPoslednimiIndexyRadku(self, seznamRadku2D):

        hledejOdIndexu = 0
        prvniAPosledniIndexyButtPole = []

        for i in range(len(seznamRadku2D)):
            prvniAPosledniIndexyButt = self.zjistiPrvniAPosledniIndexyButton(seznamRadku2D, hledejOdIndexu)

            if(prvniAPosledniIndexyButt != [None]):
                prvniAPosledniIndexyButtPole.append(prvniAPosledniIndexyButt)
                hledejOdIndexu = prvniAPosledniIndexyButt[1]
            else:
                break

        return(prvniAPosledniIndexyButtPole)


    # pokud je tam button je potreaba prohodit polozky
    def prohodPoradiSPolozkouButton(self, seznamRadku2D, prvniAPosledniIndexyButt):

        prvniIndexButt = prvniAPosledniIndexyButt[0]
        posledniIndexButt = prvniAPosledniIndexyButt[1]

        seznamRadkuPredPrvnimIndexem = seznamRadku2D[0:prvniIndexButt:1]
        seznamRadkuKProhozeni = seznamRadku2D[prvniIndexButt:posledniIndexButt+1:1]
        seznamRadkuZaPoslednimIndexem = seznamRadku2D[posledniIndexButt+1:len(seznamRadku2D):1]

        seznamRadkuKProhozeniNew = self.vratProhozeneRadky(seznamRadkuKProhozeni)

        seznamRadku2DNew = seznamRadkuPredPrvnimIndexem.copy()
        seznamRadku2DNew = seznamRadku2DNew + seznamRadkuKProhozeniNew
        seznamRadku2DNew = seznamRadku2DNew + seznamRadkuZaPoslednimIndexem

        return(seznamRadku2DNew)


    def vratProhozeneRadky(self, seznamRadkuKProhozeni):

        #seznamRadkuKProhozeniNew = seznamRadkuKProhozeni
        seznamRadkuKProhozeniNew = copy.deepcopy(seznamRadkuKProhozeni)
        idClassPrv = seznamRadkuKProhozeni[0][1]
        idClassPosl = seznamRadkuKProhozeni[len(seznamRadkuKProhozeni)-1][1]

        if(idClassPosl == 'class="sloupce?'):
            seznamRadkuKProhozeniNew[0][1] = idClassPosl
            seznamRadkuKProhozeniNew[len(seznamRadkuKProhozeni)-1][1] = idClassPrv

        return(seznamRadkuKProhozeniNew)


    def zjistiPrvniAPosledniIndexyButton(self, seznamRadku2D, hledejOdIndexu):

        jeToStaleButt = False
        posledniIndex = None
        radekObsahujeClass = False

        prvniAPosledniIndexyButt = []

        for i in range(len(seznamRadku2D)):
            i1 = hledejOdIndexu + i
            if(i1+1 > len(seznamRadku2D)):
                break

            radek = seznamRadku2D[i1]
            polozka = radek[1]

            if (polozka == '<button'):
                if (jeToStaleButt == False):
                    jeToStaleButt = True
                    prvniIndex = i

            else:
                if (jeToStaleButt == True):
                    jeToStaleButt = False
                    posledniIndex = i - 1


        # proveri, zda skutecne je za poslednim radkem 'class="sloupce?'
        if(posledniIndex != None):
            radekZaPoslednimRadkem = seznamRadku2D[posledniIndex + 1]
            radekObsahujeClass = self.detekujPritomnostSlova(radekZaPoslednimRadkem, 'class="sloupce?')

        if(radekObsahujeClass == True):
            posledniIndex = posledniIndex + 1

            prvniAPosledniIndexyButt.append(prvniIndex)
            prvniAPosledniIndexyButt.append(posledniIndex)
        else:
            prvniAPosledniIndexyButt.append(None)

        return (prvniAPosledniIndexyButt)


    def doplnDoSeznamuRadkuIdClass(self, seznamRadku2D, poleIdClass, idClassStr, sousedniRadek):


        for i in range(len(seznamRadku2D)):
            radekAPrazdny = seznamRadku2D[i]
            indexRadku = radekAPrazdny[0]
            indexRadku = indexRadku + sousedniRadek

            indexRadkuJeVPoli = self.detekujPritomnostSlova(poleIdClass, indexRadku)
            if(indexRadkuJeVPoli == True):
                seznamRadku2DObsah = seznamRadku2D[i][1]
                if(seznamRadku2DObsah == ''):
                    seznamRadku2D[i][1] = idClassStr

        return(seznamRadku2D)


    def vratSeznamIndexuRadkuSeSubstringem(self, obsahHtml, substrExp):

        seznamIndexuRadku = []

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]
            radekObsahujeSubString = self.detekujSubStrBezCisla(radek, substrExp)

            if(radekObsahujeSubString == True):
                seznamIndexuRadku.append(i)

        return(seznamIndexuRadku)



    # jelikoz mohou byt nejake radky vynechane, detekuje prislusne class, aby zjistil, zda "top" prirazuje k spravnemu radku
    def detekujSubStrBezCisla(self, radekOrig, subStringBezCislaExp):

        radekSplit = radekOrig.split(' ')

        for i in range(len(radekSplit)):
            radekSpl = radekSplit[i]
            subStringBezCisla = self.odeberCisloZeSrtringu(radekSpl)

            radekObsahujeSubString = self.detekujPritomnostSlova(subStringBezCisla, subStringBezCislaExp)
            if(radekObsahujeSubString == True):
                break

        return(radekObsahujeSubString)


    #odebere cislo, tj. proto aby dokazal detekovat id nebo class bez cisla
    #napr.: class="s43_4" vrati class="s?_?
    def odeberCisloZeSrtringu(self, radekOrig):

        radekNew = ''
        znakPredchozi = ''

        for i in range(len(radekOrig)):
            znak = radekOrig[i]

            if(znak.isnumeric() == True):
                znak = '?'

                if(znak != znakPredchozi):
                    radekNew = radekNew + znak

            else:
                radekNew = radekNew + znak

            znakPredchozi = znak

        return(radekNew)


    # aby se lepe testovalo a omezili se chyby, sjednocuji pole dohromady
    # taky z duvodu, ze kdyz jsou nejake radky vynechane, aby se nezapisovaly jinam1
    def spojSeznamRadkuAPosunPoleTot(self, seznamRadku, obsahHtmlTop, radkyPodleParagRozdel):

        for r in range(len(radkyPodleParagRozdel)):
            radkeParag = radkyPodleParagRozdel[r]
            indexRadku = radkeParag[0]

            #indexVSeznamuRadku


    # odebere style="top:0px tak aby dostal html do puvodniho stavu
    def odeberTop0Px(self, obsahHtml, seznamRadku, coOdeber):

        obsahHtmlBezNul = []

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]

            # zkontroluje, zda se jedna o dany radek v seznamu a opravi
            for i1 in seznamRadku:
                if (i1 == i):
                    radek = radek.replace(coOdeber, '')

            obsahHtmlBezNul.append(radek)

        return(obsahHtmlBezNul)


    def vlozPosunDoVsechRadku(self, obsahHtmlBezTop, seznamRadku, posunPoleTot):

        obsahHtmlTop = []
        iPos = -1

        for i in range(len(obsahHtmlBezTop)):
            radek = obsahHtmlBezTop[i]

            # zkontroluje, zda se jedna o dany radek v seznamu a opravi
            for i1 in seznamRadku:
                if i1 == i:
                    iPos = iPos + 1
                    posun = posunPoleTot[iPos]
                    radekTop = 'style="top:' + str(posun) + 'px;"'

                    radek = self.vlozTopDoRadku(radek, radekTop)

            obsahHtmlTop.append(radek)

        return(obsahHtmlTop)


    def vlozTopDoRadku(self, radekOrig, radekTop):

        # nastavi jako vychozi, bud necha, nebo prepise
        radekNew = radekOrig

        radekObsahujeStyle = self.detekujPritomnostSlova(radekOrig, 'style')
        if(radekObsahujeStyle == True):
            radekNew = radekOrig.replace('style=', radekTop)
        else:
            if(self.detekujPritomnostSlova(radekOrig, '<p') == True):
                radekNew = radekOrig.replace('<p', '<p ' + radekTop)
            if (self.detekujPritomnostSlova(radekOrig, '<td') == True):
                radekNew = radekOrig.replace('<td', '<td ' + radekTop)
            if (self.detekujPritomnostSlova(radekOrig, '<button') == True):
                radekNew = radekOrig.replace('<button', '<button ' + radekTop)

        radekNew = radekNew.replace('""', ' ')
        radekNew = self.zkontrolujRadekNew(radekNew)

        return(radekNew)


    def zkontrolujRadekNew(self, radekNewOrig):

        radekNew = radekNewOrig
        radekNewSplit = radekNewOrig.split('=')

        for i in range(len(radekNewSplit)):
            subRadek = radekNewSplit[i]
            pocetUvozovek = len(re.findall('"', subRadek))
            if(pocetUvozovek == 3):
                radekNew = radekNewOrig.replace('px;" ', 'px;')

        return(radekNew)



    def odeberStyleZeVsechRadku(self, obsahHtml, seznamRadku):

        obsahHtmlBezTop = []

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]

            #zkontroluje, zda se jedna o dany radek v seznamu
            for i1 in seznamRadku:
                if i1 == i:
                    #opravi radek - odebere style
                    radek = self.odeberStyleZRadku(radek)
                    radek = radek.replace('; ', ';"')

            obsahHtmlBezTop.append(radek)

        return(obsahHtmlBezTop)


    # odebere style z radku
    def odeberStyleZRadku(self, radekOrig):

        radekOrigSplit = radekOrig.split('>')
        radek1 = radekOrigSplit[0]
        radekSpaceSplit = radek1.split(' ')
        radekStyle = self.vratSubradekStyle(radekSpaceSplit)
        radekNew = radekOrig.replace(radekStyle, '')
        radekNew = radekNew.replace(' >', '>')

        return(radekNew)


    def vratSubradekStyle(self, splitRadek):

        vratRadek = ''

        for i in range(len(splitRadek)):
            radek = splitRadek[i]
            radekObsahujeTop = self.detekujPritomnostSlova(radek, 'top')

            if(radekObsahujeTop == True):
                vratRadek = radek

        return(vratRadek)



    def dopocitejPosunProVsechnyRadky(self, radkyPodleParagRozdel):

        posunVychozi = self.posunVychozi + self.pounOdecti
        posunPoleTot = []
        idClassPoleTot = []


        for i in range(len(radkyPodleParagRozdel)):
            radkyPodleParag = radkyPodleParagRozdel[i]
            jednaSeOTd = self.detekujZdaSeJednaOTd(radkyPodleParag, 'td')
            jednaSeOButton = self.detekujZdaSeJednaOTd(radkyPodleParag, 'button')

            if(jednaSeOTd == False):
                posunPole = self.dopocitejPosunProP(posunVychozi)
                idClassPole = self.vratSledIdClass(False, radkyPodleParag)
                if (jednaSeOButton == True):
                    posunPole = self.dopocitejPosunProButton(radkyPodleParag, posunVychozi)

                    # rozsiri pole o buttony
                    idClassPole = self.rozsirSledClassOButtony(idClassPole, radkyPodleParag)

            else:
                if (jednaSeOButton == True):
                    posunPole = self.dopocitejPosunProButton(radkyPodleParag, posunVychozi)

                    # rozsiri pole o buttony
                    idClassPole = self.vratSledIdClass(True, radkyPodleParag)
                    print()

                else:
                    posunPole = self.dopocitejPosunProTd(radkyPodleParag, posunVychozi)
                    idClassPole = self.vratSledIdClass(True, radkyPodleParag)
                    print()

            if(i == 0):
                posunPoleTot = posunPole
                idClassPoleTot = idClassPole
            else:
                posunPoleTot = posunPoleTot + posunPole
                idClassPoleTot = idClassPoleTot + idClassPole

            posunVychozi = posunPole[len(posunPole) - 1]


        posunPoleTot2D = self.sluc2Pole(posunPoleTot, idClassPoleTot)

        return(posunPoleTot2D)


    # vrati pole IDClass podle toho, zda se jedna o <p> nebo <td>
    def vratSledIdClass(self, tdNeboP, radkyPodleParag):

        idClassPoleP = []

        if(len(radkyPodleParag) == 12):
            print()

        if(tdNeboP == False):
            idClassPoleP.append('class="sloupce?')
            idClassPoleP.append('id="exp-?')
            idClassPoleP.append('class="s?_?"')

        else:
            for i in range(len(radkyPodleParag)):
                if(i == 0):
                    idClassPoleP.append('class="sloupce?')
                else:
                    if(i == len(radkyPodleParag)-1):
                        idClassPoleP.append('class="s?_?"')
                    else:
                        if (i == 10):
                            print()
                        vratButtIdExp = self.vratButtonIdExp(radkyPodleParag, i, idClassPoleP)
                        idClassPoleP.append(vratButtIdExp)
                        print("")

        return(idClassPoleP)


    def vratButtonIdExp(self, radkyPodleParag, index, idClassPoleP):

        if(index == 10):
            print()


        vratButtIdExp = ''
        radekParag = radkyPodleParag[index]
        buttIdExp = radekParag[1]
        if(buttIdExp == 'button'):
            vratButtIdExp = '<button'

        if (buttIdExp == 'td'):
            vratButtIdExp = 'id="exp-?'

        return(vratButtIdExp)


    def rozsirSledClassOButtony(self, idClassPoleP, radkyPodleParag):

        pocetButt = 0
        idClassPolePNew = []
        poleButt = []

        # spocita pocet polozek 'button'
        for i in range(len(radkyPodleParag)):
            radekParag = radkyPodleParag[i]
            polButt = radekParag[1]

            if(polButt == 'button'):
                poleButt.append('<button')


        # rozsiri pole o spocteny pocet buttonu
        for i in range(len(idClassPoleP)):
            idClassPolePNew.append(idClassPoleP[i])

            if (i == 0):
                idClassPolePNew = idClassPolePNew + poleButt

        return(idClassPolePNew)





    # pokud tam je button, pak jeste dodatecne opravuje data
    def dopocitejPosunProButton(self, radkyPodleParag, posunVychozi):

        posunPole = []
        posun = posunVychozi - self.pounOdecti

        # pokud tam je button, pak vsechny radky jsou radky vychozi
        for i in range(len(radkyPodleParag)):
            posunPole.append(posun)

        return(posunPole)


    # je-li v poli td, pak se jedna o td, jinak p
    def detekujZdaSeJednaOTd(self, radkyPodleParag, tdButt):

        jednaSeOTd = False

        for i in range(len(radkyPodleParag)):
            radekPole = radkyPodleParag[i]
            pNeboTd = radekPole[1]

            if(pNeboTd == tdButt):
                jednaSeOTd = True
                break

        return(jednaSeOTd)


    def dopocitejPosunProP(self, posunVychozi):

        p1 = posunVychozi - self.pounOdecti
        p2 = p1 - self.pounOdecti
        p3 = p2

        posunPole = []
        posunPole.append(p1)
        posunPole.append(p2)
        posunPole.append(p3)

        return(posunPole)


    def dopocitejPosunProTd(self, radkyPodleParag, posunVychozi):

        p1 = posunVychozi - self.pounOdecti
        p2 = p1 - self.pounOdecti

        posunPole = []
        posunPole.append(p1)

        for i in range(len(radkyPodleParag)):
            radek = radkyPodleParag[i]
            pNeboTd = radek[1]
            if(pNeboTd == 'td'):
                posunPole.append(p2)

        p3 = p2
        posunPole.append(p3)

        return(posunPole)



    def rozdelRadkyPodleParagrafu(self, seznamRadkuPTd, indexyRadku2):

        indexyRadku1 = self.vratSloupecZPole2D(indexyRadku2, 1)
        seznamOdstavcu = self.unique(indexyRadku1)
        seznamRadkuPTdParag = self.slucSloupcePoli(seznamRadkuPTd, indexyRadku2)

        radkyPodleParagrafuRozdel = []

        for i in range(len(seznamOdstavcu)):
            cisloOdst = seznamOdstavcu[i]
            radkyJedenParag = self.vratRadkyProJedenParagraf(seznamRadkuPTdParag, cisloOdst)

            radkyPodleParagrafuRozdel.append(radkyJedenParag)

        self.seznamRadkuPTdParag = seznamRadkuPTdParag

        return(radkyPodleParagrafuRozdel)


    def vratRadkyProJedenParagraf(self, seznamRadkuPTdParag, cisloParagExp):

        radkyJedenParag = []

        for i in range(len(seznamRadkuPTdParag)):
            radekParag = seznamRadkuPTdParag[i]
            cisloParag = radekParag[3]
            if(cisloParag == cisloParagExp):
                radekParagNew = []
                radekParagNew.append(radekParag[0])
                radekParagNew.append(radekParag[1])
                radekParagNew.append(radekParag[3])

                radkyJedenParag.append(radekParagNew)

        return(radkyJedenParag)


    def vratSloupecZPole2D(self, pole2D, cisloSloupce):

        pole1D = []

        for i in range(len(pole2D)):
            polozka = pole2D[i][cisloSloupce]
            pole1D.append(polozka)

        return(pole1D)


    def slucSloupcePoli(self, poleA, poleB):

        poleNew = []

        for i in range(len(poleA)):
            radekA = poleA[i]
            radekB = poleB[i]
            radekNew = radekA + radekB
            poleNew.append(radekNew)

        return (poleNew)


    # vrati seznam vsech indexu radku, ktere se budou posouvat
    # jedna se o vsechny <p> a <td>
    def vratSeznamIndexuRadkuPTd(self, obsahHtml):

        seznamRadkuPTd = []

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]
            radekObsahujeP = self.detekujPritomnostSlova(radek, '<p')
            radekObsahujeTd = self.detekujPritomnostSlova(radek, '<td')
            radekObsahujeButton = self.detekujPritomnostSlova(radek, '<button')

            indexPTd = []
            if(radekObsahujeP == True):
                indexPTd.append(i)
                indexPTd.append('p')
                seznamRadkuPTd.append(indexPTd)

            if (radekObsahujeButton == True):
                indexPTd.append(i)
                indexPTd.append('button')
                seznamRadkuPTd.append(indexPTd)

            if (radekObsahujeTd == True):
                indexPTd.append(i)
                indexPTd.append('td')
                seznamRadkuPTd.append(indexPTd)

        return(seznamRadkuPTd)


    # detekuje pritomnost substringu
    def detekujPritomnostSlova(self, radek, slovo):

        try:
            index = radek.index(slovo)
        except:
            index = -1

        if (index > -1):
            radekObsahujeSlovo = True
        else:
            radekObsahujeSlovo = False

        return (radekObsahujeSlovo)


    def unique(self, list1):

        # initialize a null list
        unique_list = []

        # traverse for all elements
        for x in list1:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)

        return(unique_list)


    #prida jeste jednu dimenzi k poli 1D
    def vytvorPole2D(self, pole1D):

        pole2D = []

        for i in range(len(pole1D)):
            polozka = pole1D[i]
            radek = []
            radek.append(polozka)
            radek.append('')

            pole2D.append(radek)

        return(pole2D)


    def sluc2Pole(self, poleA, poleB):

        poleNew = []

        for i in range(len(poleA)):
            polozkaA = poleA[i]
            polozkaB = poleB[i]

            radek = []
            radek.append(polozkaA)
            radek.append(polozkaB)

            poleNew.append(radek)

        return(poleNew)