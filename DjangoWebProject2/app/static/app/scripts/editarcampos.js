$( document ).ready(function(){
	$('form').not(".file-form").on('submit', function(event){
		console.log("entra y la wea")
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
		var formulario = $(this).parent("form");
		var olddato = $(this).parent().find('input[name=olddato]');
		console.log(olddato.val());
		var dato = $(this).parent().find('input[name=dato], textarea[name=dato], select[name=dato]');
		var datoValue = dato.val();
		if(typeof olddato === 'undefined'){
  			datoValue = dato.val().trim().capitalizeFirstLetter();
 		};
		
		var token = $(this).parent().find('input[name=csrfmiddlewaretoken]');
		console.log(dato);
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
	
	$('.addInstrumento').click(function(){
		$('#modal1').openModal();
	});
	$('input[type=range]').change(function(){
		var img = $(this).parent().parent().find(".card-image").find('img');
		var path = $(this).attr("data-img-url");
		var token = $(this).attr("data-token");
		var value=$(this).val()
		//cambiar en la bd
		$.ajax({
			url : "/guardarDatosArtista", // the endpoint
			type : "POST", // http method
			data : { dato : $(this).val(),
					idToca: $(this).attr("data-id"),
					target : 'iNivel',
				"X-CSRFToken" : token }, // data sent with the post request
			// handle a successful response
			success : function(response) {
				console.log(response); // log the returned json to the console
				if(response=="OK"){
					console.log("servidor responde OK")
					switch (value){
						case "1":
							img.attr("src",path+"1.jpg");
							break; 
						case "2":
							img.attr("src",path+"2.jpg");
							break; 
						case "3":
							img.attr("src",path+"3.jpg");
							break; 
						case "4":
							img.attr("src",path+"4.jpg");
							break; 
						case "5":
							img.attr("src",path+".gif");
							break; 
					}
				}
				else{
					Materialize.toast(' <span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar el nivel del instrumento', 4000);
					console.log("error en el servidor");
				}
			},
			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar el nivel del instrumento ', 4000);
				console.log("error en la comunicación");
			}
		});
		console.log("jakdjfsba")
	});
	//hay que hacer que sea mas elegante... meh
	$('.ajax-file-selection').click(function(){
		input = $('.file-form').find('input[type=file]');
		input.trigger('click'); 
	});
	$('.file-form input[type=file]').change(function(){
		readURL(this);
		$('.fileChange').toggle();
	});
	$('.fileChange.cancel').click(function(){
		$('#preview').attr('src', $('#preview').attr('data-src'));
		$('.fileChange').toggle();
	});
	$('.ajax-file').click(function(){
		form = $('.file-form');
		var formData = new FormData(form[0]);
		if(form.find('input[type=file]').val()!=''){
			$.ajax({
				url: form.attr('action'),
				type: 'POST',
				data: formData,
				cache: false,
				contentType: false,
				processData: false,
				success: function (returndata) {
					$('.myavatar img').attr('src',"/media/"+returndata);
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Imagen de perfíl cambiada con exito', 4000);
					$('.fileChange').toggle();
				},
				error: function (returndata) {
					$('#preview').attr('src', $('#preview').attr('data-src'));
					Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar Imagen de perfíl', 4000);
					$('.fileChange').toggle();
				},
			});
		}else{
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar una imagen', 4000);
		}
	})
	//fin de cambio archivo
	$('.del-instrumento').click(function(){
		var this_= $(this);
		var token = $(this).attr("data-token");
		$.ajax({
			url : "/guardarDatosArtista", // the endpoint
			type : "POST", // http method
			data : { dato : $(this).val(),
					idToca: $(this).attr("data-id"),
					target : 'delToca',
				"X-CSRFToken" : token }, // data sent with the post request
			// handle a successful response
			success : function(response) {
				if(response=="OK"){
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Ya no tocas ese instumento', 4000);
					this_.parent().remove();
				}
				else if(response="ERROR")
					Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al eliminar el instrumento', 4000);
			},
			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al eliminar el instrumento', 4000);
				console.log("error en la comunicación");
			}
		});
	});
	
	
	twitLoad();
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


function twitLoad(){
	window.twttr = (function(d, s, id) {
	var js, fjs = d.getElementsByTagName(s)[0],
		t = window.twttr || {};
	if (d.getElementById(id)) return t;
	js = d.createElement(s);
	js.id = id;
	js.src = "https://platform.twitter.com/widgets.js";
	fjs.parentNode.insertBefore(js, fjs);
	
	t._e = [];
	t.ready = function(f) {
		t._e.push(f);
	};
	
	return t;
	}(document, "script", "twitter-wjs"));
	
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