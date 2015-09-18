$( document ).ready(function(){
	$(".solicitud").click(function(){
		var formulario = $(this).closest("form");
		var olddato = $(this).parent().find('input[name=olddato]');
		console.log(formulario.find('input[name=olddato]').val());
		var dato = $(this).parent().find('input[name=dato], textarea[name=dato], select[name=dato]');
		console.log(dato.val());
		var datoValue = dato.val();
		if(typeof olddato === 'undefined'){
  			datoValue = dato.val().trim().capitalizeFirstLetter();
 		};
		
		var token = $(this).parent().find('input[name=csrfmiddlewaretoken]');

		if(dato.val()==null){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar al menos un instrumento', 4000);
			return null
		}else if(dato.val().trim()==''){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>El campo no puede estar vacio', 4000);
			return null
		}
		$.ajax({
			url : "/guardarDatosBanda", // the endpoint
			type : "POST", // http method
			data : { accion:$('#accion').attr('value'),
						bid:$('.container.sfull').attr('id-banda'),
						dato : datoValue,
					target : formulario.attr('data-target'),
				"X-CSRFToken" : token.val() }, // data sent with the post request
			// handle a successful response
			success : function(response) {
				console.log(response); // log the returned json to the console
				if(response=="OK"){
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Se han guardado cambios en '+formulario.attr('data-target'), 4000);
					if(formulario.attr('data-target')=="solicitar"){
						//TODO: Cambiar html 
						$('#botonSolicitar').replaceWith('<a class="col hover-shadow s5 offset-s2 card-panel color-principal white-text disabled" style="padding:10px">Solicitado</a>');
					}
					else if(formulario.attr('data-target')=="aceptarSolicitud"){
						console.log("MEEEE");
						formulario.hide();
						if(olddato.val()=='aceptar'){
							hrefItem = formulario.find('.valign-wrapper').attr('href');
							imagen = formulario.find('.circle').attr('style');
							nombre = formulario.find('span').text()
							console.log(hrefItem+"\n"+imagen);
							// TODO: Cambiarlo  reusando y reemplazando con el primer integrante
							$('#integrante').append('<li class="collection-item valign-wrapper">'+
											'<a class="valign-wrapper" href="'+hrefItem+'">'+
												'<div class="circle avatar-perfil small" style="'+imagen+'" ></div>'+
												'<div class="" style="margin-left:20px;"><span >'+nombre+'</span>'+
												'<br><span class="grey-text ">S</span></div>'+
											'</a>'+
										'</li>');
						}
					}
				}
				else
					Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar : '+formulario.attr('data-target'), 4000);
			},
			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar : '+formulario.attr('data-target'), 4000);
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}
		});
	});
	//hay que hacer que sea mas elegante... meh
	
	for(var i=1;i<20;i++)
		setTimeout(function(){
			if($('iframe').width()>$('iframe').parent().width()){
				var pw=$('iframe').parent().width(); 
				$('iframe').width(pw);
				$('iframe').parent('div').resize(function (){
					if($('iframe').width() != $('iframe').parent().width()){
						$('iframe').width($(this).width());
					}
				})
					
			}
		}, i*500);//arrgla problemas de visualizacion en ipad
}); 
