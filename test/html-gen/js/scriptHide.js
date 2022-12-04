
class posouvejOdstavce{

	constructor(skryjOdstPole, posunZacKonPolePredchozi){
		this.nactiPoleAPosunOdstavce(skryjOdstPole, posunZacKonPolePredchozi);
	}


	getposunZacKonPole(){
		return(this.posunZacKonPole);
	}


	nactiPoleAPosunOdstavce(skryjStr, posunZacKonPolePredchozi){

		var vsechnyDivId = this.vratVsechnyIdDiv();
		var skryjStrArr= [];
		var posunZacKonPole

		//dohleda ty posuny, ktere bude skryvat
		if(posunZacKonPolePredchozi == null){
			posunZacKonPole = this.dohledejPosunyHtml(vsechnyDivId);
			this.posunZacKonPole = posunZacKonPole;
		}
		else {
			posunZacKonPole = posunZacKonPolePredchozi;
		}
		
		console.log(posunZacKonPole);

		if(skryjStr == 0){
			//zobrazi odstavce
			skryjStrArr.push(0);
		}
		else {
			//skryje odstavce
			skryjStrArr = skryjStr.split('+');
		}

		console.log(skryjStrArr);
		console.log(posunZacKonPole);
		
		for (let i = 0; i < skryjStrArr.length; i++) {
			var cisloOdstavce = skryjStrArr[i];
			posunZacKonPole = this.posunOdstavce(cisloOdstavce, posunZacKonPole, vsechnyDivId);
		}

		//posune pole a zaroven vrati data pro dalsi posun
		//posunZacKonPole = this.posunOdstavce(1, posunZacKonPole, vsechnyDivId);
		//posunZacKonPole = this.posunOdstavce(2, posunZacKonPole, vsechnyDivId);
		//posunZacKonPole = this.posunOdstavce(4, posunZacKonPole, vsechnyDivId);

		//posune texty do popredi, aby oznaceny vyber neprekryval text
		var posunTextDoPopredi = new posunTextyNaZ1(posunZacKonPole)

	}


	posunOdstavce(idOdst, posunZacKonPole, vsechnyDivId){

		//skryje odstavce jen kdyz je idOdst > 0
		//if(idOdst > 0){
			
		console.log(posunZacKonPole);

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

			this.posunyVsechnyOdstavceOdIndexu(idOdstZaSkrytym, posunZacKonNew, idOdst);

			//vrati data, aby mohl posunout odstavce znovu, pokud se bude volat opakovane
			return(posunZacKonNew)

		//}

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

		console.log(idOdstZaSkrytym);

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


var tlactkoStisknuto = false;
var posunZacKonPoleHtml;

// reaguje na stisknuti tlacitka
function skryj(skryjOdstPole){

	if(tlactkoStisknuto == false){
		
		tlactkoStisknuto = true; //skryje odstavce
		var script = new posouvejOdstavce(skryjOdstPole, null);

		//ulozi data, jako data vychozi, 
		//tak aby kdyz je bude zobrazovat nazpet, aby vedel co zobrazit
		posunZacKonPoleHtml = script.getposunZacKonPole();

	}
	else {
		tlactkoStisknuto = false; //zobrazi odstavce
		var script = new posouvejOdstavce(0, posunZacKonPoleHtml);
	}
	
}


$(document).ready(function(){

});