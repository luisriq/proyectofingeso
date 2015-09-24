$( document ).ready(function(){
	
}); 

function seguir(id, aid){
	$.ajax({
			url : "/guardarDatosArtista", // the endpoint
			type : "POST", // http method
			data : { dato : id,
						artista : aid,
						target : 'seguir',
				},
				success : function(response) {
					if(response.indexOf("k,") > -1){
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>'+response.slice(1).slice(1), 4000);
						$('.seguir').toggle();
						jol = parseInt($("#segnum").text())+1;
						$("#segnum").text(jol+'');
						console.log("j+"+jol);
					}else{
						respuestaInstatisfactoria(response);
					}
				}
	});
}
function dejardeseguir(id, aid){
	$.ajax({
			url : "/guardarDatosArtista", // the endpoint
			type : "POST", // http method
			data : { dato : id,
						artista : aid,
						target : 'dejardeseguir',
				},
				success : function(response) {
					console.log(response);
					if(response.indexOf("k,") > -1){
						//Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Haz dejado de seguir al artista', 4000);
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>'+response.slice(1).slice(1), 4000);
						$('.seguir').toggle();
						jol = parseInt($("#segnum").text())-1;
						$("#segnum").text(jol+'');
						console.log("j-"+jol);
					}else{
						respuestaInstatisfactoria(response);
					}
				}
	});
}


function respuestaInstatisfactoria(data){
	var resp=data.split(',');
	if(resp[0]=='w')
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>'+resp[1], 4000);
	else if(resp[0]=="k")
		Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>'+resp[1], 4000);		
	else if(resp[0]=='e')
		Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>'+resp[1], 4000);
}
String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}