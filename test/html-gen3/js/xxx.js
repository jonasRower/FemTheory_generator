
class vykresliPole{

    constructor(){

        var polePosuny;
        var idOdstZaSkrytym;

        polePosuny = ["p1-6", "p1-7", "p1-8", "p1-9"];
        
        idOdstZaSkrytym = [
            ["p1-1", -15, 0, 0, -15],
            ["p1-2", -15,  0,  0,  -15],
            ["p1-3", -15,  0, 0, -15],
            ["p1-4", 170, 155, 155, -15],
            ["p1-5", 140, 125, 125, -15],
            ["p1-6", 110, 110, 110, -15],
            ["p1-7", 95, 80, 80, -15],
            ["p1-8", 65, 50, 50, -15],
            ["p1-9", 35, 20, 20, -15]
        ]

        this.posunyVsechnyOdstavceOdIndexu(idOdstZaSkrytym, polePosuny);

    }

    //posune vsechny odstavce pod indexem
	posunyVsechnyOdstavceOdIndexu(idOdstZaSkrytym, polePosuny){

		//console.log(idOdstZaSkrytym);

		for (let i = 0; i < idOdstZaSkrytym.length; i++) {
			var idOdstavec = idOdstZaSkrytym[i];
			this.posunOdstavec(idOdstavec, polePosuny);
		}

        console.log("ffffffffffff")

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


}


$(document).ready(function(){

	alert("ahoj");
    var script = new vykresliPole();

});