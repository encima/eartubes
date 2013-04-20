function login(){


$.ajax({
				type : 'POST',
				url : '/login/',
				dataType : 'json',
				data : {
					email: $("#login-email").val(),
					password: $("#login-password").val()
				},
				success : function(data){
					$("#content").html(data);
					$("#loading").fadeOut(200, function(){
						$("#content").fadeIn(600, function(){});
					});
					
					$("html, body").animate({ scrollTop: 0 }, "fast");
					//analytics();
					reloadEffects();
				},
				error : function(XMLHttpRequest, textStatus, errorThrown){
					timer = setTimeout(function(){loadPage(requestedPage)}, 5000);
					console.log("error");
				}
			});
		}
		
		
function register(){
$.ajax({
				type : 'POST',
				url : '/login/',
				dataType : 'json',
				data : {
					email: $("#register-email").val(),
					password1: $("#register-password1").val()
					password2: $("#register-password2").val()

				},
				success : function(data){
					
				},
				error : function(XMLHttpRequest, textStatus, errorThrown){
					timer = setTimeout(function(){loadPage(requestedPage)}, 5000);
					console.log("error");
				}
			});
		}
		
$("#Login").click(function(event){
		event.stopImmediatePropagation();
		login();
$("#register").click(function(event){
		event.stopImmediatePropagation();
		register();