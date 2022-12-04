# porovna html pred a po precislovani
# aby opravil prislusne reference

import copy

# meni jak cisla paragrafu, tak i cisla v "id-ckach"
class porovnejObsahHtmlPredAPo:

    # vymazat nadbytecne reference !!
    # jinak v tom bude binec

    def __init__(self, htmlPred, htmlPo):

        seznamIndexuOdlisnychRadku = self.vratIndexyOdlisnychRadku(htmlPred, htmlPo)
        seznamIndexuOdlisnychRadku = self.rozsirIndexyORozdilneRadky(seznamIndexuOdlisnychRadku, htmlPred)
        seznamIndexuOdlisnychRadku = self.rozsirIndexyORozdilneRadky(seznamIndexuOdlisnychRadku, htmlPo)

        refPuvodni = self.vratRefKVyhledani(seznamIndexuOdlisnychRadku, 1)
        refNove = self.vratRefKVyhledani(seznamIndexuOdlisnychRadku, 2)
        indexyRadkuRef = self.vratSeznamIndexuRadkuSRef(htmlPo, refPuvodni)

        self.htmlNew = self.nahradPuvRef(htmlPo, indexyRadkuRef, refPuvodni, refNove)



    def getHtmlNew(self):
        return(self.htmlNew)


    def nahradPuvRef(self, htmlPo, indexyRadkuRef, refPuvodniPole, refNovePole):

        htmlNew = copy.deepcopy(htmlPo)

        for i in range(len(indexyRadkuRef)):
            indexRadku = indexyRadkuRef[i]
            radek = htmlPo[indexRadku]
            refPuvodni = refPuvodniPole[i]
            refNovy = refNovePole[i]

            radekNew = radek.replace(refPuvodni, refNovy)
            htmlNew[indexRadku] = radekNew

        return(htmlNew)


    def vratSeznamIndexuRadkuSRef(self, htmlPo, refPuvodni):

        indexyRadkuRef = []

        for i in range(len(htmlPo)):
            radek = htmlPo[i]
            for i1 in range(len(refPuvodni)):
                ref = refPuvodni[i1]
                radekObsahujeRef = self.detekujPritomnostSlova(radek, ref)
                if(radekObsahujeRef == True):
                    indexyRadkuRef.append(i)

        return(indexyRadkuRef)


    def vratIndexyOdlisnychRadku(self, htmlPred, htmlPo):

        seznamIndexuOdlisnychRadku = []

        for i in range(len(htmlPred)):
            radekPred = htmlPred[i]
            radekPo = htmlPo[i]

            if(radekPred != radekPo):
                indexyRadku = []  # pole o dimenzi 1 - aby se mohli pridavat sloupce
                indexyRadku.append(i)
                seznamIndexuOdlisnychRadku.append(indexyRadku)

        return(seznamIndexuOdlisnychRadku)


    def rozsirIndexyORozdilneRadky(self, seznamIndexuOdlisnychRadku, obsahHtml):

        seznamIndexuOdlisnychRadkuNew = []

        for i in range(len(seznamIndexuOdlisnychRadku)):
            indexRadkuArr = seznamIndexuOdlisnychRadku[i]
            indexRadku = indexRadkuArr[0]
            rozdilnyRadek = obsahHtml[indexRadku]
            indexRadkuArr.append(rozdilnyRadek)
            seznamIndexuOdlisnychRadkuNew.append(indexRadkuArr)

        return(seznamIndexuOdlisnychRadkuNew)


    def vratRefKVyhledani(self, seznamIndexuOdlisnychRadku, index):

        refKVyhledani = []

        for i in range(len(seznamIndexuOdlisnychRadku)):
            radekPuvodni = seznamIndexuOdlisnychRadku[i][index]
            jednaSeOTd = self.detekujPritomnostSlova(radekPuvodni, 'td')
            if(jednaSeOTd == True):
                radekId = self.ziskejIdZRadku(radekPuvodni)
                radekRef = radekId.replace('id', 'ref')
                refKVyhledani.append(radekRef)

        return(refKVyhledani)



    def ziskejIdZRadku(self, radek):

        idSplit = radek.split(' ')
        radekId = ''

        for i in range(len(idSplit)):
            radekSlit = idSplit[i]
            radekObsahujeId = self.detekujPritomnostSlova(radekSlit, 'id=')
            if(radekObsahujeId == True):
                radekId = radekSlit
                break

        return(radekId)



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


