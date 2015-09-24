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
					bid:$('.container.sfull').attr('id-banda'),
					q : this_.val(),
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
                },
                success : function(data) {
                    var users = [];
                    for(var x in data)
                    {
						//console.log(data[x])
                        collectionContainer.append(liGen(this_.val(),data[x].nombre,data[x].imagenPerfil, data[x].id,"artistaSelect($(this));"));
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
	
	$('input[name=universalsearch]').keyup(function(){
		
		$(".result-list").removeClass("hide");
		var this_=$(this);
		var collectionContainer=$(".result-list");
		collectionContainer.html('')
		if($(this).val().length>=0){
			collectionContainer.width(this_.width());
			$.ajax({
                dataType : 'json',
                method : 'POST',
                url : '/universalsearch',
                data : {
					bid:$('.container.sfull').attr('id-banda'),
					q : this_.val(),
                    csrfmiddlewaretoken : $('input[name=csrfmiddlewaretoken]').val()
                },
                success : function(data) {
                    var users = [];
                    for(var x in data)
                    {
						//console.log(data[x])
                        collectionContainer.append(liGen(this_.val(),data[x].nombre,data[x].imagenPerfil, data[x].id,"artistaSelect($(this));"));
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
	console.log("/perfilArtistaNp/"+artista.attr("data-id"));
	
}

function imgGen(url){
	var pre='<div class="circle avatar-img-30"><img src="/media/';
	var pos='"></div>';
	return pre+url+pos;
}
function liGen(busc, nombre,url, id,onclick){ 
	var tagO='<a data-nombre="'+nombre+'" data-imagen="'+url+'" data-id="'+id+'"class="collection-item valign-wrapper resultado" onclick="'+onclick+'" >';
	var tagC='</a>';
	console.log(nombre.indexOf(busc));
	var icon='';
	if(nombre.toLowerCase().indexOf(busc.toLowerCase()) != -1)
		icon='<i class="material-icons">face</i>';
		
	else
		icon ='<i class="material-icons">&#xE41C;</i>';
	return tagO+imgGen(url)+icon+nombre+tagC;
}