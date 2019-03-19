let reviewNo = 0;
let commentNo = [];
var noMoreReviews = 0;

//document.getElementById("{{ game.average_rating }}").style.width = (({{game.average_rating}}* 20) + "%");

$(document).ready(function() {

$('.get-reviews').click(function() {
    const authenticated = ($(this).attr("data-authenticated") == 'true');
    const gameid = $(this).attr("data-gameid");
    $.getJSON('/ajax/get_reviews/', {
        game: gameid,
        start: reviewNo,
    }, function(data, textStatus, jqXHR) {
        reviewNo = reviewNo + 3;
        noMoreReviews = data['number'] - 3
        $('.get-reviews').html('Get more reviews (' + noMoreReviews + ')')
        const parser = new DOMParser();
        for (i = 0; i < data.reviews.length; i++) {
            commentNo[data.reviews[i].id] = 0;
            const domString = '<div class="jumbotron">\
                              <div class="row">\
                                  <div class="col">\
                                      <h3 class="gameName">' + data.reviews[i].poster + '\
                                      <img class="profilePicture" src="' + data.reviews[i].profile_image_url + '" alt="Profile Image">\
                                      </h3>\
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
                                <div class="' + data.reviews[i].id + '"></div>\
                              <div class="reviewFooter' + data.reviews[i].id + '">\
                              <div class="row">\
                              <div class="col">\
                              <button type="button" data-reviewid="' + data.reviews[i].id + '" class="get-comments review' + data.reviews[i].id + ' float-left btn btn-secondary btn-lg">Get comments</button>\
                              </div>\
                              <div class="col">\
                              <button type="button"class="add-comment float-right btn btn-secondary btn-lg">Add comment</button>\
                              </div>\
                              </div>\
                              </div>\
                          </div>';
            const html = parser.parseFromString(domString, 'text/html');

            $('.reviewContainer').append(html.body.firstChild);

            if (authenticated == false){
                $('.add-comment').hide();
            }
            if (data.more == false) {
                $('.getmorereviews').hide();

            }
            const starwidth = (data.reviews[i].rating * 20 + "%");
            $("#" + data.reviews[i].id + "").width(starwidth);
        }
        $(".get-comments").trigger("click");
    });
});

var gameScore = ($("#gameStars").attr('gameScore') * 20 + "%");
$("#gameStars").width(gameScore);
$(".get-reviews").trigger("click");

$(document).on("click", ".get-comments" , function() {
        const reviewid = $(this).attr("data-reviewid");
            $.getJSON('/ajax/get_comments/', {
                review : reviewid,
                start: commentNo[reviewid],
            }, function(data, textStatus, jqXHR) {
                commentNo[reviewid] = commentNo[reviewid] + 3;
                noMoreComments = data['number'] - 3
                $('.get-comments.review' + reviewid).html('Get more comments (' + noMoreComments + ')')
                console.log(data);
                const parser = new DOMParser();
                for (i = 0; i < data.comments.length; i++) {
                    const domString = '<div class="jumbotron comments">\
                                      <div class="row">\
                                          <div class="col">\
                                              <h3 class="gameName">' + data.comments[i].poster + '\
                                              <img class="profilePicture" src="' + data.comments[i].profile_image_url + '" alt="Profile Image">\
                                              </h3>\
                                          </div>\
                                      </div>\
                                      <p>' + data.comments[i].comment_text + '</p>\
                                  </div>';
                    const html = parser.parseFromString(domString, 'text/html');

                    $('.' + reviewid).append(html.body.firstChild);

                    }
                    if (data.more == false) {
                        console.log('.get-comments.review' + reviewid);
                        $('.get-comments.review' + reviewid).hide();
                }
        });
        });
});
