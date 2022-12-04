
// tento script posouvá některé elementy v závislosti na pozici elementů jiných

//rozdeli elementy podle radku a vola 'posunElementyJednohoRadku' pro kazdy element zvlast
class posunElementy {

    constructor (){


        
        // nacte vsechny elementy znaku z Html
        var vsechnyId = this.vratVsechnyIdZnaku();
        var poleExp = this.vytvorPoleExp(vsechnyId);
        var poleExpUnique = this.unique(poleExp)
        var poleIndexuExp = this.vytvorPoleIndexuDleExp(poleExpUnique, poleExp)


        for (let i = 0; i < poleExpUnique.length; i++) {
            var indexyRadek = poleIndexuExp[i];
            var IDjedenRadek = this.vratPoleIdZnakuProJedenRadek(indexyRadek, vsechnyId);
            
            var posunElementyJedneRadky = new posunElementyJednohoRadku(IDjedenRadek);
        }
        
        //console.log(poleIndexuExp);


        // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        //toto funguje NEMAZAT
        //var posunElementyJedneRadky = new posunElementyJednohoRadku();
        // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    }

    vratPoleIdZnakuProJedenRadek(indexyPole, vsechnyId){

        var IDjedenRadek = [];

        for (let i = 0; i < indexyPole.length; i++) {

            var index = indexyPole[i]
            var idZnaku = vsechnyId[index];

            IDjedenRadek.push(idZnaku)

        }

        return(IDjedenRadek);

    }


    vytvorPoleIndexuDleExp(poleExpUnique, poleExp){

        var poleIndexu = []

        for (let i = 0; i < poleExpUnique.length; i++) {

            var expUniq = poleExpUnique[i];
            var indexes = this.getAllIndexes(poleExp, expUniq);
            poleIndexu.push(indexes);
        
        }

        return(poleIndexu)

    }


    //vrati pole indexof-u vsech vyskytu 'expUniq' v poli 'poleExp'
    getAllIndexes(arr, val) {
        var indexes = [], i = -1;
        while ((i = arr.indexOf(val, i+1)) != -1){
            indexes.push(i);
        }
        return indexes;
    }


    // Id budou rozdeleny podle 'exp' , jelikoz jeden 'exp' je jeden radek (=expression)
    vytvorPoleExp(vsechnyId){

        var poleExp = []

        for (let i = 0; i < vsechnyId.length; i++) {
            var idZnaku = vsechnyId[i];
            var idZnakuPole = this.vratIdZnakuPole(idZnaku);
            var exp = idZnakuPole[1]

            poleExp.push(exp);
        }

        return(poleExp);

    }


    
    // ziska vsechny Id tridy 'class="znaky"'
    vratVsechnyIdZnaku(){

        var idArray = [];
        $('.znaky').each(function () {
            idArray.push(this.id);
        });
        
        return(idArray)

    }


    vratIdZnakuPole(idZnaku){

        var idZnakuPole1 = idZnaku.split('|');
        var text = idZnakuPole1[0]
        var expCol = idZnakuPole1[1]

        var expColSplit = expCol.split('_')
        var exp = expColSplit[0];
        var col = expColSplit[1];

        var idZnakuPole = []
        idZnakuPole.push(text);
        idZnakuPole.push(exp);
        idZnakuPole.push(col);

        return(idZnakuPole);

    }


    unique(arr) {
        var u = {}, a = [];
        for(var i = 0, l = arr.length; i < l; ++i){
            if(!u.hasOwnProperty(arr[i])) {
                a.push(arr[i]);
                u[arr[i]] = 1;
            }
        }
        return a;
    }
   

}


//posune vsechny elementy pouze jednoho radku
class posunElementyJednohoRadku {

    constructor(vsechnyId){

        //uchovava informace o posunech na kazde radce
        var posunBunkyIdTotal = undefined;

        // nacte vsechny ID ktere se tykaji znaku
        // jedna se o vsechny elementy, ktere se budou pridavat
        //var vsechnyId = this.vratVsechnyIdZnaku();

        //posouva radek, cimz udela mezery
        for (let i = 0; i < vsechnyId.length; i++) {

            // kod bezi pro dany ID zvlast
            var idZnaku = vsechnyId[i];
    
            //dopocita o kolik posunout celou radku a posune ji
            var posunCeleRadky = new dopocitejPosunyCeleRadky(idZnaku, posunBunkyIdTotal);
            posunBunkyIdTotal = posunCeleRadky.getPosunVsechBunek()
        }

        console.log(posunBunkyIdTotal);

        //posune elementy na jedne radce doprava
        if(posunBunkyIdTotal != undefined){
            this.posunElementyDoprava(posunBunkyIdTotal);
        }   

        console.log(vsechnyId);
        //-----------------------------------------------
        //zjisti kde jsou mezery a doplni znaky do mezer
        for (let i = 0; i < vsechnyId.length; i++) {

            // kod bezi pro dany ID zvlast
            var idZnaku = vsechnyId[i];
        
            // posune jen 1 znak
            var posun1Znak = new posunZnak(idZnaku)
    
        }
        
	}
    

