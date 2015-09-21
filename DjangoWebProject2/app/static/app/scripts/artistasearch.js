$( document ).ready(function(){
	$('input[name=search]').keyup(function(){
		
		$(".result-list").removeClass("hide");
		var this_=$(this);
		var collectionContainer=$(".result-list");
		collectionContainer.html('')
		if($(this).val().length>=0){
			collectionContainer.width(this_.width());
			$.ajax({
                dataType : 'json',
                method : 'POST',
                url : '/search',
                data : {
                    q : this_.val(),
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
                },
                success : function(data) {
                    var users = [];
                    for(var x in data)
                    {
						//console.log(data[x])
                        collectionContainer.append(liGen(data[x].nombre,data[x].imagenPerfil, data[x].id,"artistaSelect($(this));"));
                    }
                }
            });
		}
	});
	$('form').submit(function(event){
		event.preventDefault();
	});
	
	$(document).click(function() {
		$(".result-list").addClass("hide");
	});
	$('input[name=search]').click(function(e) {
		$(".result-list").removeClass("hide");
		e.stopPropagation(); // This is the preferred method.

	});
	
	
});
function artistaSelect(artista){
	console.log(artista);
	console.log("Nombre:" + artista.attr("data-nombre"));
	console.log("imagen:" + artista.attr("data-imagen"));
	console.log("id:" + artista.attr("data-id"));
	$("#seleccionado").html(artista.clone());
	$(artista).closest("form").attr("data-artista", artista.attr("data-id") )
	console.log($(artista).closest("form"));
}

function imgGen(url){
	var pre='<div class="circle avatar-img-30"><img src="/media/';
	var pos='"></div>';
	return pre+url+pos;
}
function liGen(nombre,url, id,onclick){
	var tagO='<a data-nombre="'+nombre+'" data-imagen="'+url+'" data-id="'+id+'" class="collection-item valign-wrapper resultado" onclick="'+onclick+'" >';
	var tagC='</a>';
	return tagO+imgGen(url)+nombre+tagC;
}