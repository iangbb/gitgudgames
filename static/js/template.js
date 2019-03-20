function set_active_tab(tab_name) {
  document.getElementById("homeTab").classList.remove("active");
  document.getElementById("aboutTab").classList.remove("active");
  document.getElementById("gamesTab").classList.remove("active");

  document.getElementById(tab_name).classList.add("active");
}

function populate_edit_profile(id_name, data_entry) {
    document.getElementById(id_name).value = data_entry;
}
