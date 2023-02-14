document.addEventListener("DOMContentLoaded", function () {

  /* SLIDING bar CODE*/
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

  /* SPINNER CODE */
  const form = document.getElementById("components-selection");
  const spinner = document.getElementById("spinner");
  spinner.style.display = "none";
  form.addEventListener("submit", function(event) {
    event.preventDefault();
    spinner.style.display = "block";
    this.submit();
  });






});
