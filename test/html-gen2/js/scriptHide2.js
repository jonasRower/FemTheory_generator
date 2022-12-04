
class posouvejOdstavce{

	constructor(skryjOdstPole, posunZacKonPolePredchozi){

		if(skryjOdstPole != undefined){
			this.nactiPoleAPosunOdstavce(skryjOdstPole, posunZacKonPolePredchozi);
		}

	}


	getposunZacKonPole(){
		return(this.posunZacKonPole);
	}


	nactiPoleAPosunOdstavce(skryjStr, posunZacKonPolePredchozi){

		var vsechnyDivId = this.vratVsechnyIdDiv();
		var vsechnyButtonyId = this.vratVsechnyButtony(vsechnyDivId);

		var skryjStrArr= [];
		var posunZacKonPole;

		//dohleda ty posuny, ktere bude skryvat
		if(posunZacKonPolePredchozi == null){
			posunZacKonPole = this.dohledejPosunyHtml(vsechnyDivId);
			this.posunZacKonPole = posunZacKonPole;
		}
		else {
			posunZacKonPole = posunZacKonPolePredchozi;
		}
		
		//console.log(posunZacKonPole);

		if(skryjStr == 0){
			//zobrazi odstavce
			skryjStrArr.push(0);
		}
		else {
			//skryje odstavce
			skryjStrArr = skryjStr.split('+');
		}

		//console.log(skryjStrArr);
		//console.log(posunZacKonPole);
		
		for (let i = 0; i < skryjStrArr.length; i++) {
			var cisloOdstavce = skryjStrArr[i];
			posunZacKonPole = this.posunOdstavce(cisloOdstavce, posunZacKonPole, vsechnyDivId, vsechnyButtonyId);
		}

		//posune pole a zaroven vrati data pro dalsi posun
		//posunZacKonPole = this.posunOdstavce(1, posunZacKonPole, vsechnyDivId);
		//posunZacKonPole = this.posunOdstavce(2, posunZacKonPole, vsechnyDivId);
		//posunZacKonPole = this.posunOdstavce(4, posunZacKonPole, vsechnyDivId);

		//posune texty do popredi, aby oznaceny vyber neprekryval text
		var posunTextDoPopredi = new posunTextyNaZ1(posunZacKonPole)

	}


