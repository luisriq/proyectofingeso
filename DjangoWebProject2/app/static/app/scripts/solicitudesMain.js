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
	$( "body" ).on( "click", '.solicitud', function() {
		click($(this));
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

function click(el){
		var formulario = $(el).closest("form");
		var dato = $(formulario).find('input[name=dato], textarea[name=dato], select[name=dato]');
		console.log("Data: "+dato.val());
		var datoValue = dato.val();
		var token = $(el).parent().find('input[name=csrfmiddlewaretoken]');
			
		if(dato.val()==null){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar al menos un instrumento', 4000);
			return null
		}else if(dato.val().trim()==''){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>El campo no puede estar vacio', 4000);
			return null
		}
		console.log("formulario"+formulario.attr("data-target"));
		console.log("ArtistaID:"+formulario.attr("data-artista"));
		idbanda = $('.container.sfull').attr('id-banda');
		if(typeof formulario.attr("data-banda") === 'undefined'){
			idbanda = $('.container.sfull').attr('id-banda');
		
		}else{
			idbanda = formulario.attr("data-banda");
		}
		$.ajax({
			url : "/guardarDatosBanda", // the endpoint
			type : "POST", // http method
			data : { accion:$('#accion').val(),
						bid:$(formulario).attr('data-banda'),
						dato : datoValue,
						artista : formulario.attr("data-artista"),
					target : formulario.attr('data-target'),
					
					
				}, // data sent with the post request
			// handle a successful response
			success : function(response) {
				console.log(response); // log the returned json to the console
				if(response.indexOf("OK") > -1){
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
						
						if($('#accion').val()=='aceptar'){
							var bid = formulario.find('.datos input[name=bid]').val();
							var img = formulario.find('.datos input[name=img]').val();
							var nombre = formulario.find('.datos input[name=nombre]').val();
							var ocupacion = formulario.find('.datos input[name=ocupacion]').val();
							// TODO: Cambiarlo  reusando y reemplazando con el primer integrante
							$('.bandas').append('<a href="/perfilBandaNp/'+bid+'" class="collection-item" style="padding:0px 15px">'+
													'<div class="container" style="width:100%;padding:0">'+
														'<div class="row valign-wrapper" style="margin-bottom:0;">'+
															'<div class="col s2">'+
																'<div class="circle avatar-img">'+
																	'<img src="'+img+'" style="height:50px;">'+
																'</div>'+
															'</div>'+
															'<div class="col offset-1 s5 grey-text text-darken-2 truncate" style="margin-left:10px">'+
															nombre+
															'</div>'+
															'<div class="col s4 grey-text text-darken-2 truncate">'+
															ocupacion+
															'</div>'+
														'</div>'+
													'</div>'+
												'</a>');
						}
						formulario.parent().remove();
					}
					else if(formulario.attr('data-target')=="solicitarBanda"){
						$('#modalArtista').closeModal();
						if ($('#solicitarBanda').length == 0){
							console.log("LALILULELO");
							$('#containerGeneral').append(
							'<div class="row">'+
                                '<div class="col s12 left-align">'+
                                    '<h5>Solicitantes</h5>'+
                                    '<ul id="solicitarBanda" class="collection">'+
									'</ul>'+
                               ' </div>'+
                            '</div>');
						}
						
						id = response.split(",")[1];
						$('#solicitarBanda').append(
							'<li class="collection-item valign-wrapper" >'+
                                          '<form method="POST" data-target="aceptarSolicitud" >'+
                                            
                                            '<a class="valign-wrapper" href="/perfilArtistaNp/'+formulario.attr("data-artista")+'">'+
                                            '<div class="circle avatar-perfil small" style="background: url('+"/media/"+formulario.attr("data-imagen")+'); " ></div>'+
                                            '<div class="" style="margin-left:20px;"><span >'+formulario.attr("data-nombre")+'</span>'+
                                            '<br><span class="grey-text ">'+dato.val()+'</span>'+
                                            '</div>'+
                                            '</a>'+
                                            '<input name ="dato" hidden="true" value="'+id+'"></input>'+
                                            '<input id="accion" name ="olddato" hidden="true" value="rechazar"></input>'+
                                            '<a class="btn red solicitud" onclick="document.getElementById(&quot;accion&quot;).setAttribute(&quot;value&quot;, &quot;rechazar&quot;);"   ><i class="material-icons">&#xE14C;</i></a>'+
                                        '</form>'+
                                        '</li>'
						);
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

}

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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}