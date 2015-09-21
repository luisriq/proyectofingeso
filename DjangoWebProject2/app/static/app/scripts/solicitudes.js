$( document ).ready(function(){
	
	
	$(".togglesol").click(function(){
		var form=$(this).parent("form");
		var no_hide = form.find(".no-hide");
		var hide = form.find(".hide");
		console.log(no_hide);
		no_hide.removeClass("no-hide").addClass("hide");
		hide.removeClass("hide").addClass("no-hide");
		form.find("input").val(form.find("span.dato").text());
		form.find("textarea").val(form.find("span.dato").text());
	});
	
	$(".solicitud").click(function(){
		var formulario = $(this).closest("form");
		var olddato = $(this).parent().find('input[name=olddato]');
		var dato = $(formulario).find('input[name=dato], textarea[name=dato], select[name=dato]');
		console.log("Data: "+dato.val());
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
		console.log("formulario"+formulario.attr("data-target"));
		console.log("ArtistaID:"+formulario.attr("data-artista"));
		
		$.ajax({
			url : "/guardarDatosBanda", // the endpoint
			type : "POST", // http method
			data : { accion:$('#accion').attr('value'),
						bid:$('.container.sfull').attr('id-banda'),
						dato : datoValue,
						artista : formulario.attr("data-artista"),
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
						Materialize.toast('Solicitud enviada, espere respuesta.', 4000);
						var no_hide = formulario.find(".no-hide");
						var hide = formulario.find(".hide");
						console.log(no_hide);
						no_hide.removeClass("no-hide").addClass("hide");
						hide.removeClass("hide").addClass("no-hide");
						formulario.find("input").val(formulario.find("span.dato").text());
						formulario.find("textarea").val(formulario.find("span.dato").text());
					}
					else if(formulario.attr('data-target')=="aceptarSolicitud"){
						console.log("MEEEE");
						formulario.hide();
						if(olddato.val()=='aceptar'){
							hrefItem = formulario.find('.valign-wrapper').attr('href');
							imagen = formulario.find('.circle').attr('style');
							nombre = $(formulario.find('span')[0]).text()
							ocupacion = $(formulario.find('span')[1]).text()
							console.log(hrefItem+"\n"+imagen);
							// TODO: Cambiarlo  reusando y reemplazando con el primer integrante
							$('#integrante').append('<li class="collection-item valign-wrapper">'+
											'<a class="valign-wrapper" href="'+hrefItem+'">'+
												'<div class="circle avatar-perfil small" style="'+imagen+'" ></div>'+
												'<div class="" style="margin-left:20px;"><span >'+nombre+'</span>'+
												'<br><span class="grey-text ">'+ocupacion+'</span></div>'+
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
function largoPalabra(texto, maximo){
	var palabras = texto.split(" ");
	for (p in palabras)
		p=p.replace("\n", "");
	var g=true;
	$(palabras).each(function (index,el){
		if(el.length > parseInt(maximo))
			g=false;
	});
	return g;
}