/*
* GLOBAL STUFF
*/

// Animate the login logo
$("#logout img").mouseenter(function(){
   $(this).stop().animate({opacity:'0.6'}, 300);
});
$("#logout img").mouseleave(function(){
   $(this).stop().animate({opacity:'0.3'}, 300);
});


/*
* LOGIN PAGE STUFF
*/

// Called when user clicks login button on login page
// AJAX request to /login made, posting email and password.
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
		
// Called when user clicks register button on login page
// AJAX request to /register made, posting email, password and password confirm.	
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
	
// Button listeners for logging in and registering:	
$("#login").click(function(event){
		event.stopImmediatePropagation();
		login();
});
$("#register").click(function(event){
		event.stopImmediatePropagation();
		register();
});

/*
* DASHBOARD STUFF
*/

// Boolean to represent whether or not an AJAX request is in progress to get the
// movie list from the search box (to prevent query-flooding):
var requesting = false;

// Method to update the query information
// Called from a selection of movie from movie list (from the movie search) or by
// selecting a Last.fm query method.
// Sets a loading gif as the poster until the request comes back.
function showQuery(queryTitle){
     $("#query-title").html(queryTitle);
    $("#query-poster").html('<img src="/static/media/login-loading.gif" style="width:100%;height:40px;"/>');
    var winHeight = $(window).height();
    $("#movie_name_results").css({'display':'none'});
    $("#query").slideDown(400);
    loadListeners();
}

// After changes to the DOM, reload event listeners to ensure the page
// still responds correctly
function loadListeners(){
    // Listen for key events on search field. If search string > 2, then submit an AJAX
    // request for movies of this name to appear in the movie list.
    $("#movie_name").keyup(function(event){
        event.stopImmediatePropagation();
        var request = $("#movie_name").val();
        if(request.length == 0){
            $("#query").slideDown(300);
            $("#query-lastfm").slideDown(300);
            $("#movie_name").val('');
            $("#movie_name_results").stop().animate({opacity:'0.0'},300);
        }
        // If no request currently going on, then make request based on search term.
        if(request.length > 2 && requesting == false){
            $("#query").slideUp(300);
            $("#query-lastfm").slideUp(300);
            getMovieListFromSearch(request);
        }
    });
    // Listen for clicks on movie in list.  If clicked, update query and submit
    // AJAX request to retrieve results based on this movie.
    $("#movie_name_results li").click(function(event){
        event.stopImmediatePropagation();
        $("#query-poster").html("");
        $("#query").stop().slideDown(300);
        $("#query-lastfm").stop().slideDown(300);
        var movieName = $(this).attr("rel");
        var movieID = $(this).attr("id");
        var movieYear = $(this).attr("class");
        $("#movie_name").val(movieName)
        $("#movie_name_results").html('');
        $("#movie_name_results").stop().animate({opacity: '0.0'}, 400);
        showQuery("Movies with soundtracks similar to <strong>"+movieName+"</strong>");
        getResultsFromMovie(movieID, movieYear);
    });
    // Listen for clicks on hearted tracks Last.fm button.
    $("#hearted-tracks").click(function(event){
        event.stopImmediatePropagation();
        showQuery("Movies with soundtracks based off your Last.fm <strong>hearted tracks</strong>");
        getResultsFromLastfmHearted();
    });
    // Listen for clicks on hearted tracks Last.fm button.
    $("#recent-tracks").click(function(event){
        event.stopImmediatePropagation();
        showQuery("Movies with soundtracks based off your Last.fm <strong>recent tracks</strong>");
        getResultsFromLastfmRecent();
    });
    // Hover effects on Last.fm buttons:
    $(".lastfm-button").mouseenter(function(){
       $(this).css({'background-image':'url("/static/media/lastfm-button-red.png")', 'background-color': 'rgba(0,0,0,0.05)'});
    });
    $(".lastfm-button").mouseleave(function(){
        $(this).css({'background-image':'url("/static/media/lastfm-button.png")', 'background-color':' rgba(0,0,0,0.3)'});
    });
}

// TODO: AJAX request to get movies based from Last.fm hearted tracks
function getResultsFromLastfmHearted(){

}

