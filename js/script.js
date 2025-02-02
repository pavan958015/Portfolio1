// HTML/CSS Progress Circular Bar
let htmlProgress = document.querySelector(".html-css"),
  htmlValue = document.querySelector(".html-progress");

let htmlStartValue = 0,
  htmlEndValue = 90,
  htmlSpeed = 30;

let progressHtml = setInterval(() => {
  htmlStartValue++;
  htmlValue.textContent = `${htmlStartValue}%`;
  htmlProgress.style.background = `conic-gradient(#fca61f ${htmlStartValue * 3.6}deg, #ededed 0deg)`;

  if (htmlStartValue === htmlEndValue) {
    clearInterval(progressHtml);
  }
}, htmlSpeed);

// JavaScript Progress Circular Bar
let javascriptProgress = document.querySelector(".javascript"),
  javascriptValue = document.querySelector(".javascript-progress");

let javascriptStartValue = 0,
  javascriptEndValue = 75,
  jsSpeed = 30;

let progressJs = setInterval(() => {
  javascriptStartValue++;
  javascriptValue.textContent = `${javascriptStartValue}%`;
  javascriptProgress.style.background = `conic-gradient(#7d2ae8 ${javascriptStartValue * 3.6}deg, #ededed 0deg)`;

  if (javascriptStartValue === javascriptEndValue) {
    clearInterval(progressJs);
  }
}, jsSpeed);

// PHP Progress Circular Bar
let phpProgress = document.querySelector(".php"),
  phpValue = document.querySelector(".php-progress");

let phpStartValue = 0,
  phpEndValue = 80,
  phpSpeed = 30;

let progressPhp = setInterval(() => {
  phpStartValue++;
  phpValue.textContent = `${phpStartValue}%`;
  phpProgress.style.background = `conic-gradient(#20c997 ${phpStartValue * 3.6}deg, #ededed 0deg)`;

  if (phpStartValue === phpEndValue) {
    clearInterval(progressPhp);
  }
}, phpSpeed);

// ReactJS Progress Circular Bar
let reactProgress = document.querySelector(".reactjs"),
  reactValue = document.querySelector(".reactjs-progress");

let reactStartValue = 0,
  reactEndValue = 30,
  reactSpeed = 30;

let progressReact = setInterval(() => {
  reactStartValue++;
  reactValue.textContent = `${reactStartValue}%`;
  reactProgress.style.background = `conic-gradient(#3f396d ${reactStartValue * 3.6}deg, #ededed 0deg)`;

  if (reactStartValue === reactEndValue) {
    clearInterval(progressReact);
  }
}, reactSpeed);

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
