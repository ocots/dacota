function toggleButton(btn) {
  // Remove 'clicked' class from both buttons
  document.querySelectorAll(".btn").forEach(function (btn) {
    btn.classList.remove("clicked");
  });

  // Add 'clicked' class to the clicked button
  btn.classList.add("clicked");
}
