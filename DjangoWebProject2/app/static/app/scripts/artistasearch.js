$( document ).ready(function(){
	$('input[name=search]').keyup(function(){
		var this_=$(this);
		var collectionContainer=this_.parent('div').parent('form').find('.result-list');
		collectionContainer.html('')
		console.log(this_.val()>2);
		if($(this).val().length>1)
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
					console.log(collectionContainer.length);
                    for(var x in data)
                    {
						//console.log(data[x])
                        collectionContainer.append(liGen(data[x].nombre,data[x].imagenPerfil));
                    }
                }
            });
	});
});
function imgGen(url){
	var pre='<div class="circle avatar-img-30 "><img src="/media/';
	var pos='"></div>';
	return pre+url+pos;
}
function liGen(nombre,url){
	var tagO='<li class="collection-item valign-wrapper" >';
	var tagC='</li>';
	return tagO+imgGen(url)+nombre+tagC;
}