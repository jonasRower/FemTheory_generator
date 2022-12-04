
// script pridava obdelnik, cimz zakryva nepotrebne znaky 
// jelikoz neni mozno zapsat zavorku zvlast bez obsahu, Latex to nedovoluje
// Abych zobrazil zavorku zvlast, musim ostatni znaky zakryt

class pridejObdelnik {

	constructor (){
	
		this.pridejVsechnyObdelniky();
		this.pridejObdelnik(40, 55, 236, 18);
	
	}


	pridejObdelnik(width, height, top, left){

		console.log(width);

		var appendStr = '<div ' +
						'style="width:' + width + 'px;' + 
						'		height:' + height + 'px;' + 
						'		top:' + top + 'px;' + 
						'		left:' + left + 'px;' + 
						'background-color:rgb(255,0,255);' + 
						'" class="prekryrti">' + 
						'</div>';

		console.log(appendStr);
						
		//$("body").append('<div style="width:500px;height:100px;top:20px;left:20px;background-color:rgb(255,0,255);"></div>')
		$("body").append(appendStr);

	}


	pridejVsechnyObdelniky(idArray){

		idArray = this.vratVsechnyIdZnaku();

		for (let i = 0; i < idArray.length; i++) {

			var id = idArray[i];
			id = id.replace('|', '\\|');
			id = id.replace('[', '\\[');
			id = id.replace(']', '\\]');

			var p = $('#' + id);
			var position = p.position();
			var leftTot = position.left;
			var topTot = position.top;

			console.log(leftTot);
			console.log(topTot);

		}

	}


	// ziska vsechny Id tridy 'class="znaky"'
	vratVsechnyIdZnaku(){

		var idArray = [];
		$('.znaky').each(function () {
			idArray.push(this.id);
		});
		
		return(idArray)

    }

}
      
      

$(document).ready(function(){

	var obd = new pridejObdelnik();

});