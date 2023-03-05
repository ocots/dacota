function tooltip_eventlistener(equation_name, leave_on_icon) {
  const icon = document.getElementById("tooltip-" + equation_name);
  const container = document.getElementById(equation_name);

  icon.addEventListener("mouseover", () => {
    container.style.display = "block";
  });

  let leave_element = leave_on_icon ? icon : container;
  leave_element.addEventListener("mouseleave", () => {
    container.style.display = "none";
  });
}

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

  var menuRemove = document.getElementById("index-content");

  menuRemove.addEventListener("click", function () {
    if (menu.classList.contains("show")) {
      menu.classList.remove("show");
    }
  });

  /* SPINNER CODE */
  const form = document.getElementById("components-selection");
  const spinner = document.getElementById("spinner");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (spinner) {
      spinner.style.display = "block";
    }
    form.submit();
  });

  /* Add a new compound */
  const addCompoundBtn = document.getElementById("add-compound-btn");
  const compoundFormContainer = document.getElementById(
    "compound-form-container"
  );
  const compoundForm = document.getElementById("compound-form");

  addCompoundBtn.addEventListener("click", () => {
    var new_state;
    if (compoundFormContainer.style.display == "block") {
      new_state = "none";
    } else {
      new_state = "block";
    }
    compoundFormContainer.style.display = new_state;
  });

  compoundForm.addEventListener("submit", (event) => {
    event.preventDefault();
    compoundFormContainer.style.display = "none";
    compoundForm.submit();
  });

  /* Add new relation */
  const addRelationBtn = document.getElementById("add-relation-btn");
  const relationForm = document.getElementById("relation-form-container");

  addRelationBtn.addEventListener("click", () => {
    relationForm.style.display =
      relationForm.style.display === "none" ? "block" : "none";
  });

  /* close icon */
  const close_icons = document.getElementsByClassName(
    "fa-sharp fa-regular fa-circle-xmark"
  );
  for (let i = 0; i < close_icons.length; i++) {
    close_icons[i].addEventListener("click", (event) => {
      close_icons[i].parentElement.style.display = "none";
    });
  }

  /** Tooltip for equation imgs */
  tooltip_eventlistener("antoine", false);
  tooltip_eventlistener("nrtl", false);
  tooltip_eventlistener("mixture", true);
});
