$( document ).ready(function(){
	$('form').not(".file-form").on('submit', function(event){
		
		event.preventDefault();
    });
	$(".btn.editar.toggle").click(function(){
		var form=$(this).parent("form");
		var no_hide = form.find(".no-hide");
		var hide = form.find(".hide");
		console.log(no_hide);
		no_hide.removeClass("no-hide").addClass("hide");
		hide.removeClass("hide").addClass("no-hide");
	});
	//Realizar cambio algi asi como un submit
	$(".editar.submit").click(function(){
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
		
		console.log("func:"+largoPalabra(dato.val(), formulario.attr("largomaximo")));
		if (largoPalabra(dato.val(), formulario.attr("largomaximo"))){
			console.log("que mierda")
			
			
			$.ajax({
				url : "/guardarDatosArtista", // the endpoint
				type : "POST", // http method
				data : { olddato: olddato.val(),
						 dato : datoValue,
						target : formulario.attr('data-target'),
					"X-CSRFToken" : token.val() }, // data sent with the post request
				// handle a successful response
				success : function(response) {
					console.log(response); // log the returned json to the console
					if(response=="OK"){
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Se han guardado cambios en '+formulario.attr('data-target'), 4000);
						if(formulario.attr('data-target')=="nombre"){
							$("#nombre-navbar").text(dato.val().capitalizeFirstLetter());
						}
						else if(formulario.attr('data-target')=="cuentaTwitter"){
							$('.twitter-container').html('');
							$('.twitter-container').html('<a class="twitter-timeline" style="width:100%" href="https://twitter.com/Crunchyroll" data-widget-id="634820916141289472" data-screen-name="'+dato.val()+'"></a>');
							twttr.widgets.load()
							console.log("holi");
						}else if(formulario.attr('data-target')=="solicitar"){
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
								$('#integrante').append('<li class="collection-item valign-wrapper">'+
												'<a class="valign-wrapper" href="'+hrefItem+'">'+
													'<div class="circle avatar-perfil small" style="'+imagen+'" ></div>'+
													'<div class="" style="margin-left:20px;"><span >'+nombre+'</span>'+
													'<br><span class="grey-text ">S</span></div>'+
												'</a>'+
											'</li>');
							}
							
							
						}
						else if(formulario.attr('data-target')=="instrumento")
							location.reload();
						var txtconbr=dato.val().replace(/(?:\r\n|\r|\n)/g, '<br />').trim();
						formulario.find(".dato").html(txtconbr.capitalizeFirstLetter());
						var no_hide = formulario.find(".no-hide");
						var hide = formulario.find(".hide");
						no_hide.removeClass("no-hide").addClass("hide");
						hide.removeClass("hide").addClass("no-hide");
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
		else
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Las palabras no pueden superar '+formulario.attr("largomaximo")+' caracteres', 4000);
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


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
			$('#preview').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}
String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}