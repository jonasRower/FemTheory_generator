# tento modul precislovava vsechna id dle cisla paragrafu
# aby bylo mozne precislovat paragrafy zpetne

import posunTextu
import reference
import specialniZnak
import porovnejObsahHtml

# meni jak cisla paragrafu, tak i cisla v "id-ckach"
class precislovani:

    def __init__(self, obsahHtml, prvniAPosledniIndexPole, vratPouzeSkutecneCislovani):

        self.vratPouzeSkutecneCislovani = vratPouzeSkutecneCislovani
        if(obsahHtml != None):

            # nez zacne precislovavat nacte si puvodni reference
            #puvodniRef = reference.doplnReference(obsahHtml, prvniAPosledniIndexPole, None, None)
            #puvodniReference = puvodniRef.getRefCisloPodleParagRozdel()

            obsahHtmlNew = self.precislujPodleStrExp(obsahHtml, prvniAPosledniIndexPole, '<p>(')

            # aby se to rekurentne nezacyklilo - jelikoz tridu volam opakovane
            if(vratPouzeSkutecneCislovani == False):
                obsahHtmlNew = self.precislujPodleStrExp(obsahHtmlNew, prvniAPosledniIndexPole, 'id="exp-')
                obsahHtmlNew = self.precislujPodleStrExp(obsahHtmlNew, prvniAPosledniIndexPole, '<div id="p1-')

                #referenceRadkyNove = self.precislujReference(puvodniReference, self.skutecnaCislaParag, self.skutecnaCislaParagNew)
                #obsahHtmlNew = self.zapisZmeneneReference(referenceRadkyNove, obsahHtmlNew, prvniAPosledniIndexPole, self.skutecnaCislaParagNew)

                # porovna puvodni a novy obsahHtml, aby dokazal zmenit reference
                upravReference = porovnejObsahHtml.porovnejObsahHtmlPredAPo(obsahHtml, obsahHtmlNew)
                obsahHtmlNew = upravReference.getHtmlNew()

                self.obsahHtmlPrecislovane = obsahHtmlNew


    def getObsahHtmlPrecislovane(self):
        return(self.obsahHtmlPrecislovane)

    def getSeznamRadkuPoradi(self):
        return(self.seznamRadkuPoradi)

    def getSkutecnaCislaParag(self):
        return(self.skutecnaCislaParag)



    def zapisZmeneneReference(self, referenceRadkyNove, obsahHtmlNew, prvniAPosledniIndexPole, novaCislaParag):

        for i in range(len(referenceRadkyNove)):
            referenceRadky = referenceRadkyNove[i]
            try:
                paragVychoziCislo = int(novaCislaParag[i])

                for iR in range(len(referenceRadky)):
                    radekAref = referenceRadky[iR]
                    ref = radekAref[1]
                    if (ref != ''):
                        intRef = int(ref)
                        zmeneneRefarence = reference.doplnReference(obsahHtmlNew, prvniAPosledniIndexPole, paragVychoziCislo, intRef)
                        obsahHtmlNew= zmeneneRefarence.getObsahHtmlRef()
                        print("")

            except:
                err = 'nic'

        return(obsahHtmlNew)


    def precislujReference(self, puvodniReference, puvodniCislaParag, novaCislaParag):

        referenceRadkyNove = puvodniReference.copy()

        for i in range(len(puvodniReference)):
            referenceRadkyPuvodni = puvodniReference[i]

            for iR in range(len(referenceRadkyPuvodni)):
                radekAref = referenceRadkyPuvodni[iR]
                ref = radekAref[1]
                if(ref != ''):
                    novaRef = self.vyhledejOpraveneCisloParag(puvodniCislaParag, novaCislaParag, ref)
                    radekRefNew = radekAref.copy()
                    radekRefNew[1] = novaRef
                    referenceRadkyNove[i][iR] = radekRefNew

        return(referenceRadkyNove)


    def vyhledejOpraveneCisloParag(self, puvodniCislaParag, novaCislaParag, ref):

        indRefPuv = self.vratIndexSlova(puvodniCislaParag, ref)
        novaRef = novaCislaParag[indRefPuv]

        return(novaRef)


    def precislujPodleStrExp(self, obsahHtml, prvniAPosledniIndexPole, strExpPred):

        seznamRadkuProZmenu = self.vratSeznamVsechIndexuRadku(obsahHtml, strExpPred)
        seznamRadkuPoradi = self.priradKIndexumRadkuJejichCislaParag(seznamRadkuProZmenu, prvniAPosledniIndexPole)
        obsahHtmlNew = self.zamenSeznamRadku(obsahHtml, seznamRadkuPoradi, strExpPred)

        # aby mohl ziskat data z jine tridy
        self.seznamRadkuPoradi = seznamRadkuPoradi

        if(strExpPred == '<p>('):
            self.skutecnaCislaParag = self.nactiSkutecnaCislaParag(seznamRadkuPoradi, obsahHtml)
            self.skutecnaCislaParagNew = self.nactiSkutecnaCislaParag(seznamRadkuPoradi, obsahHtmlNew)

        return(obsahHtmlNew)


    def nactiSkutecnaCislaParag(self, seznamRadkuPoradi, obsahHtml):

        skutecnaCislaParag = []

        for i in range(len(seznamRadkuPoradi)):
            radekPoradi = seznamRadkuPoradi[i]
            indexRadku = radekPoradi[0]
            radekHtml = obsahHtml[indexRadku]

            paragSkutCislo = self.vratSkutecneCisloParag(radekHtml)
            skutecnaCislaParag.append(paragSkutCislo)

        return(skutecnaCislaParag)


    def vratSkutecneCisloParag(self, radek):
        indZav = self.vratIndexSlova(radek, '>(') + 2
        radekPredCislem = radek[0:indZav:1]

        radekNew = radek.replace(radekPredCislem, '')
        paragSkutCislo = radekNew.replace(')</p>', '')

        return(paragSkutCislo)



    def zamenSeznamRadku(self, obsahHtml, seznamRadkuPoradi, strExpPred):

        obsahHtmlNew = []

        for i in range(len(obsahHtml)):
            cisloParagrafu = self.vratCisloParagrafu(seznamRadkuPoradi, i)
            if(cisloParagrafu > -1):
                strOrig = obsahHtml[i]
                strNew = self.zamenCislo(strOrig, strExpPred, str(cisloParagrafu))
            else:
                strNew = obsahHtml[i]

            obsahHtmlNew.append(strNew)

        return(obsahHtmlNew)


    def vratCisloParagrafu(self, seznamRadkuPoradi, indexExp):

        cisloParagrafu = -1

        for i in range(len(seznamRadkuPoradi)):
            indexRadku = seznamRadkuPoradi[i][0]
            if(indexRadku == indexExp):
                cisloParagrafu = seznamRadkuPoradi[i][1]
                break

        return(cisloParagrafu)


    # vrati seznam vsech indexu radku, na kterych budou zamenovany cisla paragrafu nebo id
    def vratSeznamVsechIndexuRadku(self, obsahHtml, strExpPred):

        seznamRadkuProZmenu = []

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]
            radek = self.opravRadekNaP(radek)
            jeToRadekProZmenu = self.detekujPritomnostSlova(radek, strExpPred)

            if(jeToRadekProZmenu == True):
                seznamRadkuProZmenu.append(i)

        return(seznamRadkuProZmenu)


    # radek muze obsahovat napr: '<p style="top:-15px;">(1)</p>' - pak ho nelze detekovat
    #aby bylo ho mozne detekovat, prevede se na radek '<p>(1)</p>''
    def opravRadekNaP(self, radek):

        radekObsahujeP = self.detekujPritomnostSlova(radek, '<p')

        if(radekObsahujeP == True):
            indZav = self.vratIndexSlova(radek, ">(")
            subStrRadek = radek[0:indZav:1]
            radekOpr = radek.replace(subStrRadek, '<p')

        else:
            radekOpr = radek

        return(radekOpr)


    # k cislum z pole "seznamRadkuProZmenu" priradi cisla paragrafu, ktere budou menena
    def priradKIndexumRadkuJejichCislaParag(self, seznamRadkuProZmenu, prvniAPosledniIndexPole):

        seznamRadkuProZmenuPoradi = []

        for i in range(len(seznamRadkuProZmenu)):
            indexRadku = seznamRadkuProZmenu[i]
            poradi = self.vratPoradiIntervaluDleIndexu(prvniAPosledniIndexPole, indexRadku)

            indexAPoradi = []
            indexAPoradi.append(indexRadku)
            indexAPoradi.append(poradi)

            seznamRadkuProZmenuPoradi.append(indexAPoradi)

        return(seznamRadkuProZmenuPoradi)


    def vratPoradiIntervaluDleIndexu(self, prvniAPosledniIndexPole, index):

        poradi = -1

        for i in range(len(prvniAPosledniIndexPole)):
            prvniAPosledniIndex = prvniAPosledniIndexPole[i]
            IndexJeVIntervalu = self.detekujZdaIndexJeVIntervalu(prvniAPosledniIndex, index)

            if(IndexJeVIntervalu == True):
                poradi = i + 1
                break

        return(poradi)



    # detekuje zda index je mezi prvnim a poslednim indexem
    def detekujZdaIndexJeVIntervalu(self, prvniAPosledniIndex, indexExp):

        prvniIndex = prvniAPosledniIndex[0]
        posledniIndex = prvniAPosledniIndex[1]
        IndexJeVIntervalu = False

        if(indexExp >= prvniIndex):
            if(indexExp <= posledniIndex):
                IndexJeVIntervalu = True


        return(IndexJeVIntervalu)



    def zamenCislo(self, strOrig, strExpPred, cisloNew):

        if(self.detekujPritomnostSlova(strOrig, '<p style="top:') == True):
            strExpPred =  self.opravStrOrig(strExpPred, strOrig)

        rozdelenyString = self.vratRozdelenyString(strOrig, strExpPred)
        substrOrigNew = self.vratStaryANovySubstringKNahrazeni(rozdelenyString, cisloNew)

        #nahradi substring, cimz zmeni ID
        strNew = strOrig.replace(substrOrigNew[0], substrOrigNew[1])

        return(strNew)


    def opravStrOrig(self, strExpPred, strOrig):
        radekNew = self.opravRadekNaP(strOrig)
        radekNew2 = radekNew.replace(strExpPred, '')
        strExpPred2 = strOrig.replace(radekNew2, '')

        return(strExpPred2)


    def vratStaryANovySubstringKNahrazeni(self, rozdelenyStringOrig, cisloNew):

        substrOrigNew = []
        rozdelenyStringNew = []


        for i in range(len(rozdelenyStringOrig)):
            polozkaOrig = rozdelenyStringOrig[i]

            if(i == 1):
                polozkaOrig = cisloNew

            rozdelenyStringNew.append(polozkaOrig)


        substrOrig = self.sestavSubstrZPole(rozdelenyStringOrig)
        substrNew = self.sestavSubstrZPole(rozdelenyStringNew)

        substrOrigNew.append(substrOrig)
        substrOrigNew.append(substrNew)

        return(substrOrigNew)


    def sestavSubstrZPole(self, substrPole):

        subStrStr = ""

        for i in range(len(substrPole)):
            polozka = substrPole[i]
            subStrStr = subStrStr + polozka

        return(subStrStr)



    # vrati originalni cislo v Id
    # def vratOrigCislo(self, strOrig, strExpPred):
    def vratRozdelenyString(self, strOrig, strExpPred):

        indexPrv = strOrig.index(strExpPred)
        indexPos = indexPrv + len(strExpPred)

        substr = strOrig[indexPos:len(strOrig):1]

        vsechmnoZaCislem = self.vratVsechnoZaCislem(substr)
        cislo = substr.replace(vsechmnoZaCislem, '')

        rozdelenyString = []
        rozdelenyString.append(strExpPred)
        rozdelenyString.append(cislo)
        rozdelenyString.append(vsechmnoZaCislem)

        return(rozdelenyString)



    def vratVsechnoZaCislem(self, strOrig):

        for i in range(len(strOrig)):
            znak = strOrig[i]

            if(znak.isnumeric() == False):
                prvniIndexPismene = i
                break

        vsechmnoZaCislem = strOrig[prvniIndexPismene:len(strOrig):1]

        return(vsechmnoZaCislem)

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


    def vratIndexSlova(self, radek, slovo):

        try:
            index = radek.index(slovo)
        except:
            index = -1

        return(index)