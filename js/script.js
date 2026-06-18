// Light/Dark Theme Toggle Logic
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");

  // Load saved theme preference
  const savedTheme = localStorage.getItem("portfolio-theme");
  if (savedTheme === "light") {
    document.body.classList.add("light-theme");
    if (themeIcon) {
      themeIcon.classList.replace("bi-moon-stars-fill", "bi-sun-fill");
    }
  }

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      document.body.classList.toggle("light-theme");
      if (document.body.classList.contains("light-theme")) {
        if (themeIcon) {
          themeIcon.classList.replace("bi-moon-stars-fill", "bi-sun-fill");
        }
        localStorage.setItem("portfolio-theme", "light");
      } else {
        if (themeIcon) {
          themeIcon.classList.replace("bi-sun-fill", "bi-moon-stars-fill");
        }
        localStorage.setItem("portfolio-theme", "dark");
      }
    });
  }
});




// Filter Using JavaScript (with jQuery)
$(document).ready(function () {
  $(".filter-item").click(function () {
    const value = $(this).attr("data-filter");
    if (value === "all") {
      $(".post").show("1000");
    } else {
      $(".post").not("." + value).hide("1000");
      $(".post").filter("." + value).show("1000");
    }
  });
});

// Sticky Navbar
document.addEventListener("DOMContentLoaded", function () {
  window.addEventListener("scroll", function () {
    const navbar = document.getElementById("navbar-top");
    if (window.scrollY > 50) {
      navbar.classList.add("fixed-top");
      // Add padding top to show content behind the navbar
      let navbarHeight = document.querySelector(".navbar").offsetHeight;
      document.body.style.paddingTop = navbarHeight + "px";
    } else {
      navbar.classList.remove("fixed-top");
      // Remove padding top from the body
      document.body.style.paddingTop = "0";
    }
  });
});

// Back-to-Top Button Functionality
let myButton = document.getElementById("btn-back-to-top");

// Show button when user scrolls down 20px
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    myButton.style.display = "block";
  } else {
    myButton.style.display = "none";
  }
}

// Scroll to top when the button is clicked
myButton.addEventListener("click", function () {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
});



// For Hidden Projects
document.addEventListener("DOMContentLoaded", function () {
  let hiddenProjects = document.querySelectorAll(".hidden-project");
  let showMoreBtn = document.getElementById("showMoreBtn");

  showMoreBtn.addEventListener("click", function () {
      hiddenProjects.forEach(project => project.style.display = "block");
      showMoreBtn.style.display = "none"; // Hide the button after showing projects
  });
});
