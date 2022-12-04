
import paragrafy
import zamenZnaky
import posunTextu
import reference
import specialniZnak
import pridejVyraz
import aktualizujHtml


class vykonejProgram:

    def __init__(self, uplnaCesta, obsahRadku, obsahTabulky, sirkaSloupcuTabulky, akce, buttonHeight, buttonId):

        # tiskne bud 1 soubor, nebo 2 soubory, pokud je zadana pouze slozka
        adresyHtml = self.vratUplneCesty(uplnaCesta)
        self.adresyHtml = adresyHtml


        if(akce == 'aktualizujHtml'):
            if (len(adresyHtml) > 1):
                self.aktualizujHtml(adresyHtml, None)

        else:
            # cesta k tempu
            uplnaCesta = adresyHtml[0]
            self.mainProgram(uplnaCesta, obsahRadku, obsahTabulky, sirkaSloupcuTabulky, akce, buttonHeight, buttonId)


    # zde je hlavni vetveni programu
    # prakticky vsechny vstupy jsou stejne, jen uplna adresa se meni
    def mainProgram(self, uplnaCesta, obsahRadku, obsahTabulky, sirkaSloupcuTabulky, akce, buttonHeight, buttonId):

        obsahHtmlStavajici = self.nactiObsahHtml(uplnaCesta)
        par = paragrafy.paragrafyData(obsahHtmlStavajici)

        if (akce == 'pridejVyraz'):
            self.obsahtmlNew = self.pridejVyraz(obsahHtmlStavajici, obsahTabulky, sirkaSloupcuTabulky, obsahRadku, par,
                                                buttonHeight, buttonId)

        if (akce == 'precislujParagrafy'):
            self.obsahtmlNew = self.precislujParagrafy(obsahHtmlStavajici, par)

            # aby aktualizoval data je potreba precislovat a pretisknout vsechny soubory
            if (len(self.adresyHtml) > 1):

                htmlTextStavajici = self.nactiObsahHtml(self.adresyHtml[1])
                specZnakyStavajici = self.nactiObsahHtml(self.adresyHtml[2])
                aktualSpecZnaky = aktualizujHtml.aktualizaceSpecZnaky(self.obsahtmlNew, htmlTextStavajici, specZnakyStavajici)

                htmlTextTisk = aktualSpecZnaky.getObsahHtmlTextNew()
                specZnakyTisk = aktualSpecZnaky.getObsahSpecZnakyNew()

                self.tiskniHtml(htmlTextTisk, self.adresyHtml[1])
                self.tiskniHtml(specZnakyTisk, self.adresyHtml[2])


        if (akce == 'odeberPosledniVyraz'):
            self.obsahtmlNew = self.odeberPosledniVyraz(obsahHtmlStavajici, par)

        if (akce == 'posunText'):
            pounOdecti = obsahRadku
            posunVychozi = obsahTabulky
            self.obsahtmlNew = self.posunText(obsahHtmlStavajici, par, pounOdecti, posunVychozi)

        if (akce == 'pridejReference'):
            self.obsahtmlNew = self.pridejReference(obsahHtmlStavajici, par, obsahRadku, obsahTabulky)

        if (akce == 'pridejSpecZnak'):
            self.obsahtmlNew = self.pridejSpecZnak(obsahHtmlStavajici)


        # aktualizuje a tiskne data do html
        if (len(self.adresyHtml) > 1):
            self.aktualizujHtml(self.adresyHtml, self.obsahtmlNew)

        # stary kod - pokud se tiskne pouze 1 soubor
        else:
            self.tiskniHtml(self.obsahtmlNew, uplnaCesta)



    def pridejVyraz(self, obsahHtmlStavajici, obsahTabulky, sirkaSloupcuTabulky, obsahRadku, par, buttonHeight, buttonId):

        pridaniVyrazu = pridejVyraz.pridaniVyrazu(obsahHtmlStavajici, obsahTabulky, sirkaSloupcuTabulky, obsahRadku, par, buttonHeight, buttonId)
        obsahHtmlNew = pridaniVyrazu.getObsahHtmlNew()

        """
        posledniRadekPoslednihoBloku = par.getPosledniRadekPoslednihoBloku()
        posledniCisloParagrafu = par.getPosledniCisloParagrafu()
        parCislo = str(int(posledniCisloParagrafu) + 1)
        blokHtml = self.generujRadekNeboTabulku(obsahTabulky, sirkaSloupcuTabulky, obsahRadku, parCislo, buttonHeight, buttonId)

        obsahHtmlNew = self.pridejVyrazDoHtml(obsahHtmlStavajici, blokHtml, posledniRadekPoslednihoBloku + 1)

        # vola tridu pro vlozeni specialniho znaku (az ve tride detekuje, zda tam znak je ci neni)
        # pokud neni, pak nerozsiri obsahHtmlNew
        pridejZnak = specialniZnak.pridejSpecialniZnaky(obsahHtmlNew, blokHtml)
        obsahHtmlNew = pridejZnak.getObsahHtmlNew()
        """

        return(obsahHtmlNew)


    def odeberPosledniVyraz(self, obsahHtmlStavajici, par):

        prvniAPosledniIndex = par.getPrvniAPosledniRadekPoslednihoBloku()
        indexPrvni = prvniAPosledniIndex[0]
        indexPosledni = prvniAPosledniIndex[1]+1

        obsahHtmlNew = obsahHtmlStavajici.copy()
        del obsahHtmlNew[indexPrvni:indexPosledni]

        return (obsahHtmlNew)


    def precislujParagrafy(self, obsahHtmlStavajici, par):

        prvniAPosledniIndexPole = par.getPrvniAPosledniIndexPole()
        precisluj = zamenZnaky.precislovani(obsahHtmlStavajici, prvniAPosledniIndexPole, False)
        obsahHtmlPrecislovane = precisluj.getObsahHtmlPrecislovane()

        return (obsahHtmlPrecislovane)


    def posunText(self, obsahHtmlStavajici, par, pounOdecti, posunVychozi):

        prvniAPosledniIndexPole = par.getPrvniAPosledniIndexPole()
        posunText = posunTextu.posunText(obsahHtmlStavajici, prvniAPosledniIndexPole, pounOdecti, posunVychozi)
        obsahHtmlTop = posunText.getObsahHtmlTop()

        return(obsahHtmlTop)


    def pridejReference(self, obsahHtmlStavajici, par, paragVychoziCislo, refCislo):

        prvniAPosledniIndexPole = par.getPrvniAPosledniIndexPole()
        doplneneReference = reference.doplnReference(obsahHtmlStavajici, prvniAPosledniIndexPole, paragVychoziCislo, refCislo)
        obsahHtmlRef = doplneneReference.getObsahHtmlRef()

        return (obsahHtmlRef)


    def pridejSpecZnak(self, obsahHtmlStavajici):

        #zatim provizorne je to odsud
        pridejZnak = specialniZnak.pridejSpecialniZnaky(obsahHtmlStavajici)
        obsahHtmlNew = pridejZnak.getObsahHtmlNew()

        return (obsahHtmlNew)


    # aktualizuje obsahy html, mezi sebou, tak aby souhlasili
    def aktualizujHtml(self, adresyHtml, obsahtmlNew):

        cestaUplnaHtmlTemp = adresyHtml[0]
        cestaUplnaHtmlText = adresyHtml[1]
        cestaUplnaSpecZnaky = adresyHtml[2]

        if(obsahtmlNew == None):
            obsahHtmlTemp = self.nactiObsahHtml(cestaUplnaHtmlTemp)
        else:
            obsahHtmlTemp = obsahtmlNew

        obsahHtmlText = self.nactiObsahHtml(cestaUplnaHtmlText)
        obsahSpecZnaky = self.nactiObsahHtml(cestaUplnaSpecZnaky)

        aktualSpecZnaky = aktualizujHtml.aktualizaceSpecZnaky(obsahHtmlTemp, obsahHtmlText, obsahSpecZnaky)
        obsahObsahHtmlTextNew = aktualSpecZnaky.getObsahHtmlTextNew()
        obsahSpecZnakyNew = aktualSpecZnaky.getObsahSpecZnakyNew()
        obsahTemp = aktualSpecZnaky.getObsahHtmlTemp()

        # tiskne data do html
        self.tiskniHtml(obsahObsahHtmlTextNew, cestaUplnaHtmlText)
        self.tiskniHtml(obsahSpecZnakyNew, cestaUplnaSpecZnaky)
        self.tiskniHtml(obsahTemp, cestaUplnaHtmlTemp)

        print("")


    ####################################################

    def nactiObsahHtml(self, uplnaCesta):

        with open(uplnaCesta, encoding="utf8") as f:
            lines = f.readlines()

        poleNew = self.odeberZPoleNepotrebneZnaky(lines)

        return(poleNew)


    def odeberZPoleNepotrebneZnaky(self, poleOrig):

        poleNew = []

        for i in range(len(poleOrig)):
            radek = poleOrig[i]
            radekNew = radek.replace('\n', '')
            radekNew = radekNew.replace('\t', '    ')
            poleNew.append(radekNew)

        return(poleNew)


    # pokud neni zadana cesta jako uplna, tedy bez nazvu souboru, pak tiskne data do slozky
    # a nazvy souboru se nastavuji zde
    def vratUplneCesty(self, uplnaCesta):

        adresyHtml = []

        cestaMaNazevSouboru = self.detekujZdaCestaJeUplna(uplnaCesta)

        # pokud cesta nema nazev souboru, pak se generuji html s vlastnimi nazvy
        # html jsou 2
        if(cestaMaNazevSouboru == False):
            souborHtmlTemp = 'temp.html'
            souborHtmlText = 'htmlText.html'
            souborSpecZnaky = 'specZnaky.html'

            cestaUplnaHtmlTemp = uplnaCesta + '\\' + souborHtmlTemp
            cestaUplnaHtmlText = uplnaCesta + '\\' + souborHtmlText
            cestaUplnaSpecZnaky = uplnaCesta + '\\' + souborSpecZnaky

            #odmaze lomitka, pokud tam jsou navic
            cestaUplnaHtmlTemp = cestaUplnaHtmlTemp.replace('\\\\', '\\')
            cestaUplnaHtmlText = cestaUplnaHtmlText.replace('\\\\', '\\')
            cestaUplnaSpecZnaky = cestaUplnaSpecZnaky.replace('\\\\', '\\')

            adresyHtml.append(cestaUplnaHtmlTemp)
            adresyHtml.append(cestaUplnaHtmlText)
            adresyHtml.append(cestaUplnaSpecZnaky)

        # pokud neni zadana cesta jen ke slozce, tiskne se pouze dany soubor
        else:
            adresyHtml.append(uplnaCesta)

        return(adresyHtml)



    def detekujZdaCestaJeUplna(self, uplnaCesta):

        cestaSplit = uplnaCesta.split('\\')
        nazevSouboru = cestaSplit[len(cestaSplit)-1]

        cestaMaNazevSouboru = self.detekujPritomnostSlova(nazevSouboru, '.')

        return(cestaMaNazevSouboru)



    def tiskniHtml(self, dataKTisku, nazevSouboru):

        dataWrite = ""
        f = open(nazevSouboru, 'w', encoding="utf-8")

        for i in range(0, len(dataKTisku)):
            radek = dataKTisku[i]
            dataWrite = dataWrite + radek + '\n'

        f.write(dataWrite)
        f.close()

        print("")


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



