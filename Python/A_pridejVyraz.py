import program

obsahTabulky = []
sirkaSloupcuTabulky = []


# zatim nastavuje velikost tabulky s max 20-ti sloupci
pocetSloupcuMAX = 20

for i in range(pocetSloupcuMAX):
    obsahTabulky.append('')
    sirkaSloupcuTabulky.append(10)

 # ####################################################
 # zadani

#uplnaCesta = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\HTML\\test Jupyter\\Python-genHtml\\html-gen\\test.html'
uplnaCesta = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\HTML\\test Jupyter\\Python-genHtml\\html-gen2'

#uplnaCesta = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\HTML\\test Jupyter\\Python-genHtml\\html-gen\\priklad1.html'
#uplnaCesta = 'C:\\Users\\jonas\\OneDrive\\Dokumenty\\HTML\\test Jupyter\\Python-genHtml\\html-gen\\B_priklad1.html'

#vyska tlacitka - pokud je 0, tlacitko se neprida
buttonHeight = 0

#id tlacitka
buttonId = '1'

obsahRadku = 'Dosazením do (1) redukujeme funkci průhybu na tvar:'


#obsahTabulky[0] = '\left[4a_2^2x + 12a \left[_3^2 x^3 \left[ + \\frac{144a_4^2 x^5}{5} + 12a_2a_3 x^2 + \\right] 16a_2a_4 \\right]x^3 + 36a_3a_4x^4\\right]_0^L'


obsahTabulky[0] = 'U=\\frac{EI}{2}\int_{0}^{L}(4a_2^2 + 36a_3^2 x^2 + 144a_4^2 x^4 + 24a_2a_3 x + 48a_2a_4 x^2 + 144a_3a_4x^3)'
obsahTabulky[0] = 'w_{(x)}'
obsahTabulky[1] = ' '
obsahTabulky[2] = ' '
obsahTabulky[3] = 'a_2 x^2'
obsahTabulky[4] = '+ a_3 x^3'
obsahTabulky[5] = '+ a_4 x^4'



sirkaSloupcuTabulky[0] = 10
sirkaSloupcuTabulky[1] = 10
sirkaSloupcuTabulky[2] = 10
sirkaSloupcuTabulky[3] = 10
sirkaSloupcuTabulky[4] = 10
sirkaSloupcuTabulky[5] = 10
sirkaSloupcuTabulky[6] = 10
sirkaSloupcuTabulky[6] = 10

# ####################################################
# vykonej cast programu

program.vykonejProgram(uplnaCesta, obsahRadku, obsahTabulky, sirkaSloupcuTabulky, 'pridejVyraz', buttonHeight, buttonId)