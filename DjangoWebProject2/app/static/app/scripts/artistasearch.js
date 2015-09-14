$( document ).ready(function(){
	$('input[name=search]').keyup(function(){
		console.log($(this).val().length);
		this_=$(this);
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
					var collectionContainer=this_.parent().parent().find('result-list');
					collectionContainer.html('');
                    for(var x in data)
                    {
                        collectionContainer.append(liGen(data[x].fields['nombre'],data[x].fields['imagenPerfil']));
                    }
                }
            });
	});
});
function imgGen(url){
	var pre='<div class="circle avatar-img-30 "><img src="';
	var pos='"></div>';
	return pre+url+pos;
}
function liGen(nombre,url){
	var tagO='<li class="collection-item valign-wrapper" >';
	var tagC='</li>';
	return tagO+imgGen(url)+nombre+tagC;
}