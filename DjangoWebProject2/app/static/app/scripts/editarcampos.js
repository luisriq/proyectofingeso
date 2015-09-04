$( document ).ready(function(){
	$('form').on('submit', function(event){
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
	$(".btn.editar.submit").click(function(){
		var formulario = $(this).parent("form");
		var dato = $(this).parent().find('input[name=dato], textarea[name=dato]');
		console.log(dato.val());
		var token = $(this).parent().find('input[name=csrfmiddlewaretoken]');
		if (true){
		$.ajax({
			url : "/guardarDatosArtista", // the endpoint
			type : "POST", // http method
			data : { dato : dato.val(),
					target : formulario.attr('data-target'),
				"X-CSRFToken" : token.val() }, // data sent with the post request
			
			// handle a successful response
			success : function(response) {
				console.log(response); // log the returned json to the console
				if(response=="OK"){
					Materialize.toast('Se han guardado cambios en '+formulario.attr('data-target'), 4000);
					if(formulario.attr('data-target')=="nombre")
						$("#nombre-navbar").text(dato.val());
					else if(formulario.attr('data-target')=="cuentaTwitter"){
						$('.twitter-container').html('');
						$('.twitter-container').html('<a class="twitter-timeline" style="width:100%" href="https://twitter.com/Crunchyroll" data-widget-id="634820916141289472" data-screen-name="'+dato.val()+'"></a>');
						twttr.widgets.load()
						console.log("holi");
					}
					var txtconbr=dato.val().replace(/(?:\r\n|\r|\n)/g, '<br />');
					formulario.find(".dato").html(txtconbr);
					var no_hide = formulario.find(".no-hide");
					var hide = formulario.find(".hide");
					no_hide.removeClass("no-hide").addClass("hide");
					hide.removeClass("hide").addClass("no-hide");
					
				}
				else
					Materialize.toast('Error al cambiar : '+formulario.attr('data-target'), 4000);
			},
			// handle a non-successful response
			error : function(xhr,errmsg,err) {
				Materialize.toast('Error al cambiar : '+formulario.attr('data-target'), 4000);
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}
		});}
	});
	$('.addInstrumento').click(function(){
		$('#modal1').openModal();
	});
	
	twitLoad();
}); 

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