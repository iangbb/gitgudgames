// Function to set nav-item active
function set_active_tab(tab_name) {
  document.getElementById("home_tab").classList.remove("active");
  document.getElementById("about_tab").classList.remove("active");
  document.getElementById("games_tab").classList.remove("active");
  document.getElementById("profile_tab").classList.remove("active");

  document.getElementById(tab_name).classList.add("active");
}

// Function to bring user to top of page
function back_to_top() {
    document.body.scrollTop = 0; // Safari
    document.documentElement.scrollTop = 0; // Everything else
}

function populate_edit_profile(id_name, data_entry) {
    document.getElementById(id_name).value = data_entry;
}

// Function to set a carousel-item to active
function set_active_image(image_name) {
  // Image parent needs to be set to active
  image_div = document.getElementById(image_name).parentElement
  image_div.classList.add("active");
}

$(document).ready(function() {
    $(".stars-inner").each(function(){
        var gameScore = $(this).attr('gameScore') * 20 + "%";
        $(this).width(gameScore);
    });
});
