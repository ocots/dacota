document.addEventListener("DOMContentLoaded", function () {
  const menuIcon = document.getElementById("menu-icon");
  const menu = document.getElementById("menu");

  menuIcon.addEventListener("click", function () {
    menu.classList.toggle("show");
  });

  var menuToggleIcon = document.getElementById("menu-icons");

  menuToggleIcon.addEventListener("click", function () {
    if (menu.classList.contains("show")) {
      menu.classList.remove("show");
    }
  });
});