	posunOdstavce(idOdst, posunZacKonPole, vsechnyDivId, vsechnyButtonyId){

		//skryje odstavce jen kdyz je idOdst > 0
		//if(idOdst > 0){

			//skryje odstavec
			var idSkryt = "#p1-" + idOdst;
			var posunZacKonNew;
			var posun = this.vyhledejOKolikPosunout(posunZacKonPole, idOdst);
			var idOdstZaSkrytym;

			//kdyz je pozadovano aby zobrazil skryte polozky
			if(idOdst == 0){ 
				this.zobrazVsechnyOdst(posunZacKonPole);
				idOdstZaSkrytym = vsechnyDivId;
				posunZacKonNew = posunZacKonPole;
			}
			else{
				$(idSkryt).hide();
				//posune ostatni odstavce
				idOdstZaSkrytym = this.vratVsechnyIdNasledujiciZaSkyrtym(vsechnyDivId, idOdst);
				posunZacKonNew = this.vytvorPolePosunZacKon(posunZacKonPole, vsechnyDivId, posun);
			}

			//TEST:	
			//zkusit sem pridat jine tlacitko, co to udela??

			posunZacKonNew = this.opravPosunPodleTlacitek(posunZacKonNew, vsechnyButtonyId);
			//console.log(posunZacKonNew);

			/*
			posunZacKonNew[1][1] = 170;
			posunZacKonNew[1][2] = 155;
			posunZacKonNew[1][3] = 155;
			posunZacKonNew[1][4] = -15;
			*/


			//-------------------------------------------------------
			//jsou jen 4 radky

			/*
			//SKRYJE POLOZKU 1 - je tam tlacitko (3)
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",170,185,185,-15],
				["p1-3",140,140,140,-15],
				["p1-4",125,125,125,-15]
			]


			//SKRYJE POLOZKU 1 - neni tam tlacitko (3)
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",170,185,185,-15],
				["p1-3",140,125,125,-15],
				["p1-4",110,110,110,-15]
			]
			*/


			//-------------------------------------------------------
			// je zde vice radku

			//<div id="p1-4">
			// <p style="top:80px;">Dosazením do (1) redukujeme funkci průhybu na tvar:</p>
			//   <button style="top:80px; height:20px" id="skryj-2" onclick='skryj("2")'>zobraz podrobnosti</button>
			/*
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",170,185,185,-15],
				["p1-3",140,125,125,-15],
				["p1-4",110,110,110,-15],
				["p1-5",95,80,80,-15],
				["p1-6",65,50,50,-15],
				["p1-7",35,20,20,-15],
				["p1-8",5,-10,-10,-15],
				["p1-9",-25,-40,-40,-15],
			]
			*/
			//-------------------------------------------------------
			// je zde vice radku

			// <div id="p1-4">
			//  <p style="top:80px;">Dosazením do (1) redukujeme funkci průhybu na tvar:</p>
			//  <button style="top:80px; height:20px" id="skryj-1" onclick='skryj("1")'>zobraz podrobnosti</button>
			
			/*
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",170,155,155,-15],
				["p1-3",140,125,125,-15],
				["p1-4",110,110,110,-15],
				["p1-5",95,80,80,-15],
				["p1-6",65,50,50,-15],
				["p1-7",35,20,20,-15],
				["p1-8",5,-10,-10,-15],
				["p1-9",-25,-40,-40,-15],
			]
			*/

			//-------------------------------------------------------
			// zrejme chybny posun

			/*
			//SKRYJE POLOZKU 1
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",125,110,110,-15],
				["p1-3",95,95,95,-15],
				["p1-4",80,80,80,-15]
			]
			*/

			/*
			//SKRYJE POLOZKU 2 - kdyz je button na (3)
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",125,140,140,-15],
				["p1-3",95,95,95,-15],
				["p1-4",80,80,80,-15]
			]
			/*
			
			
			//SKRYJE POLOZKU 2 - kdyz neni button na (3)
			posunZacKonNew = [
				["p1-1",-15,0,0,-15],
				["p1-2",125,140,140,-15],
				["p1-3",95,80,80,-15],
				["p1-4",65,65,65,-15]
			]
			*/

            console.log("DDDDDDDDDDDDDDDDDDDDDDD");
            console.log(idOdstZaSkrytym);
            console.log(posunZacKonNew);
            console.log("DDDDDDDDDDDDDDDDDDDDDDD");

			this.posunyVsechnyOdstavceOdIndexu(idOdstZaSkrytym, posunZacKonNew, idOdst);

			//vrati data, aby mohl posunout odstavce znovu, pokud se bude volat opakovane
			return(posunZacKonNew)

		//}

	}


	//dodelavam opravu dodatecne, zde:
	opravPosunPodleTlacitek(posunZacKon, vsechnyButtonyId){

		/*
		console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
		console.log(vsechnyButtonyId);
		console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
		*/


		//opravi posuny v zavislosti na poloze tlacitek
		var posunZacKonNew = [];
		//var divIdButt = 'p1-5';
		//var divIdHide = 'p1-1';

		var divIdButt = vsechnyButtonyId[0][0];
		var divIdHide = 'p1-' + vsechnyButtonyId[0][5][0];

		//console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");
		//console.log(posunZacKon);
		//console.log(divIdButt);
		//console.log(divIdHide);
		//console.log("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX");

		var idParButt = this.vratIdPar(divIdButt);
		var idParHide = this.vratIdPar(divIdHide);

		var posunRadekNew;

		for (let i = 0; i < posunZacKon.length; i++) {

			var posunRadek = posunZacKon[i];
			var divId = posunRadek[0];
			var idPar = this.vratIdPar(divId);

			//console.log(idPar);

			if(idPar <= idParHide){
				posunRadekNew = posunRadek;
			}
			else {
				if(idPar < idParButt){	
					posunRadekNew = this.vratRadekPosunHide(posunRadek, divId);
					
				}
				if(idPar == idParButt){
					posunRadekNew = this.vratRadekPosunButtPred(posunRadek, divId);
					//console.log(posunRadekNew);
				}
				if(idPar == idParButt + 1){
					posunRadek = posunZacKonNew[posunZacKonNew.length-1];
					posunRadekNew = this.vratRadekPosunButtZa1(posunRadek, divId);
				}
				if(idPar > idParButt + 1){
					posunRadek = posunZacKonNew[posunZacKonNew.length-1];
					posunRadekNew = this.vratRadekPosunButtZa2(posunRadek, divId);
				}
			}

			posunZacKonNew.push(posunRadekNew);

		}

		//console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
		//console.log(posunZacKonNew);
		//console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA");

		return(posunZacKonNew);

	}


