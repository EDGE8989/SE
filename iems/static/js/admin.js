document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.querySelector(".admin-mobile-toggle");

  if (sidebar && sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      sidebar.classList.toggle("is-open");
    });

    document.addEventListener("click", (event) => {
      const clickedInsideSidebar = sidebar.contains(event.target);
      const clickedToggle = sidebarToggle.contains(event.target);
      if (!clickedInsideSidebar && !clickedToggle) {
        sidebar.classList.remove("is-open");
      }
    });
  }

  document.querySelectorAll("[id$='Modal']").forEach((modal) => {
    modal.addEventListener("click", (event) => {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      document.querySelectorAll("[id$='Modal']").forEach((modal) => {
        modal.style.display = "none";
      });
    }
  });

  document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", () => {
      const submitButton = form.querySelector("button[type='submit']");
      if (submitButton && !submitButton.dataset.keepEnabled) {
        submitButton.disabled = true;
        submitButton.style.opacity = "0.75";
      }
    });
  });
});
