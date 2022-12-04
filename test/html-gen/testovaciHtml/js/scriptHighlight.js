
class vratIdDalsiBunkyProZvyrazneni {

	constructor(idVolane){

		this.zjistiIdDleReference(idVolane)
		
	}

	//tady to predelat na 'ref'
	zjistiIdDleReference(idVolane){

		this.odbarviVsechnyBunky();
		var refArr = '';

		var ref1 = $('#' + idVolane).attr('ref');
		this.zvirazniBunkuDleId(ref1);

		var refOrig = idVolane.replace(refArr, '');
		this.zvirazniBunkuDleId(refOrig);
		
	}


	vratReferencniId(col, ref){
		var refId = 'exp-' + ref + '_col-' + col;
		return(refId);
	}

	odbarviVsechnyBunky(){
		$("td").css('background-color',"white");
	}

	zvirazniBunkuDleId(id){
		$('#' + id).css("background", "#ffe0ff");
	}

	zvirazniBunkuDleColRef(col, ref){
		var refId = this.vratReferencniId(col, ref);
		$('[id^=' + refId + ']').css("background", "#ffe0ff");
	}

}


class zvyrazniBunky {

	constructor(){
		this.pohybMysiTd();
		this.pohybMysiP();
	}

	pohybMysiTd(){
		$( "td" )
		.mouseover(function() {
			var idElementu = $(this).attr("id");
			var vratId = new vratIdDalsiBunkyProZvyrazneni(idElementu)
		})
	}

	pohybMysiP(){
		$( ".s2_4" )
		.mouseover(function() {
			$("td").css('background-color',"white");
			$("button").hide();
			$("button").show();
			//$("button").css('border-width',"20px");
		})
	}

}


$(document).ready(function(){

  	var script = new zvyrazniBunky();

});