	vratIdPar(divId){

		var idParStr = divId.replace('p1-', '')
		var idParNum = parseInt(idParStr);

		return(idParNum);

	}


	//vrati data pro radek za skrytym radkem
	vratRadekPosunHide(posunRadekHide, divId){

		var pol2Hide = posunRadekHide[1];
		var posunHide = posunRadekHide[4];
		var posun = Math.abs(posunHide)

		var pol2 = pol2Hide;
		var pol1 = pol2-posun;
		var pol0 = pol1;

		var posunRadekNew = [];
		
		posunRadekNew.push(divId);
		posunRadekNew.push(pol2);
		posunRadekNew.push(pol1);
		posunRadekNew.push(pol0);
		posunRadekNew.push(posunHide);

		return(posunRadekNew);

	}


	//vrati data pro radek pred tlacitkem
	vratRadekPosunButtPred(posunRadekButt, divId){

		var pol2Butt = posunRadekButt[1];
		var posunButt = posunRadekButt[4];
		var posun = Math.abs(posunButt)

		var pol2 = pol2Butt;
		var pol1 = pol2;
		var pol0 = pol1;

		var posunRadekNew = [];
		
		posunRadekNew.push(divId);
		posunRadekNew.push(pol2);
		posunRadekNew.push(pol1);
		posunRadekNew.push(pol0);
		posunRadekNew.push(posunButt);

		return(posunRadekNew);

	}


	//vrati data pro radek hned za tlacitkem (1. radek)
	vratRadekPosunButtZa1(posunRadekButt, divId){

		var pol2Butt = posunRadekButt[1];
		var pol1Butt = posunRadekButt[2];
		var posunButt = posunRadekButt[4];
		var posun = Math.abs(posunButt);

		var pol2 = pol2Butt - posun;
		var pol1 = pol1Butt - 2*posun;
		var pol0 = pol1;

		var posunRadekNew = [];
		
		posunRadekNew.push(divId);
		posunRadekNew.push(pol2);
		posunRadekNew.push(pol1);
		posunRadekNew.push(pol0);
		posunRadekNew.push(posunButt);

		return(posunRadekNew);

	}


	//vrati data pro radek za tlacitkem (libovolny dalsi radek)
	vratRadekPosunButtZa2(posunRadekPrew, divId){

		var pol2Prew = posunRadekPrew[1];
		var pol1Prew = posunRadekPrew[2];
		var posunPrew = posunRadekPrew[4];
		var posun = Math.abs(posunPrew);

		var pol2 = pol2Prew - 2*posun;
		var pol1 = pol1Prew - 2*posun;
		var pol0 = pol1;

		var posunRadekNew = [];
		
		posunRadekNew.push(divId);
		posunRadekNew.push(pol2);
		posunRadekNew.push(pol1);
		posunRadekNew.push(pol0);
		posunRadekNew.push(posunPrew);

		return(posunRadekNew);


	}


	zobrazVsechnyOdst(posunZacKonPole){

		for (let i = 0; i < posunZacKonPole.length; i++) {

			var odstIdRadek = posunZacKonPole[i]
			var odstId = odstIdRadek[0]
			var idZobraz = "#" + odstId;

			$(idZobraz).show();

		}
	}


	//vrati velikost posunu o kolik bude posouvat smerem nahoru
	vyhledejOKolikPosunout(vsechnyDivId, idOdst){

		var posun = '-1';
		var idPoleExp = 'p1-' + idOdst;
		for (let i = 0; i < vsechnyDivId.length; i++) {
			var divId = vsechnyDivId[i];
			var idPole = divId[0]

			if(idPole == idPoleExp){
				posun = divId[4];
			}
		}

		return(posun);

	}


