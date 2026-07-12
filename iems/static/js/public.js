document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.getElementById("navLinks");

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const isOpen = navLinks.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
      navToggle.querySelector("i")?.classList.toggle("fa-xmark", isOpen);
      navToggle.querySelector("i")?.classList.toggle("fa-bars", !isOpen);
    });

    navLinks.addEventListener("click", (event) => {
      if (event.target.closest("a")) {
        navLinks.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        navToggle.querySelector("i")?.classList.add("fa-bars");
        navToggle.querySelector("i")?.classList.remove("fa-xmark");
      }
    });
  }
});
