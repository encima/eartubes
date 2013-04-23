function login(){
    $("#login").fadeOut(300, function(){
        $(".login-loading").fadeIn(300, function(){
        $.ajax({
				type : 'POST',
				url : '/login/',
				dataType : 'json',
				data : {
					email: $("#login-email").val(),
					password: $("#login-password").val()
				},
				success : function(data){
				    console.log(data);
                    if(data['success'] == true){
                        window.location="/";
                    }
                    if(data['success'] == false){
                        $("#login-error").html(data['error']);
                        $("#login-error").fadeIn(400);
                        $(".login-loading").fadeOut(300, function(){
                            $("#login").fadeIn(300);   
                        });
                    }
                },
				error : function(XMLHttpRequest, textStatus, errorThrown){
					console.log("error");
				}
			});
    });
    });
}
		
		
function register(){
   $("#login").fadeOut(300, function(){
     $(".login-loading").fadeIn(300, function(){
        $.ajax({
				type : 'POST',
				url : '/register/',
				dataType : 'json',
				data : {
					email: $("#register-email").val(),
					password1: $("#register-password1").val(),
					password2: $("#register-password2").val()

				},
				success : function(data){
					if(data['success'] == true){
                        $("#registration-success").fadeIn(400);
                    }
                    if(data['success'] == false){
                        $("#registration-error").html(data['error']);
                        $("#registration-error").fadeIn(400);
                    }
                    $(".login-loading").fadeOut(300, function(){
                          $("#login").fadeIn(300);
                    });
				},
				error : function(XMLHttpRequest, textStatus, errorThrown){
					console.log("error");
				}
			});
     });
   });
}
		
$("#login").click(function(event){
		event.stopImmediatePropagation();
		login();
});
$("#register").click(function(event){
		event.stopImmediatePropagation();
		register();
});