	//posune vsechny odstavce pod indexem
	posunyVsechnyOdstavceOdIndexu(idOdstZaSkrytym, polePosuny){

		//console.log(idOdstZaSkrytym);

		for (let i = 0; i < idOdstZaSkrytym.length; i++) {
			var idOdstavec = idOdstZaSkrytym[i];
			this.posunOdstavec(idOdstavec, polePosuny);
		}

	}


	//posune odstavec dle daneho indexu
	posunOdstavec(idOdst, polePosuny){

		//console.log(polePosuny);
		//console.log("polePosuny");

		var idPosunOdstTd = "#" + idOdst + " td";
		var posunyProId = this.ziskejPosunyProID(idOdst, polePosuny);

		var idPosun1 = posunyProId[0];
		var posP0 = posunyProId[1];
		var posP1 = posunyProId[2];
		var posP2 = posunyProId[3];

		//console.log(posunyProId);
		//console.log(idPosun1);

		if($(idPosunOdstTd).length){
			this.posunPolozkyOdstavceTd(idPosun1, posP0, posP1, posP2);
		}
		else{
			this.posunPolozkyOdstavceP(idPosun1, posP0, posP1, posP2);
		}

		this.posunPolozkyTlacitka(idPosun1, posP0);  //kdyz tlacitka nejsou neposune nic

	}


	vytvorPolePosunZacKon(posunZacKonPole, vsechnyDivId, posun){

		var posunZacKonPoleNewPole = [];

		if(posunZacKonPole != undefined){

			for (let i = 0; i < vsechnyDivId.length; i++) {
		
				var pol2New;
				var pol1New;
				var pol0New;
				var DivId;

				DivId = vsechnyDivId[i]

				//je nekde chyba, proto pro 0. radyek nastavuji na tvrdo
				if(i < 1){
					pol2New = posun
					pol1New = 0
					pol0New = 0
				}
				else{
					var posunZacKon = posunZacKonPole[i-1]

					var pol0 = posunZacKon[1];
					
					pol2New = pol0;
					pol1New = pol2New - posun;
					pol0New = pol1New;

				}

				var posunZacKonNew = [];

				posunZacKonNew.push(DivId);
				posunZacKonNew.push(pol2New);
				posunZacKonNew.push(pol1New);
				posunZacKonNew.push(pol0New);
				posunZacKonNew.push(posun);


				posunZacKonPoleNewPole.push(posunZacKonNew)

			}
		}

		return(posunZacKonPoleNewPole);

	}


	ziskejPosunyProID(idPosunExp, polePosuny)
	{

		var vratPosuny = [];

		for (let i = 0; i < polePosuny.length; i++) {

			var Posun = polePosuny[i]
			var id = Posun[0]

			if(id == idPosunExp){
				vratPosuny = Posun
			}

		}

		return(vratPosuny);

	}


	//posun odstavce P
	posunPolozkyOdstavceP(idPosun, posP0, posP1, posP2){

		var p0 = idPosun + ' p:eq(0)';
		var p1 = idPosun + ' p:eq(1)';
		var p2 = idPosun + ' p:eq(2)';

		p0 = '#' + p0;
		p1 = '#' + p1;
		p2 = '#' + p2;

		$(p0).css('top', posP0 + 'px');
		$(p1).css('top', posP1 + 'px');
		$(p2).css('top', posP2 + 'px');

		/*
		console.log(idPosun);
		console.log(posP0);
		
		console.log(p0);
		console.log(posP0);
		console.log('---------');
		console.log(p1);
		console.log(posP1);
		console.log('---------');
		console.log(p2);
		console.log(posP2);
		*/

	}


	//posun tlacitka
	posunPolozkyTlacitka(idPosun, posP0){

		var but = '#' + idPosun + ' button';
		$(but).css('top', posP0 + 'px');
	}


	//posun odstavce TD
	posunPolozkyOdstavceTd(idPosun, posP0, posTd, posP1)
	{
		
		var idPosunOdstTd = idPosun + ' td';
		var p0 = idPosun + ' p:eq(0)';
		var p1 = idPosun + ' p:eq(1)';

		idPosunOdstTd = '#' + idPosunOdstTd;
		p0 = '#' + p0;
		p1 = '#' + p1;

		$(idPosunOdstTd).css('top', posTd +'px');
		$(p0).css('top', posP0 + 'px');
		$(p1).css('top', posP1 + 'px');

		/*
		console.log(idPosun);
		console.log(posP0);

		
		console.log(p0);
		console.log(posP0);
		console.log('---------');
		console.log(p1);
		console.log(posP1);
		console.log('---------');
		*/

	}


