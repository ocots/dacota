console.log("menu");
window.onload = function () {
  const menuIcon = document.getElementById("menu-icon");
  const menu = document.getElementById("menu");
  const content = document.getElementById("content");

  if (menuIcon & menu) {
    menuIcon.addEventListener("click", function () {
      menu.classList.toggle("show");
      console.log("menu2");
    });

    content.addEventListener("click", function () {
      if (menu.classList.contains("show")) {
        menu.classList.remove("show");
      }
    });
  }
};
