
import specialniZnak


class pridaniVyrazu:

    def __init__(self, obsahHtmlStavajici, obsahTabulky, sirkaSloupcuTabulky, obsahRadku, par, buttonHeight, buttonId):

        posledniRadekPoslednihoBloku = par.getPosledniRadekPoslednihoBloku()
        posledniCisloParagrafu = par.getPosledniCisloParagrafu()
        parCislo = str(int(posledniCisloParagrafu) + 1)
        blokHtml = self.generujRadekNeboTabulku(obsahTabulky, sirkaSloupcuTabulky, obsahRadku, parCislo, buttonHeight, buttonId)

        obsahHtmlNew = self.pridejVyrazDoHtml(obsahHtmlStavajici, blokHtml, posledniRadekPoslednihoBloku)

        # vola tridu pro vlozeni specialniho znaku (az ve tride detekuje, zda tam znak je ci neni)
        # pokud neni, pak nerozsiri obsahHtmlNew
        pridejZnak = specialniZnak.pridejSpecialniZnaky(obsahHtmlNew)
        obsahHtmlNew = pridejZnak.getObsahHtmlNew()

        self.obsahHtmlNew = obsahHtmlNew


    def getObsahHtmlNew(self):
        return (self.obsahHtmlNew)



    # slouci stavajici html s pridanymi radky ("blokHtml")
    def pridejVyrazDoHtml(self, poleA, poleB, vlozZaRadek):

        poleNew = []

        poleNew = poleA.copy()
        poleA2 = poleA.copy()

        del poleNew[vlozZaRadek:len(poleA)]
        del poleA2[0:vlozZaRadek]
        poleNew = poleNew + poleB + poleA2

        return (poleNew)

    # pokud "obsahTabulky" obsahuje pouze jednu bunku, pak generuje radek, jinak generuje tabulku
    def generujRadekNeboTabulku(self, obsahTabulky, sirkaSloupcuTabulky, obsahRadku, parCislo, buttonHeight,
                                buttonId):

        pocetSloupcu = self.zjistiPocetSloupcuTabulky(obsahTabulky)

        if (pocetSloupcu == 1):
            blokHtml = self.generujRadek(obsahRadku, obsahTabulky[0], parCislo, buttonHeight, buttonId)
        else:
            blokHtml = self.generujTabulku(obsahRadku, obsahTabulky, parCislo, pocetSloupcu, sirkaSloupcuTabulky,
                                           buttonHeight, buttonId)

        return (blokHtml)

    # generuje blok do html, ktery obsahuje popsi radku + vyraz - tabulka NENI
    def generujRadek(self, obsahRadku, vyraz, parCislo, buttonHeight, buttonId):

        blokHtml = []

        blokHtml.append('')
        blokHtml.append('\t<div id="p1-' + parCislo + '">')

        if (obsahRadku != ''):
            blokHtml.append('\t\t<p>' + obsahRadku + '</p>')

        if (buttonHeight > 0):
            blokHtml.append('\t\t<button style="height:' + str(
                buttonHeight) + 'px" id="skryj-' + buttonId + '" onclick=\'skryj("' + buttonId + '")\'>zobraz podrobnosti</button>')

        blokHtml.append('\t\t<div class="sloupce4">')
        blokHtml.append('\t\t\t<div class="s1_4">')
        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t\t<div class="s2_4">')
        blokHtml.append('\t\t\t\t<p id="exp-' + parCislo + '">')
        blokHtml.append('\t\t\t\t\t\[')
        blokHtml.append('\t\t\t\t\t\t' + vyraz)
        blokHtml.append('\t\t\t\t\t\]')
        blokHtml.append('\t\t\t\t</p>')
        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t\t<div class="s3_4">')
        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t\t\t<div class="s4_4">')
        blokHtml.append('\t\t\t\t\t<p>(' + parCislo + ')</p>')
        blokHtml.append('\t\t\t\t</div>')
        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t</div>')
        blokHtml.append('\t</div>')

        return (blokHtml)

    # generuje blok do html, ktery obsahuje popsi radku + vyraz - tabulka JE
    def generujTabulku(self, obsahRadku, obsahTabulky, parCislo, pocetSloupcu, sirkaSloupcuTabulky, buttonHeight,
                       buttonId):

        blokHtml = []

        blokHtml.append('')
        blokHtml.append('\t<div id="p1-' + parCislo + '">')

        if (obsahRadku != ''):
            blokHtml.append('\t\t<p>' + obsahRadku + '</p>')

        if (buttonHeight > 0):
            blokHtml.append('\t\t<button style="height:' + str(
                buttonHeight) + 'px" id="skryj-' + buttonId + '" onclick=\'skryj("' + buttonId + '")\'>zobraz podrobnosti</button>')

        blokHtml.append('\t\t<div class="sloupce3">')
        blokHtml.append('\t\t\t<div class="s1_3">')
        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t\t<div class="s2_3">')

        # ziska telo tabulky
        tableHtml = self.generujTableHtml(obsahTabulky, sirkaSloupcuTabulky, parCislo)
        blokHtml = blokHtml + tableHtml

        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t\t<div class="s3_3">')
        blokHtml.append('\t\t\t\t<p>(' + parCislo + ')</p>')
        blokHtml.append('\t\t\t</div>')
        blokHtml.append('\t\t</div>')
        blokHtml.append('\t</div>')
        blokHtml.append('')

        return (blokHtml)

    def generujTableHtml(self, obsahTabulky, sirkaSloupcuTabulky, parCislo):

        pocetSloupcu = self.zjistiPocetSloupcuTabulky(obsahTabulky)

        obsahTabulkyHtml = []
        obsahTabulkyHtml.append('\t\t\t<table>')
        obsahTabulkyHtml.append('\t\t\t\t<tr>')

        for i in range(pocetSloupcu):
            obsahSloupce = obsahTabulky[i]
            sirkaSloupce = str(sirkaSloupcuTabulky[i])
            indexSloupce = str(i + 1)

            radek = '\t\t\t\t\t<td style="width:' + sirkaSloupce + 'px" id="exp-' + parCislo + '_col-' + indexSloupce + '">'
            obsahTabulkyHtml.append(radek)
            obsahTabulkyHtml.append('\t\t\t\t\t\t\[')
            obsahTabulkyHtml.append('\t\t\t\t\t\t\t' + obsahSloupce)
            obsahTabulkyHtml.append('\t\t\t\t\t\t\]')
            obsahTabulkyHtml.append('\t\t\t\t\t</td>')

        obsahTabulkyHtml.append('\t\t\t\t</tr>')
        obsahTabulkyHtml.append('\t\t\t</table>')

        return (obsahTabulkyHtml)

    # ackoli je delka pole obsahTabulky = pocetSloupcuMAX,
    # je potreba zjistit posledni zaplneny index,
    # jelikoz ten urcuje pocet sloupcu v html
    def zjistiPocetSloupcuTabulky(self, obsahTabulky):

        pocetSloupcu = -1

        for i in range(len(obsahTabulky)):
            i1 = len(obsahTabulky) - i - 1
            obsahSloupce = obsahTabulky[i1]

            if (obsahSloupce != ''):
                pocetSloupcu = i1 + 1
                break

        return (pocetSloupcu)