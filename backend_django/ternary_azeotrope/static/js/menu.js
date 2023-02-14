const menuIcon = document.getElementById("menu-icon");
const menu = document.getElementById("menu");
const content = document.getElementById("content");

menuIcon.addEventListener("click", function () {
  menu.classList.toggle("show");
});

content.addEventListener("click", function () {
  if (menu.classList.contains("show")) {
    menu.classList.remove("show");
  }
});
