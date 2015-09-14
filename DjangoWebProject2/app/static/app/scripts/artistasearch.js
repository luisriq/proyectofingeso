$( document ).ready(function(){
	$('input[name=search]').keyup(function(){
		var this_=$(this);
		var collectionContainer=this_.parent('div').parent('form').find('.result-list');
		collectionContainer.html('')
		if($(this).val().length>1){
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
                        collectionContainer.append(liGen(data[x].nombre,data[x].imagenPerfil,""));
                    }
                }
            });
		}
	});
	$('form').submit(function(event){
		event.preventDefault();
	});
});
function imgGen(url){
	var pre='<div class="circle avatar-img-30"><img src="/media/';
	var pos='"></div>';
	return pre+url+pos;
}
function liGen(nombre,url,onclick){
	var tagO='<li class="collection-item valign-wrapper" onclick="'+onclick+'" >';
	var tagC='</li>';
	return tagO+imgGen(url)+nombre+tagC;
}