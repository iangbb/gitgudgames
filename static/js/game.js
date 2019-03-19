let startval = 0;

//document.getElementById("{{ game.average_rating }}").style.width = (({{game.average_rating}}* 20) + "%");

$(document).ready(function() {

$('.get-reviews').click(function() {
    const gameid = $(this).attr("data-gameid");
    $.getJSON('/ajax/get_reviews/', {
        game: gameid,
        start: startval
    }, function(data, textStatus, jqXHR) {
        startval = startval + 3;
        const parser = new DOMParser();
        for (i = 0; i < data.reviews.length; i++) {
            const domString = '<div class="jumbotron">\
                              <div class="row">\
                                  <div class="col">\
                                      <h3 class="gameName">' + data.reviews[i].poster + '</h3>\
                                      <img class="profilePicture" src="' + data.reviews[i].profile_image_url + '" alt="Profile Image">\
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
                          </div>';
            const html = parser.parseFromString(domString, 'text/html');

            $('.reviewContainer').append(html.body.firstChild);
            if (data.more == false) {
                $('.getmorereviews').hide();
            }
            const starwidth = (data.reviews[i].rating * 20 + "%");
            $("#" + data.reviews[i].id + "").width(starwidth);
            $(".profilePicture").width("50px");
            $(".profilePicture").height("50px");
        }
    });
});

var gameScore = ($("#gameStars").attr('gameScore') * 20 + "%");
$("#gameStars").width(gameScore);
$(".get-reviews").trigger("click");

});
