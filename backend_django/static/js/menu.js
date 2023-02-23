document.addEventListener("DOMContentLoaded", function () {
  const menuIcon = document.getElementById("menu-icon");
  const menu = document.getElementById("menu");
  const menu_content = document.getElementById("content");

  menuIcon.addEventListener("click", function () {
    menu.classList.toggle("show");
    menu_content.style.display = "block";
  });

  var menuToggleIcon = document.getElementById("menu-icons");

  menuToggleIcon.addEventListener("click", function () {
    if (menu.classList.contains("show")) {
      menu.classList.remove("show");
      menu_content.style.display = "none";
    }
  });
});
