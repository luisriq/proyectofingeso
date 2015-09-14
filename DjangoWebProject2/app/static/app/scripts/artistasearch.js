$( document ).ready(function(){
	$('input[name=search]').keyup(function(){
		console.log($(this).val().length);
		this_=$(this);
		if($(this).val().length>3)
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
                        console.log(data[x]);
                    }
                    //cache[request.term] = users;
                }
            });
	});
});