# tento modul aktualizuje html.
# tzn. vytvori nove html z temp.html
# vytvori se 2 nove html - "htmelText.html" a "specZnaky.html"

import posunTextu
import specialniZnak


class aktualizaceSpecZnaky:

    def __init__(self, obsahHtmlTemp, obsahHtmlText, obsahSpecZnaky):

        # ziska data k oprave zavorek
        self.opravaZavorekData = self.vratOpravaZavorekData()

        # obnovi specialni znaky
        obnovSpecZnaky = specialniZnak.pridejSpecialniZnaky(obsahHtmlTemp)
        obsahHtmlTemp = obnovSpecZnaky.getObsahHtmlNew()

        tempSpecZnaky = specialniZnak.pridejSpecialniZnaky(obsahHtmlTemp)
        obsahHtmlTemp = tempSpecZnaky.getObsahHtmlNew()

        self.obsahHtmlTextNew = self.vratHtmlNew(obsahHtmlTemp, obsahHtmlText, True)
        self.specZnakyNew = self.vratHtmlNew(obsahHtmlTemp, obsahSpecZnaky, False)
        self.obsahHtmlTemp = obsahHtmlTemp


        # tiskni html, s tim, ze se nahradi Latexy
        #self.specZnakyNewLatex = self.nahradOriginalniLatexy(specZnakyNew, seznamRadkuPtdHtmlTextSpecZnaky)


    def getObsahHtmlTextNew(self):
        return(self.obsahHtmlTextNew)

    def getObsahSpecZnakyNew(self):
        return(self.specZnakyNew)

    def getObsahHtmlTemp(self):
        return(self.obsahHtmlTemp)



    # je potreba prepsat Latexy v "specZnakyNew" s originalniho z "radkyPtdSpecZnaky"
    # to se nalezne v "seznamRadkuPtdHtmlTextSpecZnaky"
    def nahradOriginalniLatexy(self, specZnakyNew, seznamRadkuPtdHtmlTextSpecZnaky):

        for i in range(len(seznamRadkuPtdHtmlTextSpecZnaky)):
            indexyRadku = seznamRadkuPtdHtmlTextSpecZnaky[i]
            indexRadku = indexyRadku[1]
            latexNew = indexyRadku[5]

            indSpecZnakNew = indexRadku + 2
            specZnakyNew[indSpecZnakNew] = latexNew

        return(specZnakyNew)


    def vratSeznamRadkuPtdHtmlTextSpecZnaky(self, obsahHtmlTemp, obsahHtml, textHtmlBool):

        radkyPtdHtmlText = posunTextu.posunText(obsahHtmlTemp, None, None, None)
        radkyPtdSpecZnaky = posunTextu.posunText(obsahHtml, None, None, None)

        htmlTextPtd = radkyPtdHtmlText.getSeznamRadkuPTd()
        specZnakyPtd = radkyPtdSpecZnaky.getSeznamRadkuPTd()

        seznamRadkuPtdTemp = self.vratRadkyIdTd(obsahHtmlTemp, htmlTextPtd)
        seznamRadkuPtdHtml = self.vratRadkyIdTd(obsahHtml, specZnakyPtd)

        seznamRadkuPtdHtml = self.vyhledejIndexyRadkuHtmlTextSpecZnaky(seznamRadkuPtdTemp, seznamRadkuPtdHtml)
        seznamRadkuPtdHtml = self.vyhledejAZapisLatexy(seznamRadkuPtdHtml, obsahHtmlTemp, textHtmlBool)

        return(seznamRadkuPtdHtml)


    # prevadi temp.html na specZnaky.html nebo htmlText.html
    def vratHtmlNew(self, obsahHtmlTemp, obsahHtml, textHtmlBool):

        indexRadkuP11HtmlTemp = self.vratIndexRadku(obsahHtmlTemp, '<div id="p1-')
        indexRadkuP11Html = self.vratIndexRadku(obsahHtml, '<div id="p1-')

        obsahHtmlTempDiv = obsahHtmlTemp[indexRadkuP11HtmlTemp:len(obsahHtmlTemp):1]
        obsahHtmlScript = obsahHtml[0:indexRadkuP11Html:1]
        htmlNew = obsahHtmlScript + obsahHtmlTempDiv

        seznamRadkuPtdHtmlTextSpecZnaky = self.vratSeznamRadkuPtdHtmlTextSpecZnaky(obsahHtmlTemp, htmlNew, textHtmlBool)

        # ulozi data pokud momentalne kod bezi pro htmlText
        if(textHtmlBool == True):
            self.seznamRadkuPtdHtmlText = seznamRadkuPtdHtmlTextSpecZnaky
        else:
            # je potreba upravit seznam - porovnaji se data z htmlText.html (=self.seznamRadkuPtdHtmlText)
            seznamRadkuPtdHtmlTextSpecZnaky = self.upravSeznamRadkuPtd(self.seznamRadkuPtdHtmlText, seznamRadkuPtdHtmlTextSpecZnaky)

        htmlNew = self.zapisLatexyDoHtml(seznamRadkuPtdHtmlTextSpecZnaky, htmlNew)

        # opravi znaky dle toho zda se jedna o textHtml.html nebo specZnaky.html
        htmlNew = self.opravSpecZnaky(textHtmlBool, htmlNew)

        return(htmlNew)


    # opravi spec znaky
    def opravSpecZnaky(self, textHtmlBool, html):

        for i in range(len(html)):
            radek = html[i]
            jednaSeOIRadkuZnaky = self.detekujPritomnostSlova(radek, 'class="znaky"')
            if(jednaSeOIRadkuZnaky == True):
                radekNew = self.vyhledejOpravaZavorekData(radek, textHtmlBool)
                html[i] = radekNew

        return(html)


    def vyhledejOpravaZavorekData(self, radek, textHtmlBoolExp):

        for i in range(len(self.opravaZavorekData)):
            oprZav = self.opravaZavorekData[i]
            textHtmlBool = oprZav[0]
            if(textHtmlBool == textHtmlBoolExp):
                zavOt = oprZav[1]
                colOt = oprZav[2]
                posunOt = oprZav[3]
                zavZav = oprZav[4]
                colZav = oprZav[5]
                posunZav = oprZav[6]

                if(posunZav == '-30'):
                    print()

                jednaSeOZavOt = self.detekujZdaSeJednaOZavOt(radek)

                if(jednaSeOZavOt == True):
                    radekNew = self.generujRadekNew(radek, colOt, posunOt)

                if (jednaSeOZavOt == False):
                    radekNew = self.generujRadekNew(radek, colZav, posunZav)

                break

        return(radekNew)


    def detekujZdaSeJednaOZavOt(self, radek):

        zavOt = False

        attrId = self.ziskejAtribut(radek, 'id')
        prvniZnak = attrId[1]

        if(prvniZnak == ']'):
            zavOt = True
        if(prvniZnak == '['):
            zavOt = False

        return(zavOt)



    def generujRadekNew(self, radek, col, posunLeft):

        # ziska atribut id
        attrId = self.ziskejAtribut(radek, 'id')

        #opravi col
        atributIdNew = self.opravAtrCol(attrId, col)

        # prepise col
        radekNew =  self.prepisAtrDoRadku('id', attrId, atributIdNew, radek)

        #prepise posunLeft
        attrPosun = self.ziskejAtribut(radek, 'posun')
        radekNew = self.prepisAtrDoRadku('posunLeft', attrPosun, '"' + posunLeft + '"', radekNew)

        return(radekNew)



    def prepisAtrDoRadku(self, par, attr, attrNew, radek):

        parAtrOrig = par + '=' + attr
        parAtrOrigNew = par + '=' + attrNew
        radekNew = radek.replace(parAtrOrig, parAtrOrigNew)

        return(radekNew)



    def ziskejAtribut(self, radekOrig, paramExp):

        radek = radekOrig.strip()
        paramSplit = radek.split(' ')
        radekParam = self.vratRadekObsahujiciSubstr(paramSplit, paramExp)
        atribut = self.vratAtribut(radekParam)

        return(atribut)


    def vratAtribut(self, radek):

        radekSplit = radek.split('=')
        atribut = radekSplit[1]

        return(atribut)


    def opravAtrCol(self, radekAtr, ColNumPos):

        colSplit = radekAtr.split('_')
        colStr = colSplit[1]
        colStr = colStr.replace('"', '')
        colNumStr = colStr.replace('col-', '')
        colNum = int(colNumStr)
        colNumNew = colNum + int(ColNumPos)
        colStrNew = 'col-' + str(colNumNew)
        radekStrNew = radekAtr.replace(colStr, colStrNew)

        return(radekStrNew)


    def vratRadekObsahujiciSubstr(self, pole, substr):

        vratRadek = ''

        for i in range(len(pole)):
            polItem = pole[i]
            polItemObsahujeSubstr = self.detekujPritomnostSlova(polItem, substr)
            if(polItemObsahujeSubstr == True):
                vratRadek = polItem

        return(vratRadek)



    def upravSeznamRadkuPtd(self, seznamRadkuPtdHtmlText, seznamRadkuPtdSpecZnaky):

        nahradniString = '\left[\\frac{1^1}{1_1}\\right]_0^L'
        nahradniStringL = '\left[\\frac{1^1}{1_1}'
        nahradniStringR = '\\right]_0^L'

        for i in range(len(seznamRadkuPtdSpecZnaky)):
            radekB = seznamRadkuPtdSpecZnaky[i][5].strip()
            print("")

            if(radekB == '\\left['):
                strNew = seznamRadkuPtdHtmlText[i-1][5].strip() + nahradniString
                seznamRadkuPtdSpecZnaky[i-1][5] = seznamRadkuPtdSpecZnaky[i][5].replace(radekB, strNew)
                seznamRadkuPtdSpecZnaky[i][5] = seznamRadkuPtdHtmlText[i][5]

            if(radekB == '\\right]'):
                strNew = nahradniStringL + seznamRadkuPtdHtmlText[i][5].strip() + nahradniStringR
                seznamRadkuPtdSpecZnaky[i][5] = seznamRadkuPtdSpecZnaky[i][5].replace(radekB, strNew)

            if(radekB == ''):
                seznamRadkuPtdSpecZnaky[i][5] = seznamRadkuPtdHtmlText[i][5]


        return(seznamRadkuPtdSpecZnaky)



    def zapisLatexyDoHtml(self, seznamRadkuPtdHtmlTextSpecZnaky, obsahHtml):

        for i in range(len(seznamRadkuPtdHtmlTextSpecZnaky)):
            indexy = seznamRadkuPtdHtmlTextSpecZnaky[i]
            indHtml = indexy[1] + 2
            LaTexNew = indexy[5]

            obsahHtml[indHtml] = LaTexNew

        return(obsahHtml)


    def vyhledejAZapisLatexy(self, seznamRadkuPtdHtmlTextSpecZnaky, obsahHtmlText, textHtmlBool):

        seznamRadkuPtdHtmlTextSpecZnakyNew = []

        for i in range(len(seznamRadkuPtdHtmlTextSpecZnaky)):
            indPtdId = seznamRadkuPtdHtmlTextSpecZnaky[i]
            indPtdHtmlText = indPtdId[0]
            indPtdSpecZnak = indPtdId[1]

            LatexTemp = self.vratRadekLaTexu(obsahHtmlText, indPtdHtmlText)
            LatexHtml = self.vratLatexyProHtmlTextNeboSpecZnaky(LatexTemp, textHtmlBool)

            indPtdIdNew = []
            indPtdIdNew.append(indPtdId[0])
            indPtdIdNew.append(indPtdId[1])
            indPtdIdNew.append(indPtdId[2])
            indPtdIdNew.append(indPtdId[3])

            indPtdIdNew.append(LatexTemp)
            indPtdIdNew.append(LatexHtml)

            seznamRadkuPtdHtmlTextSpecZnakyNew.append(indPtdIdNew)

        return(seznamRadkuPtdHtmlTextSpecZnakyNew)


    def vratLatexyProHtmlTextNeboSpecZnaky(self, radek, textHtmlBool):

        radekTrim = radek.strip()
        bezLeft = radekTrim.replace('\\left[', '')
        bezRight = radekTrim.replace('\\right]', '')

        if(radekTrim == bezRight):
            radekBez = bezLeft
        else:
            radekBez = bezRight


        if(textHtmlBool == True):
            vratradek = radek.replace(radekTrim, radekBez)
        else:
            vratradek = radek.replace(radekBez, '')

        return(vratradek)


    # vrati radek Latexu
    def vratRadekLaTexu(self, obsahHtml, indRadek):

        indRadekLaTex = indRadek + 2
        LatexStr = obsahHtml[indRadekLaTex]

        return(LatexStr)




    # vrati pole kde jsou napojeny cisla radku html textu se spec. znaky vzajemne na sebe
    def vyhledejIndexyRadkuHtmlTextSpecZnaky(self, seznamRadkuPtdHtmlText, seznamRadkuPtdSpecZnaky):

        seznamRadkuPtdHtmlTextSpecZnaky = []

        for i in range(len(seznamRadkuPtdHtmlText)):
            indPtdId = seznamRadkuPtdHtmlText[i]
            idHtmlText = indPtdId[2]
            if(idHtmlText != -1):
                indSpecZnak = self.vratIndexRadkuDleId(seznamRadkuPtdSpecZnaky, idHtmlText)

                indPtdIdNew = []
                indPtdIdNew.append(indPtdId[0])
                indPtdIdNew.append(indSpecZnak)
                indPtdIdNew.append(indPtdId[1])
                indPtdIdNew.append(indPtdId[2])

                seznamRadkuPtdHtmlTextSpecZnaky.append(indPtdIdNew)

        return(seznamRadkuPtdHtmlTextSpecZnaky)


    # vyhleda v seznamu radku ID-cko, ktere odpovida danemu indexu radku
    def vratIndexRadkuDleId(self, seznamRadkuPtd, idExp):

        indRadku = -1

        for i in range(len(seznamRadkuPtd)):
            indPtdId = seznamRadkuPtd[i]
            id = indPtdId[2]
            if(id == idExp):
                indRadku = indPtdId[0]
                break

        return(indRadku)


    # vrati seznam radku Id pro indexy radku Td
    def vratRadkyIdTd(self, obsahHtml, seznamRadkuPtd):

        seznamRadkuPtdNew = []

        for i in range(len(seznamRadkuPtd)):
            radekPtd = seznamRadkuPtd[i]
            pTd = radekPtd[1]
            if(pTd == 'td'):
                indexRadku = radekPtd[0]
                radek = obsahHtml[indexRadku]
                idRadku = self.vratIdZRadku(radek)
            else:
                idRadku = -1

            radekPtd.append(idRadku)
            seznamRadkuPtdNew.append(radekPtd)


        return(seznamRadkuPtdNew)


    def vratIdZRadku(self, radek):

        radek = radek.strip()
        vratRadek = ''

        radekSplit = radek.split(' ')

        for i in range(len(radekSplit)):
            radekSpl = radekSplit[i]
            radekObsahujeId = self.detekujPritomnostSlova(radekSpl, 'id=')
            if (radekObsahujeId == True):
                vratRadek = radekSpl
                vratRadek = vratRadek.replace('>', '')
                vratRadek = vratRadek.replace('id=', '')
                vratRadek = vratRadek.replace('"', '')

        return (vratRadek)


    def vratIndexRadku(self, obsahHtml, subStr):

        indexRadku = -1

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]
            radekTrim = radek.strip()

            radekObsahujeSubString = self.detekujPritomnostSlova(radekTrim, subStr)
            if(radekObsahujeSubString == True):
                indexRadku = i
                break

        return(indexRadku)


    def vratOpravaZavorekData(self):

        opravaZavorekData = []
        oprZav = []
        oprZav.append(True)
        oprZav.append('[')
        oprZav.append('0')
        oprZav.append('15')
        oprZav.append(']')
        oprZav.append('1')
        oprZav.append('15')

        opravaZavorekData.append(oprZav)

        oprZav = []
        oprZav.append(False)
        oprZav.append('[')
        oprZav.append('0')
        oprZav.append('-35')
        oprZav.append(']')
        oprZav.append('0')
        oprZav.append('-30')

        opravaZavorekData.append(oprZav)

        return(opravaZavorekData)


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

