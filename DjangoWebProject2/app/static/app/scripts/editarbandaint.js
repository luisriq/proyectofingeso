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
		if(dato.val()==null){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar al menos un genero', 4000);
			return null
		}else if(dato.val().trim()==''){
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>El campo no puede estar vacio', 4000);
			return null
		}
		if (largoPalabra(dato.val(), formulario.attr("largomaximo"))){
			$.ajax({
				url : "/guardarDatosBanda", // the endpoint
				type : "POST", // http method
				data : { bid:$('.container.sfull').attr('id-banda'),
						dato : datoValue,
						target : formulario.attr('data-target')
						}, // data sent with the post request
				// handle a successful response
				success : function(response) {
					console.log(response); // log the returned json to the console
					if(response=="OK"){
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Se han guardado cambios en '+formulario.attr('data-target'), 4000);
						if(formulario.attr('data-target')=="nombre"){
							$("#nombre-navbar").text(dato.val().capitalizeFirstLetter());
						}
						else if(formulario.attr('data-target')=="retirarse"){
							window.location="/perfilArtista";
						}
						else if(formulario.attr('data-target')=="cuentaTwitter"){
							$('.twitter-container').html('');
							$('.twitter-container').html('<a class="twitter-timeline" style="width:100%" href="https://twitter.com/Crunchyroll" data-widget-id="634820916141289472" data-screen-name="'+dato.val()+'"></a>');
							twttr.widgets.load()
							console.log("holi");
						} 
						var txtconbr=dato.val().replace(/(?:\r\n|\r|\n)/g, '<br />').trim();
						formulario.find(".dato").html(txtconbr.capitalizeFirstLetter());
						var no_hide = formulario.find(".no-hide");
						var hide = formulario.find(".hide");
						if(formulario.attr('data-target')=="genero"){
							var opttxt = dato.children("option").filter(":selected").text();
							formulario.find(".dato").html(opttxt);
						}
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
	$('form#addMaterial').on('submit', function(event){
		event.preventDefault();
		var icon=$(this).find('input[name=icon]');
		var color=$(this).find('input[name=color]');
		var enlace=$(this).find('input[name=enlace]');
		var desc=$(this).find('input[name=desc]');
		var nombre=$(this).find('input[name=nombre]');
		var bid=$('.container.sfull').attr('id-banda');
		var token=$(this).find('input[name=csrfmiddlewaretoken]');
		var correcto=true;
		if(icon.val().trim()==''){
			correcto=false;
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar un icono', 4000);			
		}
		
		if(color.val().trim()==''){
			correcto=false;
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes seleccionar un color', 4000);			
		}
		if(enlace.val().trim()==''){
			correcto=false;
			enlace.addClass('invalid')
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes ingresar un enlace', 4000);			
		}
		if(nombre.val().trim()==''){
			correcto=false;
			nombre.addClass('invalid')
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes ingresar un Nombre', 4000);			
		}
		if(desc.val().trim()==''){
			correcto=false;
			desc.addClass('invalid')
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>Debes escribir una descripcion', 4000);			
		}
		if(enlace.val().indexOf("http") == -1){
			console.warn("formato no corresponde a enlace procediendo a corregir...");
			enlace.val('http://'+enlace.val());
		}
			
		if(correcto)
			$.ajax({
				url: $(this).attr('action'),
				type: 'POST',
				data: {
					bid:bid,
					tipo:icon.val(),
					nombre:nombre.val().capitalizeFirstLetter(),
					color:color.val(),
					enlace:enlace.val(),
					descripcion:desc.val().capitalizeFirstLetter(),
					"X-CSRFToken" : token.val()
				},
				success: function (data) {
					var id = data.split(',');
					if(id[0]=="k"){
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Material agregado', 4000);
						var m = materialgen(id[1],icon.val(),nombre.val(),color.val(),enlace.val(),desc.val());
						console.log(m);
						$(m).insertBefore( ".add-material" );
						$('.no-hay-material').remove();
						$('#modalMaterial').closeModal();
					}
					else{
						var resp=data.split(',');
						if(resp[0]=='w')
							Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>'+resp[1], 4000);		
						else if(resp[0]=='e')
							Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>'+resp[1], 4000);		
					}
					
				},
				error: function (data) {
					Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error de conección', 4000);
				},
			});
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
	 $('.cabezaSelect').click(function(e) {
			var cabezaSelect=$(this);
           $('.selector').show();
			$('.selector li').click(function(e) {
              var clase=$(this).find('i').text();
				$(cabezaSelect).html('<i class=\"material-icons\">'+clase+'</i>')
				$('.inIcon').val(clase);
				$('.selector').hide();
           });
		   
        });
       //color selector 
      $('.color-selector .trigger').click(function(){
          var piker =   $(this).prevAll('.piker');
          if(piker.hasClass('hide'))
            piker.removeClass('hide');
          else
            piker.addClass('hide');
      });
      $('.color-selector .piker .color').click(function(){
          var color=$(this).attr('data-option');
          var trigger = $(this).parent('.piker').nextAll('.trigger');
          trigger.attr('class','trigger white-text inline')
          trigger.addClass(color);
          var input = $(this).parent('.piker').prevAll('input');
          input.val(color);
          $(this).parent('.piker').addClass('hide');
      });
}); 
function materialgen(id,tipo,nombre,color,enlace,descripcion){
	var litagO='<li id="mat'+id+'" class="collection-item manito">';
	var remtag='<span class="right white red-text text-darken-2 valign-wrapper tooltipped" data-position="right" data-tooltip="quitar material" style="height:46px" onclick="removeMaterial('+id+')"><i class="material-icons">remove_circle</i></span>'
	var atagO='<a class="valign-wrapper tooltipped" href="'+enlace+'" data-tooltip="ir al enlace" target="_blank">';
	var icon ='<div class="inline" style="margin:0"><i class="material-icons '+color+' white-text " style="padding:8px;">'+tipo+'</i></div>';
	var letras ='<div class="inline">'+nombre.capitalizeFirstLetter()+'<br><span class="truncate grey-text stext">'+descripcion.capitalizeFirstLetter()+'</span></div>'
    var atagC = '</a>';
    var litagC = '</li>';
	return litagO+remtag+atagO+icon+letras+atagC+litagC;
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
function removeMaterial(mId,confirmado){
	if(confirmado){
		$('.rem-confirm').remove();
		bid= $('.container.sfull').attr('id-banda');
		console.log(bid);
		
		$.ajax({
			url: "/guardarDatosBanda",
			type: 'POST',
			data: {
				bid:bid,
				target:'material-delete',
				dato:mId,
				"X-CSRFToken" : $('input[name=csrfmiddlewaretoken]').val()
			},
			success: function (data) {
				if(data=='OK'){
					$('#mat'+mId).remove()
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Material removido con exito', 4000);				
				}else
					respuestaInstatisfactoria(data);
			},
			error: function (data) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al quitar el material', 4000);
			},
		});
	}else{
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>¿Estás seguro que deseas quitar el material?<a style="margin-left:10px;" href="#" onclick="removeMaterial('+mId+',true);"><b>SI</b></a>', 10000,"rem-confirm");
	}
}


function dejarBanda(uId,confirmado){
	
	if(confirmado){
		$('.rem-confirm').remove();
		bid= $('.container.sfull').attr('id-banda');
		console.log(bid);
		$.ajax({
			url: "/guardarDatosBanda",
			type: 'POST',
			data: {
				bid:bid,
				target:'retirarse',
				dato:uId,
			},
			success: function (data) {
				if(data=='OK'){
					window.location="/perfilArtista";
				}else
					respuestaInstatisfactoria(data);
			},
			error: function (data) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Erro al intentar dejar la banda', 4000);
			},
		});
	}else{
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>¿Estás seguro que deseas abandonar esta banda?<a style="margin-left:10px;" href="#" onclick="dejarBanda('+uId+',true);"><b>SI</b></a>', 10000,"rem-confirm");
	}
}

function expulsar(uId,confirmado){
	
	if(confirmado){
		$('.rem-confirm').remove();
		bid= $('.container.sfull').attr('id-banda');
		console.log(bid);
		$.ajax({
			url: "/guardarDatosBanda",
			type: 'POST',
			data: {
				bid:bid,
				target:'retirarse',
				dato:uId,
			},
			success: function (data) {
				if(data=='OK'){
					//window.location="/perfilArtista";
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Artista expulsado', 4000);
					//remover el usuario de la cosa de los usarios
					$('#int'+uId).remove();
				}else
					respuestaInstatisfactoria(data);
			},
			error: function (data) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Erro al intentar dejar la banda', 4000);
			},
		});
	}else{
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>¿Estás seguro que deseas expulsar al usuario?<a style="margin-left:10px;" href="#" onclick="expulsar('+uId+',true);"><b>SI</b></a>', 10000,"rem-confirm");
	}
}

function removeDisco(dId,confirmado){
	
	$('#modalDisco').closeModal();
	if(confirmado){
		$('.rem-confirm').remove();
		bid= $('.container.sfull').attr('id-banda');
		console.log(bid);
		$.ajax({
			url: "/guardarDatosBanda",
			type: 'POST',
			data: {
				bid:bid,
				target:'disco-delete',
				dato:dId,
			},
			success: function (data) {
				if(data=='OK'){
					$('#dis'+dId).remove()
					Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Material removido con exito', 4000);				
				}else
					respuestaInstatisfactoria(data);
			},
			error: function (data) {
				Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al quitar el material', 4000);
			},
		});
	}else{
		Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>¿Estás seguro que deseas quitar el material?<a style="margin-left:10px;" href="#" onclick="removeDisco('+dId+',true);"><b>SI</b></a>', 10000,"rem-confirm");
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