    //ziska vsechny Id tridy 'class="znaky"'
    vratVsechnyIdZnaku(){

        var idArray = [];
        $('.znaky').each(function () {
            idArray.push(this.id);
        });
        
        return(idArray)

    }

    //posune vsechny elementy doprava
    posunElementyDoprava(posunBunkyNaRadku){

        for (let i = 0; i < posunBunkyNaRadku.length; i++) {
            var posunBunky = posunBunkyNaRadku[i];
            var id = posunBunky[0]
            var posun = posunBunky[1]

            id = '#' + id;
            $(id).css('left', posun);

        }

    }

}


//posouva dany znak na pozici
class posunZnak{

    constructor(idZnaku){

        var idZnakuPredch = this.vratIdZnakuPredch(idZnaku);

        //ziska souradnici na kterou ma posouvat
        var poziceLeftTop = this.ziskejPoziciDanehoID(idZnakuPredch);

        console.log(poziceLeftTop);
        poziceLeftTop[0] = 50;
      
        //na pozadovane souradnice posune znak
        this.posunElementNaSouradnici(idZnaku, poziceLeftTop);

        
        /*
        console.log(idZnaku);
        console.log('------- exp-2_col-1 ---------------');
        var test = this.ziskejPoziciDanehoID('[|exp-2_col-1');
        console.log('------- exp-2_col-2 ---------------');
        var test = this.ziskejPoziciDanehoID('[|exp-2_col-2');
        console.log('-------- exp-2_col-3 --------------');
        var test = this.ziskejPoziciDanehoID('[|exp-2_col-3');
        console.log('--------- exp-2_col-4 -------------');
        var test = this.ziskejPoziciDanehoID('[|exp-2_col-4');
        */

    }


    // je potreba vratit predchozi id, tak aby vlozil zavorku za toto id
    vratIdZnakuPredch(idZnaku){

        var colSplit = idZnaku.split('col-');
        var colStr = colSplit[1];
        var col = parseInt(colStr);
        var strCol = 'col-' + col;;
        
        var colPredch;

        if(col > 1){
            colPredch = col - 1;
        }
        else{
            colPredch = col;
        }

        var strColPredch = 'col-' + colPredch;
        var idZnakuNew = idZnaku.replace(strCol, strColPredch);


        return(idZnakuNew)

    }


    //jelikoz je id ve tvaru '[|exp-1_col-2' rozdeli na pole '[' a 'exp-1_col-2'
    ziskejID(idZnaku){

        var IdArr = idZnaku.split('|')
        var id = IdArr[1];

        return(id);

    }


    //ziska pozici left a top dle zadaneho Id
    ziskejPoziciDanehoID(idZnaku){

        console.log(idZnaku);

        var id = this.ziskejID(idZnaku);
        var pozicePole = [];
        var IdJquery = this.vratIdJQuery(idZnaku);
        var posunLeft = parseInt($(IdJquery).attr('posunLeft'));

        if(posunLeft > 0){
            posunLeft = posunLeft + 0;
        }
        else{
            posunLeft = 0;
        }

       
        id = '#' + id;
        if( $(id).length ) { // pokud Id existuje, pokracuje dal
            var p = $(id);
            var position = p.position();
            var leftTot = position.left - posunLeft;
            var topTot = position.top;
    
            pozicePole.push(leftTot);
            pozicePole.push(topTot);
            
            /*
            pozicePole.push(100);
            pozicePole.push(topTot);
            */

            console.log(id);
            console.log(leftTot);
            console.log(position);

        } 

        return(pozicePole);

    }



    //posune element se znakem na zadanou pozici
    posunElementNaSouradnici(idZnaku, poziceLeftTop){

        console.log(idZnaku);

        var IdJquery = this.vratIdJQuery(idZnaku)
        var left = poziceLeftTop[0];
        var top = poziceLeftTop[1];

        // posouva o neco nahoru 
        var posunTop = parseInt($(IdJquery).attr('posunTop'));
        var posunLeft = parseInt($(IdJquery).attr('posunLeft'));
        var topTot = top + posunTop;
        var leftTot = left + posunLeft;

        $(IdJquery).css('left',leftTot);
        $(IdJquery).css('top', topTot);

    }


    //vrati Id pro JQuery
    vratIdJQuery(id){

        var idJQuery = '#' + id; 
        idJQuery = idJQuery.replace('[', '\\[');
        idJQuery = idJQuery.replace(']', '\\]');
        idJQuery = idJQuery.replace('|', '\\|');

        return(idJQuery);

    }

}


class dopocitejPosunyCeleRadky{

