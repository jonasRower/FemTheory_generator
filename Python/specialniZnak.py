# zde se pridavaji specialni znaky jako napr:
# '[' nebo ']'

# dela se to zvlast, jelikoz do tabulky nejdou pridavat parove znaky bez druhého znaku (v páru)
# nejde to proto, protoze druhy (parovy znak) je pridan v jine bunce tabulky
# resi se to tedy tak, ze se prida <p> na z-index:-1, cimz vzorec dojde do pozadi
# pricemz vsechny znaky zustanou skryty v pozadi, avsak jen pozadovane znaky '[' nebo ']' zustanou videt

# aby se neovlivnoval stavajici kod, je pridan na konec html <p class="znaky">
# ten je v css nastaven s absolutni souradnici,
# souradnice se dopocitava v teto tride

import posunTextu

class pridejSpecialniZnaky:

    def __init__(self, obsahHtml):

        IdExp = 'exp-1_col-4'
        prictiRadky = 90

        self.posunTop = -50
        self.posunLeft = 15


        #poleRadku = self.vratPoleRadkuHtml('exp-3_col-4', -50, 15)
        #self.obsahHtmlNew = self.pridejPoleRadkuDoHtml(obsahHtml, poleRadku)


        # nejdriv odebere puvodni specZnaky
        obsahHtmlBezZnaku = self.odeberDivSpecZnaky(obsahHtml)

        # pak prida vsechny spec znaky znovu
        self.obsahHtmlNew = self.pridejSpecZnakyDoHtml(obsahHtmlBezZnaku)
        print("")


    # vrati data - pro tisk do html

    def getIndexyRadkuLatex(self):
        return(self.indexyRadkuLatex)

    def getObsahHtmlNew(self):
        return(self.obsahHtmlNew)



    def pridejSpecZnakyDoHtml(self, obsahHtmlNew):

        indexyRadkuTd = self.ziskejIndexyRadkuTd(obsahHtmlNew)
        indexyRadkuLatex = self.vratIndexyRadkuSLatexem(obsahHtmlNew, indexyRadkuTd)
        ideVsechRadkuBlokuHtml = self.vratIdVsechRadku(obsahHtmlNew, indexyRadkuTd)

        radkySpecZnakyId = self.selektujJenBunkyZacinajiciSpecZnakem(indexyRadkuLatex, ideVsechRadkuBlokuHtml, obsahHtmlNew, indexyRadkuTd)
        dataSpecZnaky = self.pripravDataProPoleRadkuHtml(radkySpecZnakyId)
        #obsahHtmlNew = self.opravHtml(obsahHtmlNew, radkySpecZnakyId)

        for i in range(len(dataSpecZnaky)):
            idBlokuHtmlData = dataSpecZnaky[i]
            poleRadku = self.vratPoleRadkuHtml(idBlokuHtmlData, self.posunTop, self.posunLeft)
            obsahHtmlNew = self.pridejPoleRadkuDoHtml(obsahHtmlNew, poleRadku)

        return(obsahHtmlNew)



    # aby mohl pridavat nove radky spec znaku, je treba odebirat ty stavajici
    def odeberDivSpecZnaky(self, obsahHtml):

        indexRadkuPid1 = self.vyhledejPrvniRadek(obsahHtml, '<p id="[|exp-', len(obsahHtml))
        indexRadkuPid2 = self.vyhledejPrvniRadek(obsahHtml, '<p id="(|exp-', indexRadkuPid1)
        indexRadkuPid3 = self.vyhledejPrvniRadek(obsahHtml, '<p id="{|exp-', indexRadkuPid2)
        indexRadkuPid4 = self.vyhledejPrvniRadek(obsahHtml, '<p id="]|exp-', indexRadkuPid3)
        indexRadkuPid5 = self.vyhledejPrvniRadek(obsahHtml, '<p id=")|exp-', indexRadkuPid4)
        indexRadkuPid6 = self.vyhledejPrvniRadek(obsahHtml, '<p id="}|exp-', indexRadkuPid5)

        indexRadkuBody = self.vyhledejPrvniRadek(obsahHtml, '</body>', len(obsahHtml))
        indexRadkuHtml = self.vyhledejPrvniRadek(obsahHtml, '</html>', len(obsahHtml))
        indexRadkuPid = min(indexRadkuPid1, indexRadkuPid2, indexRadkuPid3, indexRadkuPid4, indexRadkuPid5, indexRadkuPid6)

        obsahHtml1 = obsahHtml[0:indexRadkuPid-2:1]
        obsahHtml2 = obsahHtml[indexRadkuBody:len(obsahHtml):1]
        #obsahHtml2 = obsahHtml[indexRadkuBody:indexRadkuHtml:1]

        obsahHtmlBezSpecZnaku = obsahHtml1 + obsahHtml2


        return(obsahHtmlBezSpecZnaku)


    def vyhledejPrvniRadek(self, obsahHtml, strExp, hledejDo):

        vratIndexRadku = hledejDo

        for i in range(hledejDo):
            radek = obsahHtml[i]
            radekObsahujeStrExp = self.detekujPritomnostSlova(radek, strExp)
            if(radekObsahujeStrExp == True):
                vratIndexRadku = i
                break

        return(vratIndexRadku)



    # ze stavajiciho html odebere spec. znaky, tak aby je pridal zvlast a nebyl 2x
    def opravHtml(self, obsahHtmlNew, radkySpecZnakyId):

        for i in range(len(radkySpecZnakyId)):
            radkyData = radkySpecZnakyId[i]
            indexRadku = radkyData[4] + 2
            radekOrig = radkyData[5]
            radekTrim = radekOrig.strip()
            radekNahrad = radkyData[0]

            radekNew = radekOrig.replace(radekTrim, radekNahrad)
            obsahHtmlNew[indexRadku] = radekNew

        return(obsahHtmlNew)


    def pripravDataProPoleRadkuHtml(self, radkySpecZnakyId):

        dataSpecZnaky = []

        for i in range(len(radkySpecZnakyId)):
            leftRightIdData = radkySpecZnakyId[i]
            left = leftRightIdData[1]
            right = leftRightIdData[2]
            id = leftRightIdData[3]

            if(left != ''):
                dataRadek = []
                dataRadek.append(left)
                dataRadek.append(id)
                dataSpecZnaky.append(dataRadek)

            if (right != ''):
                dataRadek = []
                dataRadek.append(right)
                dataRadek.append(id)
                dataSpecZnaky.append(dataRadek)

        return(dataSpecZnaky)


    def selektujJenBunkyZacinajiciSpecZnakem(self, indexyRadkuLatex, ideVsechRadkuBlokuHtml, obsahHtml, indexyRadkuTd):

        # vytvori pole vsech Id se specialnimi znaky
        # soucasne jej doplni o novy radek (redukovany) a index radku v html, ktery bude nahrazen
        radkySpecZnakyId = []

        for i in range(len(indexyRadkuLatex)):
            indexRadku = indexyRadkuLatex[i]
            radekOrig = obsahHtml[indexRadku]
            radek = radekOrig.strip()

            # vrati specialni znaky z radku (resp. jen ty na zacatku a konci vyrazu)
            # a soucasne je odmaze z radku
            radekSpecZnaky = self.odeberZRadkuSpecZnaky(radek)
            radekSpecZnakyObsahujeLeftRight = self.detekujLeftRight(radekSpecZnaky)

            if(radekSpecZnakyObsahujeLeftRight == True):
                id = ideVsechRadkuBlokuHtml[i]
                indTd = indexyRadkuTd[i]
                radekSpecZnaky.append(id)
                radekSpecZnaky.append(indTd)
                radekSpecZnaky.append(radekOrig)

                radkySpecZnakyId.append(radekSpecZnaky)

        return(radkySpecZnakyId)



    def detekujLeftRight(self, radekSpecZnaky):

        radekSpecZnakyObsahujeLeftRight = self.detekujPritomnostSlova(radekSpecZnaky, '\\left[')
        if(radekSpecZnakyObsahujeLeftRight == False):
            radekSpecZnakyObsahujeLeftRight = self.detekujPritomnostSlova(radekSpecZnaky, '\\right')

        return(radekSpecZnakyObsahujeLeftRight)



    def odeberZRadkuSpecZnaky(self, radek):

        indexyVsechZnaku = self.vratSeznamOddelovacu(radek)
        vsechnySubStringy = self.vratVsechnySubStringy(radek, indexyVsechZnaku)
        specZnaky = self.ziskejSpecZnaky(vsechnySubStringy)

        if(len(specZnaky) > 0):

            specZnakyAdekv = self.vyberPouzeAdekvatniSpecZnaky(specZnaky, radek)
            radekNew = self.vratRadekBezSpecZnaku(radek, specZnakyAdekv)
            zavOtStr = specZnakyAdekv[0][2]
            zavZavStr = specZnakyAdekv[1][2]

            radekSpecZnaky = self.pridejZapisDoPole(radekNew, zavOtStr, zavZavStr)

        else:
            radekSpecZnaky = self.pridejZapisDoPole(radek, '', '')

        return(radekSpecZnaky)


    # vrati bud prvni nebo posledni index, dle substringu
    #def vratPrvniPosledniIndex(self, ):


    def vratRadekBezSpecZnaku(self, radek, specZnakyAdekv):

        # ponecha jen stred stringu ohranicene indexy:
        indPonechStart = specZnakyAdekv[0][1]+1
        indponechEnd = specZnakyAdekv[1][0]

        ponechRadek = radek[indPonechStart:indponechEnd:1]

        return(ponechRadek)


    def vyberPouzeAdekvatniSpecZnaky(self, specZnaky, radek):

        specZnakyNew = []
        zavOtNalezena = False
        zavZavNalezena = False

        if(len(specZnaky) > 0):

            # prvni znak
            specZnak = specZnaky[0][2]
            specZnakObsahujeZavorku = self.detekujPritomnostSlova(specZnak, '\\left[')

            if(specZnakObsahujeZavorku == True):
                zavOtNalezena = True
                specZnakNew = self.pridejZapisDoPole(specZnaky[0][0], specZnaky[0][1], specZnak)
                specZnakyNew.append(specZnakNew)

            # posledni znak
            poslInd = len(specZnaky)-1
            specZnak = specZnaky[poslInd][2]
            specZnakObsahujeZavorku = self.detekujPritomnostSlova(specZnak, '\\right')

            if (specZnakObsahujeZavorku == True):
                zavZavNalezena = True
                specZnakNew = self.pridejZapisDoPole(specZnaky[poslInd][0], specZnaky[poslInd][1], specZnak)
                specZnakyNew.append(specZnakNew)

            # pokud zavorka neni nalezena, pak se data opravi
            specZnakyNew = self.opravPolePokudZavorkaNalezenaNeni(zavOtNalezena, zavZavNalezena, specZnakyNew, radek)

        return(specZnakyNew)


    def opravPolePokudZavorkaNalezenaNeni(self, zavOtNalezena, zavZavNalezena, specZnaky, radek):

        # nastavi jako vychozi, pokud jsou data OK
        specZnakyNew = specZnaky

        # pokud OK nejsou, pak se data prepisi
        if(zavOtNalezena == False):
            specZnakyNew = []
            specZnakyRadek = []
            specZnakyRadek.append(0)
            specZnakyRadek.append(0)
            specZnakyRadek.append('')

            specZnakyNew.append(specZnakyRadek)
            specZnakyNew.append(specZnaky[0])


        if (zavZavNalezena == False):
            specZnakyNew = []
            specZnakyRadek = []
            specZnakyRadek.append(len(radek)-1)
            specZnakyRadek.append(len(radek)-1)
            specZnakyRadek.append('')

            specZnakyNew.append(specZnaky[0])
            specZnakyNew.append(specZnakyRadek)

        return(specZnakyNew)



    def ziskejSpecZnaky(self, vsechnySubStringy):

        specZnaky = []

        for i in range(len(vsechnySubStringy)):
            substrRadek = vsechnySubStringy[i]

            specZnaky = self.pridejSpecZnak(substrRadek, '\\left[', specZnaky)
            specZnaky = self.pridejSpecZnak(substrRadek, '\\right', specZnaky)

        return(specZnaky)


    def pridejSpecZnak(self, substrRadek, specZnak, specZnaky):

        radek = substrRadek[2]
        radekBezSpecZnaku = radek.replace(specZnak, '')
        radekSpecZnak = radek.replace(radekBezSpecZnaku, '')

        radekObsahujeSpecZnak = self.detekujPritomnostSlova(radekSpecZnak, specZnak)


        if(radekObsahujeSpecZnak == True):
            radekNew = specZnak + radekBezSpecZnaku
            specZnakyRadek = self.pridejZapisDoPole(substrRadek[0], substrRadek[1], radekNew)

            specZnaky.append(specZnakyRadek)

        return(specZnaky)


    def pridejZapisDoPole(self, polA, polB, polC):

        pole = []

        pole.append(polA)
        pole.append(polB)
        pole.append(polC)

        return(pole)


    def vratSeznamOddelovacu(self, radek):

        lomitkaIndexy = self.vratIndexyZnakuDleSpecZnaku(radek, '\\')
        mezeryIndexy = self.vratIndexyZnakuDleSpecZnaku(radek, ' ')
        zavorkyHranIndexy = self.vratIndexyZnakuDleSpecZnaku(radek, '[')
        zavorkyHranIndexyZav = self.vratIndexyZnakuDleSpecZnaku(radek, ']')
        zavorkyIndexy = self.vratIndexyZnakuDleSpecZnaku(radek, '{')

        indexyVsechZnaku = [0]
        indexyVsechZnaku = indexyVsechZnaku + lomitkaIndexy
        indexyVsechZnaku = indexyVsechZnaku + mezeryIndexy
        indexyVsechZnaku = indexyVsechZnaku + zavorkyHranIndexy
        indexyVsechZnaku = indexyVsechZnaku + zavorkyHranIndexyZav
        indexyVsechZnaku = indexyVsechZnaku + zavorkyIndexy
        indexyVsechZnaku.sort()

        return(indexyVsechZnaku)


    def vratVsechnySubStringy(self, radek, indexyVsechZnaku):

        vsechnySubStringy = []

        for i in range(len(indexyVsechZnaku)-1):
            indexStart = indexyVsechZnaku[i]
            indexEnd = indexyVsechZnaku[i+1]

            vsechnySubStringy = self.zapisSubstrDoPole(radek, indexStart, indexEnd, vsechnySubStringy)


        # prida jeste posledni substring
        indexStart = indexyVsechZnaku[len(indexyVsechZnaku)-1]
        indexEnd = len(radek)

        vsechnySubStringy = self.zapisSubstrDoPole(radek, indexStart, indexEnd, vsechnySubStringy)



        return(vsechnySubStringy)


    def zapisSubstrDoPole(self, radek, indexStart, indexEnd, vsechnySubStringy):

        indexStartEndSubStr = []

        substr = radek[indexStart:indexEnd:1]
        substr = substr.replace('\\left', '\\left[')

        indexStartEndSubStr.append(indexStart)
        indexStartEndSubStr.append(indexEnd)
        indexStartEndSubStr.append(substr)
        vsechnySubStringy.append(indexStartEndSubStr)

        return(vsechnySubStringy)


    def vratradekBezZavorky(self, radek, indexy):

        try:
            indexStart = indexy[0]
            indexEnd = indexy[1]

            if(indexStart == 0):
                radekNew = radek[indexEnd:len(radek):1]

            if(indexEnd == len(radek)):
                radekNew = radek[0:indexStart:1]
        except:
            radekNew = radek

        return(radekNew)


    #def vratIndexySubstringu(self, radek, subString):




    # pokud se jedna o zavorku otevrenou vybere jen tu dvojici, ktera zacina 0
    def vyberIndexyDleKriteriaOtev(self, indexyZavorekAll):

        vratIndexy = []

        for i in range(len(indexyZavorekAll)):
            indexZavorek = indexyZavorekAll[i]
            if(indexZavorek[0] == 0):
                vratIndexy = indexZavorek

        return(vratIndexy)


    # pokud se jedna o zavorku zavrenou vybere jen tu dvojici, ktera konci s len(radek)
    def vyberIndexyDleKriteriaZav(self, indexyZavorekAll, radek):

        vratIndexy = []

        for i in range(len(indexyZavorekAll)):
            indexZavorek = indexyZavorekAll[i]
            if (indexZavorek[1] == len(radek)):
                vratIndexy = indexZavorek

        return (vratIndexy)






    def vratIndexyZnakuDleSpecZnaku(self, radek, specZnak):

        nalezeneZnakyIndexy = []
        radekNew = radek
        posledniIndex = 0
        for i in range(len(radek)):

            try:
                indexStart = radekNew.index(specZnak)
                indexEnd = indexStart + len(specZnak)

                nalezeneZnakyIndexy.append(indexStart + posledniIndex)
                posledniIndex = nalezeneZnakyIndexy[len(nalezeneZnakyIndexy)-1] + 1
                radekNew = radekNew[indexEnd:len(radekNew):1]


            except:
                break

        return(nalezeneZnakyIndexy)


    def vratIndexyRadkuSLatexem(self, blokHtml, indexyRadkuTd):

        indexyRadkuLatex = []

        for i in range(len(indexyRadkuTd)):
            indexRadku1 = indexyRadkuTd[i]
            try:
                indexRadku1 = indexyRadkuTd[i]
                indexRadku2 = indexyRadkuTd[i+1]
            except:
                indexRadku2 = -1

            latexIndex = self.vratIndexRadkuLatex(blokHtml, indexRadku1, indexRadku2)
            indexyRadkuLatex.append(latexIndex)


        return(indexyRadkuLatex)


    def vratIdVsechRadku(self, blokHtml, indexyRadkuTd):

        ideVsechRadkuBlokuHtml = []

        for i in range(len(indexyRadkuTd)):
            indexRadku = indexyRadkuTd[i]
            radek = blokHtml[indexRadku]
            idZRadku = self.vratIdZRadku(radek)

            ideVsechRadkuBlokuHtml.append(idZRadku)

        return(ideVsechRadkuBlokuHtml)


    def vratIdZRadku(self, radek):

        radek = radek.strip()
        vratRadek = ''

        radekSplit = radek.split(' ')

        for i in range(len(radekSplit)):
            radekSpl = radekSplit[i]
            radekObsahujeId = self.detekujPritomnostSlova(radekSpl, 'id=')
            if(radekObsahujeId == True):
                vratRadek = radekSpl
                vratRadek = vratRadek.replace('>', '')
                vratRadek = vratRadek.replace('id=', '')
                vratRadek = vratRadek.replace('"', '')

        return(vratRadek)




    def vratIndexRadkuLatex(self, blokHtml, indexRadkuTd1, indexRadkuTd2):

        latexStrBool = False
        latexStart = -1
        latexEnd = -1

        for i in range(len(blokHtml)):
            i1 = indexRadkuTd1 + i

            if(i1 == indexRadkuTd2):
                break

            if (latexStart * latexEnd > 1):
                break


            radek = blokHtml[i1]

            if(latexStrBool == False):
                if(radek.strip() == '\\['):
                    latexStart = i1
                    latexStrBool = True

            else:
                if (radek.strip() == '\\]'):
                    latexEnd = i1
                    latexStrBool = False


        latexIndex = int((latexStart + latexEnd)/2)

        return(latexIndex)


    def ziskejIndexyRadkuTd(self, blokHtml):

        indexyRadkuTd = []

        for i in range(len(blokHtml)):
            radek = blokHtml[i]
            jednaSeOradekTd = self.detekujPritomnostSlova(radek, '<td style=')
            if(jednaSeOradekTd == True):
                indexyRadkuTd.append(i)

        return(indexyRadkuTd)



    def pridejPoleRadkuDoHtml(self, obsahHtml, poleRadku):

        # kdyby nenalezl nic
        obsahHtmlNew = obsahHtml.copy()

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]
            radekObsahujeBody = self.detekujPritomnostSlova(radek, '</body>')

            if(radekObsahujeBody == True):
                indexRadkuBodyEnd = i
                obsahHtmlPredBody = obsahHtml[0:indexRadkuBodyEnd - 1:1]
                obsahHtmlBodyEnd = obsahHtml[indexRadkuBodyEnd:len(obsahHtml):1]

                obsahHtmlNew = obsahHtmlPredBody.copy()
                obsahHtmlNew = obsahHtmlNew + poleRadku
                obsahHtmlNew = obsahHtmlNew + obsahHtmlBodyEnd
                print("")

        return(obsahHtmlNew)


    def vratPoleRadkuHtml(self, idBlokuHtmlData, posunTop, posunLeft):

        id = idBlokuHtmlData[1]
        leftRight = idBlokuHtmlData[0]
        zavorka = leftRight[-1]
        if (zavorka == 't'):
            zavorka = ']'       # asi bude treba v budoucnu opravit

        radkyProSkrytyParag = []
        radkyProSkrytyParag.append('    <div>')
        radekIdSpec = '        <p id="' + zavorka + '|' + id + '" posunTop="' + str(posunTop) + '" posunLeft="' + str(posunLeft) + '" class="znaky">'
        radkyProSkrytyParag.append(radekIdSpec)
        radkyProSkrytyParag.append('        ')
        radkyProSkrytyParag.append('        </p>')
        radkyProSkrytyParag.append('    </div>')

        return (radkyProSkrytyParag)


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

