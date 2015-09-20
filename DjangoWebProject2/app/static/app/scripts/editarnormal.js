$( document ).ready(function(){
	$('form').not(".file-form, #addMaterial").on('submit', function(event){
		
		event.preventDefault();
    });
	$(".btn.editar.toggle").click(function(){
		var form=$(this).parent("form");
		var no_hide = form.find(".no-hide");
		var hide = form.find(".hide");
		no_hide.removeClass("no-hide").addClass("hide");
		hide.removeClass("hide").addClass("no-hide");
		form.find("input").val(form.find("span.dato").text());
		form.find("textarea").val(form.find("span.dato").text());
	});
	//Realizar cambio algi asi como un submit
	$(".editar.submit").click(function(){
		var formulario = $(this).closest("form");
		var dato = $(this).parent().find('input[name=dato], textarea[name=dato], select[name=dato]');
		
		var datoValue = dato.val();
		var token = $(this).parent().find('input[name=csrfmiddlewaretoken]');
		if(dato.val()==null){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar al menos un genero', 4000);
			return null
		}else if(dato.val().trim()==''){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>El campo no puede estar vacio', 4000);
			return null
		}
		if (largoPalabra(dato.val(), formulario.attr("largomaximo"))){
			$.ajax({
				url : "/guardarDatosNormal", // the endpoint
				type : "POST", // http method
				data : { bid:$('.container.sfull').attr('id-banda'),
						dato : datoValue,
						target : formulario.attr('data-target'),
						 }, // data sent with the post request
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
						}else if(formulario.attr('data-target')=="instrumento")
							location.reload();
						var txtconbr=dato.val().replace(/(?:\r\n|\r|\n)/g, '<br />').trim();
						formulario.find(".dato").html(txtconbr.capitalizeFirstLetter());
						var no_hide = formulario.find(".no-hide");
						var hide = formulario.find(".hide");
						no_hide.removeClass("no-hide").addClass("hide");
						hide.removeClass("hide").addClass("no-hide");
					}
					else
						respuestaInstatisfactoria(response);
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
	$('.ajax-file-selection').click(function(){
		input = $(this).parent().find('input[type=file]');
		input.trigger('click'); 
	});
	$('.file-form input[type=file]').change(function(){
		readURL(this, $(this).parent().attr("preview"));
		 $(this).parent().parent().find('.fileChange').toggle();
	});
	$('.fileChange.cancel').click(function(){
		tar = $(this).parent().find('form').attr("preview");
		if(tar == "portada"){
			$("#"+tar).attr('style', "background:url("+$("#"+tar).attr('data-src')+");");
		}else{
			$("#"+tar).attr('src', $('#'+tar).attr('data-src'));
		}
		$(this).parent().find('.fileChange').toggle();
	});
	$('.ajax-file').click(function(){
		var form = $(this).parent().find('.file-form');
		var formData = new FormData(form[0]);
		console.log(form.attr('target'));
		formData.append('target',form.attr('target'));
		formData.append('bid', $('.container.sfull').attr('id-banda'));
		if(form.find('input[type=file]').val()!=''){
			$.ajax({
				url: form.attr('action'),
				type: 'POST',
				data: formData,
				cache: false,
				contentType: false,
				processData: false,
				success: function (returndata) {
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Imagen de perfíl cambiada con exito', 4000);
					form.parent().find('.fileChange').toggle();
				},
				error: function (returndata) {
					$('#preview').attr('src', $('#preview').attr('data-src'));
					Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar Imagen de perfíl', 4000);
					form.parent().find('.fileChange').toggle();
				},
			});
		}else{
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar una imagen', 4000);
		}
	})
	//fin de cambio archivo
	
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



function readURL(input, tar) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
			if(tar == "portada"){
				$("#"+tar).attr('style', "background:url("+e.target.result+");");
			}else{
				$("#"+tar).attr('src', e.target.result);
			}
        }

        reader.readAsDataURL(input.files[0]);
    }
}

function respuestaInstatisfactoria(data){
	var resp=data.split(',');
	if(resp[0]=='w')
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>'+resp[1], 4000);		
	else if(resp[0]=='e')
		Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>'+resp[1], 4000);
}
String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}