	vratVsechnyIdNasledujiciZaSkyrtym(vsechnyDivId, idOdst){

		var idOdstZaSkrytym = []

		for (let i = 0; i < vsechnyDivId.length; i++) {

			var DivId = vsechnyDivId[i];
			var DivIdCisloStr = DivId.replace('p1-', '')
			var DivIdCisloInt = parseInt(DivIdCisloStr);

			if(DivIdCisloInt > idOdst){
				idOdstZaSkrytym.push(DivId);
			}

		}

		return(idOdstZaSkrytym)
	}


	vratVsechnyIdDiv(){

		var seznamIdDiv = []

		for (let i = 0; i < 1000; i++) {

			var idDiv;
			idDiv = $('div:eq(' + i + ')').attr("id");
			if(idDiv != undefined){
				let idDivExp = idDiv.substring(0, 3);
				if (idDivExp == 'p1-'){
					seznamIdDiv.push(idDiv);
				}
			}
		}

		return(seznamIdDiv)


	}


	dohledejPosunyHtml(vsechnyDivId){

		var posunZacKonPole = [];

		for (let i = 0; i < vsechnyDivId.length; i++) {

			var idOdst = vsechnyDivId[i]
			var posunZacKon = this.vratPosunyOdstavce(idOdst)

			posunZacKonPole.push(posunZacKon);

		}

		//console.log(vsechnyDivId);
		//console.log(posunZacKonPole);
		return(posunZacKonPole);

	}


	// vrati pole se vsemi buttony, vcetne jejich id
	vratVsechnyButtony(vsechnyDivId){

		var vsechnyButtonyId = [];

		for (let i = 0; i < vsechnyDivId.length; i++) {
			var divId = vsechnyDivId[i];
			var id = $('#' + divId + ' button').attr('id');
			if(id != undefined){

				var style = $('#' + divId + ' button').attr('style');
				var onclick = $('#' + divId + ' button').attr('onclick');
				var topHeightSpl = style.split('; ');
				var top = topHeightSpl[0];
				var height = topHeightSpl[1];

				var skryjStr = id.replace('skryj-', '');
				var skryjStrSpl = skryjStr['-'];

				//pokud skryjStr nelze rozdelit, pak
				if(skryjStrSpl == undefined){
					skryjStrSpl = []
					skryjStrSpl.push(skryjStr);
				}

				var buttRadek = []
				buttRadek.push(divId);
				buttRadek.push(top);
				buttRadek.push(height);
				buttRadek.push(id);
				buttRadek.push(onclick);
				buttRadek.push(skryjStrSpl);	//pole ss vsemi id radky "skryj-"

				vsechnyButtonyId.push(buttRadek);

			}
		}

		return(vsechnyButtonyId);

	}


	vratPosunyOdstavce(idOdst){

		var posunHtml1 = $("#" + idOdst + " p:eq(0)").attr("style");
		var posunHtml2 = $("#" + idOdst + " p:eq(2)").attr("style");
		
		if(posunHtml2 == undefined){
			posunHtml2 = $("#" + idOdst + " p:eq(1)").attr("style");
		}

		var posunZacKon = []
		var posunZac;
		var posunKon;
		var rozdil;

		posunZac = this.vratPosunVel(posunHtml1);
		posunKon = this.vratPosunVel(posunHtml2);
		rozdil = Math.abs(posunKon) - Math.abs(posunZac);

		//console.log(posunHtml1);


		posunZacKon.push(idOdst);
		posunZacKon.push(posunZac);
		posunZacKon.push(posunKon);
		posunZacKon.push(posunKon);
		posunZacKon.push(rozdil);

		return(posunZacKon);

	}


	vratPosunVel(posunTxt){

		var posunCislo = posunTxt.replace('top:', '')
		var posunInt = parseInt(posunCislo);

		return(posunInt);

	}

}


// aby se texty neprekryvaly s oznacenymi bunkami, posova texty nahoru
class posunTextyNaZ1{

