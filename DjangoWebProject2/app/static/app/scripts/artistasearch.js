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
		collectionContainer.html('');
		if($(this).val().length>=2){
			collectionContainer.width(this_.parent().width());
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
                        collectionContainer.append(uniGen(data[x].imagen,data[x].url, data[x].nombre,data[x].tipo));
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
	
	console.log(artista);
	console.log("Nombre:" + artista.attr("data-nombre"));
	console.log("imagen:" + artista.attr("data-imagen"));
	console.log("id:" + artista.attr("data-id"));
	console.log("/perfilArtistaNp/" +artista.attr("data-id") );
	$("#seleccionado").html(artista.clone());
	$(artista).closest("form").attr("data-artista", artista.attr("data-id") );
	$(artista).closest("form").attr("data-imagen", artista.attr("data-imagen") );
	$(artista).closest("form").attr("data-nombre", artista.attr("data-nombre") );
	console.log($(artista).closest("form"));
}

function universalselect(todo){
	/*console.log(artista);
	console.log("Nombre:" + todo.attr("data-nombre"));
	console.log("imagen:" + todo.attr("data-imagen"));
	console.log("id:" + todo.attr("data-id"));
	console.log("/perfilArtistaNp/" +todo.attr("data-id") );*/
	//window.location = todo.attr("href");
	//$("#seleccionado").html(artista.clone());
	//console.log($(artista).closest("form"));
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

function uniGen(imagen, url, nombre, tipo){
	img = '<div class="circle avatar-img-30 inline"><img src="'+imagen+'"></div>';
	icon = '';
	if(tipo == "artista")
		icon='<i class="material-icons inline" style="width:25px;font-size:20px;" >person</i>';
	else
		icon ='<i class="material-icons inline" style="width:25px;font-size:20px;" >group</i>';
	a = '<a href="'+url+'" class="collection-item resultado" >'+img+'<div class="inline ">'+icon+'<span class="grey-text text-darken-2" style="font-size:18px;">'+nombre+'</span></div></a>';
	console.log("AAAA "+a);
	return a;
}