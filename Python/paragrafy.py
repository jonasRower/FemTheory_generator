# tento modul zjistuje a uchovava data o paragrafech
# tak aby je mohl zmenit, nebo pro doplneni dalsiho

import posunTextu

class paragrafyData:

    def __init__(self, obsahHtml):

        # je potreba odstranit style, aby dokazal rozpoznat paragrafy
        posunText = posunTextu.posunText(obsahHtml, None, None, None)
        obsahHtml = posunText.getObsahHtmlBezTop()

        cislaRadkuSParag = self.vratSeznamIndexuRadkuSParagrafy(obsahHtml)
        self.posledniCisloParagrafu = self.vratPosledniCisloParagrafu(obsahHtml, cislaRadkuSParag)
        self.prvniAPosledniIndexPole = self.vratPrvniAPosledniIndexyRadku(obsahHtml, cislaRadkuSParag)
        self.posledniRadekPoslednihoBloku = self.vratPosledniIndexRadku(self.prvniAPosledniIndexPole)

        print()



    def getPosledniCisloParagrafu(self):
        return(self.posledniCisloParagrafu)

    def getPrvniAPosledniIndexPole(self):
        return(self.prvniAPosledniIndexPole)

    def getPosledniRadekPoslednihoBloku(self):
        return(self.posledniRadekPoslednihoBloku)

    def getPrvniAPosledniRadekPoslednihoBloku(self):
        return(self.prvniAPosledniIndexPole[len(self.prvniAPosledniIndexPole) - 1])



    def vratPrvniAPosledniIndexyRadku(self, obsahHtml, cislaRadkuSParag):

        prvniAPosledniIndexPole = []

        for i in range(len(cislaRadkuSParag)):
            cisloRadkuSParag = cislaRadkuSParag[i]
            prvniAPosledniIndexRadkuBloku = self.vratPrvniAPosledniIndexRadku(obsahHtml, cisloRadkuSParag)
            prvniAPosledniIndexPole.append(prvniAPosledniIndexRadkuBloku)

        return(prvniAPosledniIndexPole)


    def vratPrvniAPosledniIndexRadku(self, obsahHtml, cisloRadkuSParag):

        prvniIndexRadkuBloku = self.vratPrvniIndexRadkuBloku(obsahHtml, cisloRadkuSParag)
        #posledniIndexRadkuBloku = cisloRadkuSParag + 2
        posledniIndexRadkuBloku = self.vratPosledniIndexRadkuBloku(obsahHtml, cisloRadkuSParag+1)

        prvniAPosledniIndexRadkuBloku = []
        prvniAPosledniIndexRadkuBloku.append(prvniIndexRadkuBloku)
        prvniAPosledniIndexRadkuBloku.append(posledniIndexRadkuBloku)

        return(prvniAPosledniIndexRadkuBloku)


    def vratPosledniIndexRadkuBloku(self, obsahHtml, cisloRadkuSParag):

        posledniRadek = -1

        for i in range(len(obsahHtml)):

            i1 = cisloRadkuSParag + i
            radek = obsahHtml[i1]
            radekObsahujeHtmlEnd = self.detekujPritomnostSlova(radek, '</html>')

            if (radekObsahujeHtmlEnd == True):
                posledniRadek = i1 - 1
                break

            jednaSeOOtevrenyElement = self.detekujZdaSeJednaOOtevrenyElement(radek)

            if(jednaSeOOtevrenyElement == True):
                posledniRadek = i1 - 1
                break

        return(posledniRadek)


    def detekujZdaSeJednaOOtevrenyElement(self, radek):

        radekTrim = radek.strip()

        if(radekTrim == ''):
            jednaSeOOtevrenyElement = False
        else:
            prvniDvaznaky = radekTrim[0:2:1]

            if(prvniDvaznaky == '</'):
                jednaSeOOtevrenyElement = False
            else:
                jednaSeOOtevrenyElement = True

        return(jednaSeOOtevrenyElement)


    def vratPrvniIndexRadkuBloku(self, obsahHtml, cisloRadkuSParag):

        prvniIndexRadkuBloku = -1

        for i in range(len(obsahHtml)):
            i1 = cisloRadkuSParag - i

            if(i1 == -1):
                break

            else:
                radek = obsahHtml[i1]
                radekObsahujeClassSloupec = self.detekujPritomnostSlova(radek, '<div id="p1-')

                if (radekObsahujeClassSloupec == True):
                    prvniIndexRadkuBloku = i1
                    break

        return(prvniIndexRadkuBloku)



    def vratPosledniCisloParagrafu(self, obsahHtml, cislaRadkuSParag):

        posledniIndex = cislaRadkuSParag[len(cislaRadkuSParag)-1]
        radekPosledniIndex = obsahHtml[posledniIndex]
        posledniCisloParagrafu = radekPosledniIndex.replace('<p>(','')
        posledniCisloParagrafu = posledniCisloParagrafu.replace(')</p>', '')
        posledniCisloParagrafu = posledniCisloParagrafu.strip()

        return(posledniCisloParagrafu)


    #vrati cisla radku obsahujici napr. : "<p>(2)</p>"
    def vratSeznamIndexuRadkuSParagrafy(self, obsahHtml):

        cislaRadkuSParag = []

        for i in range(len(obsahHtml)):
            radek = obsahHtml[i]
            radekObsahujeSlovo = self.detekujZdaSeJednaORadekSCislemParagrafu(radek)
            if(radekObsahujeSlovo == True):
                cislaRadkuSParag.append(i)

        return(cislaRadkuSParag)


    def detekujZdaSeJednaORadekSCislemParagrafu(self, radek):
        radekObsahujeSlovo = self.detekujPritomnostSlova(radek, '<p>(')

        if(radekObsahujeSlovo == True):
            radekObsahujeSlovo = self.detekujPritomnostSlova(radek, ')</p>')

        return(radekObsahujeSlovo)


    def vratPosledniIndexRadku(self, prvniAPosledniIndexPole):

        prvniAPosledniRadekBloku = prvniAPosledniIndexPole[len(prvniAPosledniIndexPole) - 1]
        posledniRadekBloku = prvniAPosledniRadekBloku[1]

        return(posledniRadekBloku)


    # detekuje pritomnost substringu
    def detekujPritomnostSlova(self, radek, slovo):

        try:
            index = radek.index(slovo)
        except:
            index = -1

        if(index > -1):
            radekObsahujeSlovo = True
        else:
            radekObsahujeSlovo = False

        return(radekObsahujeSlovo)