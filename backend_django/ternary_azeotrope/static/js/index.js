/*const comp_form =  document.getElementsByName("form");
console.log(comp_form);

comp_form.addEventListener("submit", function(event) {
    event.preventDefault();
    document.getElementById("spinner").style.display = "block";
    this.submit();
});

$('form').on('submit', function(){
    console.log("submitted");
});*/
console.log("DEBUG");
const submitButton = document.getElementById("submit-btn");
console.log(submitButton);

document.addEventListener("DOMContentLoaded", function () {
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

  var menuToggleIcon = document.getElementById("menu-icons");

  menuToggleIcon.addEventListener("click", function () {
    if (menu.classList.contains("show")) {
      menu.classList.remove("show");
    }
  });
});
