document.addEventListener("DOMContentLoaded", function () {
  /* SLIDING BAR CODE*/
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

  /* SPINNER CODE */
  const form = document.getElementById("components-selection");
  const spinner = document.getElementById("spinner");
  spinner.style.display = "none";
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    spinner.style.display = "block";
    form.submit();
  });


  /* Add a new compound */
  const addCompoundBtn = document.getElementById("add-compound-btn");
  const compoundFormContainer = document.getElementById("compound-form-container");
  const compoundForm = document.getElementById("compound-form");


  addCompoundBtn.addEventListener("click", () => {
    compoundFormContainer.style.display = "block";
  });

  compoundForm.addEventListener("submit", (event) => {
    event.preventDefault();
    compoundFormContainer.style.display = "none";
    compoundForm.submit();
  });










});
