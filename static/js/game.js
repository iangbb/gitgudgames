let reviewNo = 0;
let commentNo = [];
var noMoreReviews = 0;

// Called when page is loaded
$(document).ready(function() {

// Create 'get reviews' button and define functions
$('.get-reviews').click(function() {
    const authenticated = ($(this).attr("data-authenticated") == 'true'); // Is user logged in?
    const gameid = $(this).attr("data-gameid"); // Get the game's unique ID
	// AJAX request to get reviews
    $.getJSON('/ajax/get_reviews/', {
        game: gameid,
        start: reviewNo,
    }, function(data, textStatus, jqXHR) {
        reviewNo = reviewNo + 3; // Track what the start index of the next 3 reviews it
        noMoreReviews = data['number'] - 3; // Track how many more reviews are left to get
        $('.get-reviews').html('Get more reviews (' + noMoreReviews + ')');
        const parser = new DOMParser();
		
		// For each review returned by AJAX, generate the HTML
        for (i = 0; i < data.reviews.length; i++) {
            commentNo[data.reviews[i].id] = 0;
            var className = "jumbotron"
            var journalString = "";
			
			// If the poster is a journalist, then highlight their review
            if (data.reviews[i].is_journalist) {
                journalString = "[ This is a journalist review ]"
                className = "jumbotron journalist-review"
            }
			
            const domString = '<div class="' + className +'">\
                                <h5> ' + journalString + ' </h5>\
                              <div class="row">\
                                  <div class="col">\
                                      <a href="../../../profile/' + data.reviews[i].username + '"><h3 class="gameName">' + data.reviews[i].poster + '\
                                      <img class="profilePicture" src="' + data.reviews[i].profile_image_url + '" alt="Profile Image">\
                                      </h3>\
                                      </a>\
                                  </div>\
                                  <div class="col">\
                                      <div class="col">\
                                          <h3>\
                                              <div>\
                                                  <div class="stars-outer">\
                                                      <div id="' + data.reviews[i].id + '"class="stars-inner"></div>\
                                                  </div>\
                                              </div>\
                                          </h3>\
                                      </div>\
                                  </div>\
                              </div>\
                              <br>\
                              <p>' + data.reviews[i].review_text + '</p>\
                                <div id="review-' + data.reviews[i].id + '"></div>\
                              <div class="reviewFooter' + data.reviews[i].id + '">\
                              <div class="row">\
                              <div class="col">\
                              <button type="button" data-reviewid="' + data.reviews[i].id + '" class="get-comments review' + data.reviews[i].id + ' float-left btn btn-secondary btn-lg">Get comments</button>\
                              </div>\
                              <div class="col">\
                              <form>\
                                <div class="form-group">\
                                    <textarea class="form-control" id="addcomment' + data.reviews[i].id + '" rows = "3" placeholder="Enter your comment here"></textarea>\
                                </div>\
                              <div class="text-danger error-' + data.reviews[i].id + ' float-right">\
                              </div>\
                              <button type="button" data-reviewid="' + data.reviews[i].id + '" class="add-comment float-right btn btn-secondary btn-lg">Add comment</button>\
                              </form>\
                              </div>\
                              </div>\
                              </div>\
                          </div>';
            const html = parser.parseFromString(domString, 'text/html');

            $('.reviewContainer').append(html.body.firstChild);

            $('.journal')

			// Hide 'add comment' form if user is not authenticated
            if (authenticated == false){
                console.log("here");
                $('.add-comment').hide();
                $(".form-control").hide();

            }
			
			// If there are no more reviews to retrieve, hide the 'get more' button
            if (data.more == false) {
                $('.getmorereviews').hide();

            }
			
			// Generate the visual star ratings on the reviews
            const starwidth = (data.reviews[i].rating * 20 + "%");
            $("#" + data.reviews[i].id + "").width(starwidth);
			$("button.review" + data.reviews[i].id).trigger("click"); // Retrieve first 3 comments
        }
    });
});
$(".get-reviews").trigger("click");

// Create 'get comments' button, which is specific to each review
$(document).on("click", ".get-comments" , function() {
        const reviewid = $(this).attr("data-reviewid");
			// AJAX request to get comments
            $.getJSON('/ajax/get_comments/', {
                review : reviewid,
                start: commentNo[reviewid],
            }, function(data, textStatus, jqXHR) {
				// Track starting index of next 3 comments and the number remaining for each review
                commentNo[reviewid] = commentNo[reviewid] + 3;
                noMoreComments = data['number'] - 3
                $('.get-comments.review' + reviewid).html('Get more comments (' + noMoreComments + ')')
                const parser = new DOMParser();
				
				// For each comment, generate HTML
                for (i = 0; i < data.comments.length; i++) {
                    if (!($('.' + data.comments[i].id).length)){
                    const domString = '<div class="jumbotron comments comment-' + data.comments[i].id +'">\
                                      <div class="row">\
                                          <div class="col">\
                                              <a href="../../../profile/' + data.comments[i].username + '"><h3 class="gameName">' + data.comments[i].poster + '\
                                              <img class="profilePicture" src="' + data.comments[i].profile_image_url + '" alt="Profile Image">\
                                              </h3>\
                                              </a>\
                                          </div>\
                                      </div>\
                                      <p>' + data.comments[i].comment_text + '</p>\
                                  </div>';
                    const html = parser.parseFromString(domString, 'text/html');

                    $('#review-' + reviewid).append(html.body.firstChild);

                    }
                }
				
				// If there are no more comments, hide the 'get comments' button
                if (data.more == false) {
                    $('.get-comments.review' + reviewid).hide();
                }
        });
        });

// Define 'add comment' button
$(document).on("click", ".add-comment" , function() {
    const reviewid = $(this).attr("data-reviewid");
    const commentText = $("#addcomment" + reviewid).val();
	
	// AJAX request structure for POST request
    $.ajax({
        url : '/ajax/add_comment/',
        type : 'POST',
        data : { review : reviewid, comment_text : commentText},

		// Define function which is called on a successful comment submission
        success : function(data) {
			// Hide the add comment box & button and error text
            $('.add-comment').hide();
            $("#addcomment" + reviewid).hide();
            $('.error-' + reviewid).hide();

			// Display the newly created comment from AJAX response
            const parser = new DOMParser();
            const domString = '<div class="jumbotron comments ' + data.comment.id +'">\
                              <div class="row">\
                                  <div class="col">\
                                      <h3 class="gameName">' + data.comment.poster + '\
                                      <img class="profilePicture" src="' + data.comment.profile_image_url + '" alt="Profile Image">\
                                      </h3>\
                                  </div>\
                              </div>\
                              <p>' + data.comment.comment_text + '</p>\
                          </div>';
            const html = parser.parseFromString(domString, 'text/html');

            $('.' + reviewid).append(html.body.firstChild);




        },

		// Define function called when comment posting fails
        error : function(xhr, errmsg, err){
            $('.error-' + reviewid).html(JSON.parse(xhr.responseText).error); // Display error returned by the server
        }

});

});
});

// This function adds the CSRF token to the POST request, so that adding comments
// works correctly whilst retaining the security function provided by CSRF tokens.
// This code originates from https://github.com/realpython/django-form-fun/blob/master/part1/main.js
$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