    constructor(idZnaku, posunBunkyIdPredch){

        var idZnakuPole = this.vratIdZnakuPole(idZnaku);
        var exp = idZnakuPole[1];
        var col = idZnakuPole[2];
        var vsechnyIdNaRadku = this.ziskejVsechnyIdNaRadku(exp);

        //pokracuje dal jen v pripade ze to ma smysl, dana ID byla nalezena
        if(vsechnyIdNaRadku.length > 0){
           
            var posunLeft = this.vratPosunLeft(idZnaku);
            var posunBunkyNaRadku = this.vratPoleSPosunyBunek(vsechnyIdNaRadku, col, posunLeft);
            console.log(posunBunkyNaRadku);
            var posunBunkyId = this.vytvorPole2D(vsechnyIdNaRadku, posunBunkyNaRadku);

            this.posunBunkyIdTotal = this.sectiPosuny(posunBunkyId, posunBunkyIdPredch);

            //this.posunElementyDoprava(posunBunkyId);
            console.log(this.posunBunkyIdTotal);

        }
        else {
            
            //pokud nenajde dane ID, pak originální elementy v html skryje
            var JQueryId = this.vratIdJQuery(idZnaku);
            $(JQueryId).hide();   

        }

    }

    getPosunVsechBunek(){
        return(this.posunBunkyIdTotal);
    }

    //pokud je znaku na stejne radce vic, je potreba aby scital posuny
    sectiPosuny(posunBunkyId, posunBunkyIdPredch){

        var id;
        var posun;
        var posunPredchozi;
        var posunTot;


        if(posunBunkyIdPredch == undefined){

            var posunBunkyIdNew = posunBunkyId

        }
        else{

            var posunBunkyIdNew = []

            for (let i = 0; i < posunBunkyId.length; i++) {
                id = posunBunkyId[i][0];
                posun = posunBunkyId[i][1];
                posunPredchozi = posunBunkyIdPredch[i][1];
                posunTot = posun + posunPredchozi;

                var idPosunNew = [];
                idPosunNew.push(id);
                idPosunNew.push(posunTot);

                posunBunkyIdNew.push(idPosunNew);

            }
        }
        
        console.log(posunBunkyId);
        return(posunBunkyIdNew);

    }


    //nacte posunLeft z html
    vratPosunLeft(idZnaku){

        var IdJquery = this.vratIdJQuery(idZnaku)
        var posunLeft = parseInt($(IdJquery).attr('posunLeft'));

        return(posunLeft);

    }


    //posune vsechny elementy doprava
    posunElementyDoprava(posunBunkyNaRadku){

        for (let i = 0; i < posunBunkyNaRadku.length; i++) {
            var posunBunky = posunBunkyNaRadku[i];
            var id = posunBunky[0]
            var posun = posunBunky[1]


            id = '#' + id;
            $(id).css('left', posun);

        }

    }

    //posune element doprava, aby uvolnil misto a byl znak vyditelny
    posunElementDoPrava(id, oKolikPosunout){

        id = '#' + id;
        $(id).css('left', oKolikPosunout);

    }


    //vrati pole s posuny na radku
    //je-li totiz posunuta 1. bunka, je potreba posunout i ty ostatni
    //pole udava o kolik je kazda bunka posunuta
    vratPoleSPosunyBunek(vsechnyIdNaRadku, col, posunVpravo){

        var posunBunky = []
        
        //vychozi posun
        var posun = 0

        for (let i = 0; i < vsechnyIdNaRadku.length; i++) {

            var idBunka = vsechnyIdNaRadku[i]
            if(idBunka.includes(col) == true){
                posun = posun + posunVpravo;
            }
           
            posunBunky.push(posun);
        }

        return(posunBunky);

    }


    vratIdZnakuPole(idZnaku){

        var idZnakuPole1 = idZnaku.split('|');
        var text = idZnakuPole1[0]
        var expCol = idZnakuPole1[1]

        var expColSplit = expCol.split('_')
        var exp = expColSplit[0];
        var col = expColSplit[1];

        var idZnakuPole = []
        idZnakuPole.push(text);
        idZnakuPole.push(exp);
        idZnakuPole.push(col);

        return(idZnakuPole);

    }


    ziskejVsechnyIdNaRadku(exp){

        var idArray = [];

        $( 'td[id*=' + exp + ']' ).each(function () {
            idArray.push(this.id);
        });

        return(idArray)

    }


    vytvorPole2D(poleA, poleB){

        var pole2D = []

        for (let i = 0; i < poleA.length; i++) {
            var polozkaA = poleA[i];
            var polozkaB = poleB[i];

            var polAB = []
            polAB.push(polozkaA);
            polAB.push(polozkaB);

            pole2D.push(polAB)

        }

        return(pole2D);

    }


    //vrati Id pro JQuery
    vratIdJQuery(id){

        var idJQuery = '#' + id; 
        idJQuery = idJQuery.replace('[', '\\[');
        idJQuery = idJQuery.replace(']', '\\]');
        idJQuery = idJQuery.replace('|', '\\|');

        return(idJQuery);

    }

}



$(document).ready(function(){

    var script = new posunElementy();
    

});



