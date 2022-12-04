# aby mohl obarvovat bunky pri najeti mysi, je potreba doplnit referenec

import posunTextu
import zamenZnaky

class doplnReference:

    def __init__(self, obsahHtml, prvniAPosledniIndexPole, paragVychoziCislo, refCislo):

        radkyPodleParag = posunTextu.posunText(obsahHtml, prvniAPosledniIndexPole, None, None)
        radkyPodleParagRozdel = radkyPodleParag.getRadkyPodleParagRozdel()


        # pokud vychozi cislo neni, pak jen vraci cisla jiz zapsanych referenci
        # to je potreba zjistit, pokud precislovava reference
        if(paragVychoziCislo == None):
            self.refCisloPodleParagRozdel = self.vratCislaJizZapsanychReferenci(radkyPodleParagRozdel, obsahHtml)

        else:
            ziskejSkutecneCislovani = zamenZnaky.precislovani(obsahHtml, prvniAPosledniIndexPole, True)
            skutecnaCislaParag = ziskejSkutecneCislovani.getSkutecnaCislaParag()

            self.vratCislaJizZapsanychReferenci(radkyPodleParagRozdel, obsahHtml)
            self.obsahHtmlRef = self.doplnRefKRadkumTd(radkyPodleParagRozdel, skutecnaCislaParag, obsahHtml, paragVychoziCislo, refCislo)

        print("")


    def getObsahHtmlRef(self):
        return(self.obsahHtmlRef)

    def getRefCisloPodleParagRozdel(self):
        return(self.refCisloPodleParagRozdel)


    def vratCislaJizZapsanychReferenci(self, radkyPodleParagRozdel, obsahHtml):

        refCisloPodleParagRozdel = []

        for i in range(len(radkyPodleParagRozdel)):
            radkyPodleParag = radkyPodleParagRozdel[i]
            refCisloPodleParag = []

            for i1 in range(len(radkyPodleParag)):
                cisloRadkuARefCislo = []
                radek = radkyPodleParag[i1]
                pNeboTd = radek[1]
                refCislo = ''
                cisloRadku = radek[0]

                if(pNeboTd == 'td'):
                    radekHtml = obsahHtml[cisloRadku]
                    refCislo = self.odeberReferenciZRadku(radekHtml, True)

                cisloRadkuARefCislo.append(cisloRadku)
                cisloRadkuARefCislo.append(refCislo)
                refCisloPodleParag.append(cisloRadkuARefCislo)

            refCisloPodleParagRozdel.append(refCisloPodleParag)

        return(refCisloPodleParagRozdel)



    #jelikoz by metoda pro ziskani ref, byla podobna pouzivam netodou stejnou
    def odeberReferenciZRadku(self, radekOrig, vratCisloRef):

        uvozSplit = radekOrig.split('"')
        if(vratCisloRef == True):
            radekNew = ''
        else:
            radekNew = radekOrig


        for i in range(len(uvozSplit)):
            uvozRadek = uvozSplit[i]
            uvozRadekObsahujeRef = self.detekujPritomnostSlova(uvozRadek, 'ref-')
            if(uvozRadekObsahujeRef == True):
                radekRef = uvozRadek
                indRef = self.vratIndexSlova(radekRef, '_ref-')
                refCislo = radekRef[indRef:len(radekRef):1]

                if (vratCisloRef == True):
                    radekNew = refCislo.replace('_ref-', '')
                else:
                    radekBezRef = radekRef.replace(refCislo, '')
                    radekNew = radekOrig.replace(radekRef, radekBezRef)

        return(radekNew)


    def doplnRefKRadkumTd(self, radkyPodleParagRozdel, skutecnaCislaParag, obsahHtml, paragVychoziCislo, refCislo):

        radkyPodleParagSkut = self.vratRadkyDleSkutParag(radkyPodleParagRozdel, skutecnaCislaParag, paragVychoziCislo)
        obsahHtmlRef = obsahHtml.copy()

        for i in range(len(radkyPodleParagSkut)):
            radekParag = radkyPodleParagSkut[i]
            if(radekParag[1] == 'td'):
                cisloRadku = radekParag[0]
                radek = obsahHtml[cisloRadku]

                #nejdriv odebere stavajici referenci
                radekBezRef = self.odeberReferenciZRadku(radek, False)

                if(refCislo > -1):
                    refNew = self.ziskejRef(radekBezRef, refCislo)
                    radekRefNew = radekBezRef.replace('>', '') + ' ' + refNew

                    # opravi radek
                    obsahHtmlRef[cisloRadku] = radekRefNew

                else:
                    # opravi radek - jako radek bez reference
                    obsahHtmlRef[cisloRadku] = radekBezRef


        return(obsahHtmlRef)


    def ziskejRef(self, radekBezRef, refCislo):

        id = self.ziskejId(radekBezRef)
        radekBezId = id.replace('id="', '')
        radekSpl = radekBezId.split('_')
        expOrig = radekSpl[0]

        expNew = 'exp-' + str(refCislo)
        idNew = id.replace(expOrig, expNew)
        refNew = idNew.replace('id', 'ref')

        return(refNew)



    def ziskejId(self, radekBezRef):

        radekBezRefSplit = radekBezRef.split(' ')
        vratRadek = ''

        for i in range(len(radekBezRefSplit)):
            radekSpl = radekBezRefSplit[i]
            detekujZdaObsahujeId = self.detekujPritomnostSlova(radekSpl, 'id=')

            if(detekujZdaObsahujeId == True):
                vratRadek = radekSpl
                break

        return(vratRadek)


    """
    # dodatecnou referenci se mysli napr: '_ref-6-3+5' -> tedy vraci -3+5
    def ziskejDodatRef(self, radek, radekBezRef):

        dodatRef = ''

        radekBezRef1 = radekBezRef.replace('">', '')
        ref = radek.replace(radekBezRef1, '')
        ref1 = ref.replace('_ref-', '')
        ref1 = ref1.replace('">', '')
        refSplit = ref1.split('-')

        if(len(refSplit) == 2):
            dodatRef = refSplit[1]

        return(dodatRef)
    """

    def vratRadkyDleSkutParag(self, radkyPodleParagRozdel, skutecnaCislaParag, skutParagExp):

        indSkut = skutecnaCislaParag.index(str(skutParagExp))
        radkyPodleParagSkut = radkyPodleParagRozdel[indSkut]

        return(radkyPodleParagSkut)

    """
    def doplnReferenciDoRadku(self, radekOrig, refCislo, dodatRef):

        expRadek = ''
        refString = '_ref-' + str(refCislo)
        refString = refString + '-' + dodatRef
        uvozSplit = radekOrig.split('"')


        for i in range(len(uvozSplit)):
            uvozRadek = uvozSplit[i]
            uvozRadekObsahujeExp = self.detekujPritomnostSlova(uvozRadek, 'exp-')

            if(uvozRadekObsahujeExp == True):
                expRadek = uvozRadek
                break

        expRadek2 = expRadek + refString
        radekNew = radekOrig.replace(expRadek, expRadek2)
        #radekNew = radekNew + dodatRef


        return(radekNew)
    """


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

        return (index)


