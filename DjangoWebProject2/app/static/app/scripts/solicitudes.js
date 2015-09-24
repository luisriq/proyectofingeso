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
$('.solicitud').click(function(){Onclick(this)});
var Onclick= function (este){
		var formulario = $(este).closest("form");
		console.log("formulario "+formulario.html())
		console.log("formulario "+$(este).html())
		var olddato = formulario.find('input[name=olddato]');
		var dato = $(formulario).find('input[name=dato], textarea[name=dato], select[name=dato]');
		console.log("Data: "+dato.val());
		var datoValue = dato.val();
		if(typeof olddato === 'undefined'){
  			datoValue = dato.val().trim().capitalizeFirstLetter();
 		};
		
		var token = $(este).parent().find('input[name=csrfmiddlewaretoken]');
			
		if(dato.val()==null){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>NULL', 4000);
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
			data : { accion:$('#accion').attr('value'),
						bid:$('.container.sfull').attr('id-banda'),
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
						//Materialize.toast('Solicitud enviada, espere respuesta.', 4000);
						var no_hide = formulario.find(".no-hide");
						var hide = formulario.find(".hide");
						console.log(no_hide);
						no_hide.removeClass("no-hide").addClass("hide");
						hide.removeClass("hide").addClass("no-hide");
						formulario.find("input").val(formulario.find("span.dato").text());
						formulario.find("textarea").val(formulario.find("span.dato").text());
					}
					else if(formulario.attr('data-target')=="aceptarSolicitud"){
						console.log( olddato.val());
						if(olddato.val()=='aceptar'){
							hrefItem = formulario.find('.valign-wrapper').attr('href');
							imagen = formulario.find('.circle').attr('style');
							nombre = $(formulario.find('span')[0]).text()
							ocupacion = $(formulario.find('span')[1]).text()
							// TODO: Cambiarlo  reusando y reemplazando con el primer integrante
							var id = hrefItem.split('/')[hrefItem.split('/').length-1];
							console.log(id);
							var str = '<li class="collection-item valign-wrapper">'+
											'<a class="valign-wrapper" href="'+hrefItem+'">'+
												'<div class="circle avatar-perfil small" style="'+imagen+'" ></div>'+
												'<div class="" style="margin-left:20px;"><span >'+nombre+'</span>'+
												'<br><span class="grey-text ">'+ocupacion+'</span></div>'+
											'</a>'+
											' <a class="btn grey darken-1 tooltipped"  data-tooltip="Opciones" data-position="right" onclick="intOpciones('+id+')" style="padding:0 8px"><i class="material-icons">&#xE8B8;</i></a>'+
										'</li>';
							console.log($('#integrante li:last'));
							$('#integrante li:last').before(str);
							
						}
						var cont = formulario.parent().parent();
						formulario.parent().remove();
						if(cont.find('li').length==0){
							cont.parent().remove();
						}
					}
					else if(formulario.attr('data-target')=="solicitarBanda"){
						$('#modalArtista').closeModal();
						
						if ($('#solicitarBanda').length == 0){
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
							'<li class="collection-item valign-wrapper new-append" >'+
                                          '<form method="POST" class="valign-wrapper" data-target="aceptarSolicitud" style="width:100%">'+
                                            
                                            '<a class="valign-wrapper" href="/perfilArtistaNp/'+formulario.attr("data-artista")+'" style="width:calc(100% - 40px)">'+
                                            '<div class="circle avatar-perfil small" style="background: url('+"/media/"+formulario.attr("data-imagen")+'); " ></div>'+
                                            '<div class="" style="margin-left:20px;"><span >'+formulario.attr("data-nombre")+'</span>'+
                                            '<br><span class="grey-text ">'+dato.val()+'</span>'+
                                            '</div>'+
                                            '</a>'+
                                            '<div class="inline"><a class="btn red solicitud" onclick="document.getElementById(&quot;accion&quot;).setAttribute(&quot;value&quot;, &quot;rechazar&quot;);" style="padding:0 8px"><i class="material-icons">&#xE14C;</i></a></div>'+											
                                            '<input name ="dato" hidden="true" value="'+id+'"></input>'+
                                            '<input id="accion" name ="olddato" hidden="true" value="rechazar"></input>'+
                                        '</form>'+
                                        '</li>'
						);
						$('.new-append form .inline .solicitud').click(function(){Onclick(this)});
						$('.new-append').removeClass('new-append');
						dato.val('');
						olddato.val('');
						formulario.find('input[name=search]').val('');
					}
				}else{
					respuestaInstatisfactoria(response);
					 	if(response.split(',')[0]=="k"){
							if(formulario.attr('data-target')=="seguir"){
								$(formulario).attr("data-target", "dejardeseguir");
								$(este).text("Dejar de seguir");
								jol = parseInt($("#segnum").text())+1;
								$("#segnum").text(jol+'');
								console.log("j-"+jol);
							}else if(formulario.attr('data-target')=="dejardeseguir"){
								$(formulario).attr("data-target", "seguir");
								$(este).text("Seguir");
								jol = parseInt($("#segnum").text())-1;
								$("#segnum").text(jol+'');
								console.log("j+"+jol);
							}
						}
					}
				},
			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar : '+formulario.attr('data-target'), 4000);
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}
		});

};

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
function respuestaInstatisfactoria(data){
	var resp=data.split(',');
	if(resp[0]=='w')
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>'+resp[1], 4000);	
	else if(resp[0]=="k")
		Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>'+resp[1], 4000);
	else if(resp[0]=='e')
		Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>'+resp[1], 4000);
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