	constructor(posunZacKonPole){
		this.nastavTextumZ1All(posunZacKonPole)
	}

	nastavTextumZ1All(posunZacKonPole){

		for (let i = 0; i < posunZacKonPole.length; i++) {
			var radekPole = posunZacKonPole[i];
			var id = radekPole[0];

			this.nastavTextuZ1(id)
		}

	}

	nastavTextuZ1(id){

		var selector = '#' + id + ' p:eq(0)';
		$(selector).css('z-index', "1");

	}

}



var posunZacKonPoleOrig;
var tlactkoStisknuto = false;
var posunZacKonPoleHtml;

// reaguje na stisknuti tlacitka
function skryj(skryjOdstPole){

	if(tlactkoStisknuto == false){

        console.log(posunZacKonPoleOrig);
		
		tlactkoStisknuto = true; //skryje odstavce
		var script = new posouvejOdstavce(skryjOdstPole, posunZacKonPoleOrig);

		//ulozi data, jako data vychozi, 
		//tak aby kdyz je bude zobrazovat nazpet, aby vedel co zobrazit
		posunZacKonPoleHtml = script.getposunZacKonPole();
        
	}
	else {
        
        console.log(posunZacKonPoleOrig);

		tlactkoStisknuto = false; //zobrazi odstavce
		
		//var script = new posouvejOdstavce(0, posunZacKonPoleHtml);
		var script = new posouvejOdstavce(0, posunZacKonPoleOrig);

        console.log(posunZacKonPoleOrig);
        
	}
	
}



class ziskejVychoziData{

    constructor(){


    }

    vratVsechnyIdDiv(){

		var seznamIdDiv = []

		for (let i = 0; i < 1000; i++) {

			var idDiv;
			idDiv = $('div:eq(' + i + ')').attr("id");
			if(idDiv != undefined){
				let idDivExp = idDiv.substring(0, 3);
				if (idDivExp == 'p1-'){
					seznamIdDiv.push(idDiv);
				}
			}
		}

		return(seznamIdDiv)

	}


    dohledejPosunyHtml(vsechnyDivId){

		var posunZacKonPole = [];

		for (let i = 0; i < vsechnyDivId.length; i++) {

			var idOdst = vsechnyDivId[i]
			var posunZacKon = this.vratPosunyOdstavce(idOdst)

			posunZacKonPole.push(posunZacKon);

		}

		console.log(vsechnyDivId);
		console.log(posunZacKonPole);
		return(posunZacKonPole);

	}


    vratPosunyOdstavce(idOdst){

		var posunHtml1 = $("#" + idOdst + " p:eq(0)").attr("style");
		var posunHtml2 = $("#" + idOdst + " p:eq(2)").attr("style");
		
		if(posunHtml2 == undefined){
			posunHtml2 = $("#" + idOdst + " p:eq(1)").attr("style");
		}

		var posunZacKon = []
		var posunZac;
		var posunKon;
		var rozdil;

		posunZac = this.vratPosunVel(posunHtml1);
		posunKon = this.vratPosunVel(posunHtml2);
		rozdil = Math.abs(posunKon) - Math.abs(posunZac);

		console.log(posunHtml1);


		posunZacKon.push(idOdst);
		posunZacKon.push(posunZac);
		posunZacKon.push(posunKon);
		posunZacKon.push(posunKon);
		posunZacKon.push(rozdil);

		return(posunZacKon);

	}


    vratPosunVel(posunTxt){

		var posunCislo = posunTxt.replace('top:', '')
		var posunInt = parseInt(posunCislo);

		return(posunInt);

	}

}



$(document).ready(function(){

	//uchovava data dulezita pro vychozi zobrazeni dat
	var vsechnyDivIdCl = new ziskejVychoziData();
	var vsechnyDivId = vsechnyDivIdCl.vratVsechnyIdDiv();
	posunZacKonPoleOrig = vsechnyDivIdCl.dohledejPosunyHtml(vsechnyDivId);

	


	//vsechnyDivIdCl.posunyVsechnyOdstavceOdIndexu(vsechnyDivId, posunZacKonPole);
	//console.log(posunZacKonPole);
	/*
	$(document).ready(function() {
            $('div p').each(function () {
                console.log($(this).attr('id'));
            });
	});
	*/

});