// TODO: AJAX request to get movies based from Last.fm recent tracks
function getResultsFromLastfmRecent(){

}

// Get movies based on movie selected in movie list (from search)
// AJAX request made to api/imdb to get further information on query movie and an
// array of result movies. #movie-results is populated with the result movies
// and #query is updated with more information on the query movie.
function getResultsFromMovie(id, year){   
    $("#movie-results").slideUp(300, function(){
        $("#movie-results").html('');
    });
    $.ajax({
        type : 'POST',
        url : '/api/imdb',
        dataType : 'json',
        data : {
            q: id
        },
        success : function(data){
            $("#movie-results").html('');
            console.log(data);
            // If results are available (data[0] is the query movie)
            if(data.length > 1){
                $("#welcome").slideUp(600);
                for(var i = 0; i < data[1].length; i++){
                    console.log(data[1][i]['title']+": "+data[1][i]['poster']);
                    stuff = '<div class="movie"><div class="poster">';
                    // If poster exists:
                    if(data[1][i]['poster'] != null){
                        stuff = stuff + '<img src="'+data[1][i]['poster']+'" />';
                    }
                    // If no poster exists for this movie, load default image:
                    else{
                        stuff = stuff + '<img src="/static/media/movie_default.gif" style="opacity:0.6; width:170px;" />';
                    }
                    stuff = stuff + '</div><div class="info"><p>';
                    stuff = stuff + data[1][i]['title']+'</p><p>';
                    stuff = stuff + data[1][i]['year']+'</p></p>';
                    stuff = stuff + '</i></p></div><div class="clear"></div></div>';
                    // Append this movie to #movie-results:
                    $("#movie-results").append(stuff);
                }
                $("#movie-results").slideDown(300);
            }
            
            // Update the query movie information.
            $("#query-poster").slideUp(200, function(){
                posterHTML = "";
                // If poster exists, load this:
                if(data[0][0]['poster'] != null){
                    posterHTML = posterHTML + '<img src="'+data[0][0]['poster']+'" />'
                }
                // Else get an error ready:
                else{
                    posterHTML = '<p class="error">Sorry, we couldn\'t find an image for this movie.</p>';
                }
                // If no results from query, get error ready:
                if(data.length < 2){
                    posterHTML = posterHTML + '<p class="error">Sorry, we couldn\'t find any movies similar to this one by soundtrack</p>';
                }
                // Set #query-poster with appropriate information and make it visible:
                $("#query-poster").html(posterHTML);
                $("#query-poster").slideDown(300);
            });
            // Reload event listeners:
            loadListeners();
        },
        error : function(XMLHttpRequest, textStatus, errorThrown){
            // If error, then display an error message:
            $("#query-poster").html( '<p class="error">Sorry, we couldn\'t get any details on this movie</p>');
        }
    });
}

// Get list of movies from search box. Called only if length of search string > 2.
// AJAX request made to /api/ps and posted the query string as 'q'.
// Function populates result list of movies which can be clicked upon to query that movie.
function getMovieListFromSearch(name){
    requesting = true;
    $.ajax({
        type : 'POST',
        url : '/api/ps',
        dataType : 'json',
        data : {
            q: name
        },
        success : function(data){
            $("#movie_name_results").html('');
            if($("#movie_name").val().length <=2){
                $("#movie_name_results").stop().animate({opacity: '0.0'},300);   
                requesting = false;
                return;
            }
            $("#movie_name_results").css({'display':'block'});
            $("#movie_name_results").stop().animate({opacity: '1.0'},400);
            
            // Iterate through each result and append to list. Maintain information
            // on movie name, if, and year.
            for(var i = 0; i < data.length; i++){
                var item = "";
                item = '<li id="'+data[i]['id']+'" rel="'+data[i]['title']+'">'+data[i]['title']
                if(data[i]['year'] != "-1"){
                    item = item + ' ('+data[i]['year']+')'
                }
                item = item + '</li>';
                $("#movie_name_results").append(item);
                if(i > 200){i = data.length;}
                loadListeners();
            }
            requesting = false;
        },
        error : function(XMLHttpRequest, textStatus, errorThrown){
            requesting = false;
        }
    });

}

// Initial load of listeners
$(document).ready(function(){
    loadListeners();
});