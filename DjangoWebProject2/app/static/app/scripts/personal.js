$( document ).ready(function(){
	$('form').not(".file-form").on('submit', function(event){
		console.log("entra y la wea")
		event.preventDefault();
    });
	$(".btn.editar.toggle").click(function(){
		var form=$(this).parent("form");
		var no_hide = form.find(".no-hide");
		var hide = form.find(".hide");
		no_hide.removeClass("no-hide").addClass("hide");
		hide.removeClass("hide").addClass("no-hide");
	});
	
	//Realizar cambio algi asi como un submit
	$(".btn.editar.submit.email").click(function(){
		var formulario = $(this).parent("form");
		var dato = $(this).parent().find('input[name=dato]');
		var token =formulario.find('input[name=csrfmiddlewaretoken]');
		console.log(token.val())
		if(formulario.find('.invalid').length==0)
			$.ajax({
				url : "/guardarDatosPersonales", // the endpoint
				type : "POST", 
				data : { target : formulario.attr('data-target'),
					dato : dato.val(),
					"X-CSRFToken" : token.val()
					}, 
				success : function(resp){
					if(resp=="OK")
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Email cambiado correctamente', 4000);
					else{
						r=resp.split(',');
						console.log(r[0])
						if(r[0]=="w")
							Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>'+r[1], 4000);
						if(r[0]=="e")
							Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>'+r[1], 4000);						
					}
				},
				error : function(xhr,errmsg,err) {
					Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar el email', 4000);
					console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
				}
			});
	});
	$(".btn.editar.submit.pass").click(function(){
		var formulario = $(this).parent("form");
		var pass = $(this).parent().find('input[name=pass]');
		var oldpass = $(this).parent().find('input[name=oldpass]');
		var rpass = $(this).parent().find('input[name=repeat]');
		var token =formulario.find('input[name=csrfmiddlewaretoken]');
		console.log(pass.val()+'='+rpass.val())
		 
		if(pass.val()==rpass.val()&&pass.val()!=''){
			if(true)
				$.ajax({
					url : "/guardarDatosPersonales", // the endpoint
					type : "POST", 
					data : { target : formulario.attr('data-target'),
						olddato:oldpass.val(),
						dato : pass.val(),
						"X-CSRFToken" : token.val()
						}, 
					success : function(resp){
						if(resp=="OK")
						Materialize.toast('<span class="green-text"><i class="material-icons">&#xE5CA;</i></span>Contraseña cambiada correctamente', 4000);
						else{
							r=resp.split(',');
							console.log(r[0])
							if(r[0]=="w")
								Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span>'+r[1], 4000);
							else if(r[0]=="e")
								Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>'+r[1], 4000);
							else
								console.log(resp);					
						}
					},
					error : function(xhr,errmsg,err) {
						Materialize.toast('<span class="red-text"><i class="material-icons">&#xE14C;</i></span>Error al cambiar la contraseña', 4000);
						console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
					}
				});
			else
				Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span> Debe llenar todos los campos correctamente', 4000);
		}
		else if(pass.val()==''){
			formulario.find('input').each(function(k,el){
				if($(el).val()=='')
					$(el).addClass('invalid')
			});
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span> La contraseña no puede ser vacio', 4000);	
		}	
		else{
			pass.addClass('invalid');
			rpass.addClass('invalid');
			Materialize.toast('<span class="yellow-text"><i class="material-icons">&#xE002;</i></span> Las contraseñas no coinciden', 4000);
		}
	});
	$(".btn.editar.submit.desactivar").click(function(){
		Materialize.toast('<span class="blue-text"><i class="material-icons">&#xE869;</i></span>Lo sentimos, funcionalidad no implementada', 4000);		
	});
	
});
function asyncCambio(data_, success_){
	console.warn("enviando");
}