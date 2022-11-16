function toggleDmenu(ev) {
    let menu = document.querySelector("#desktop-menu")
    let footer = document.querySelector("#footer");
    let screen = document.querySelector("#dim-screen")

    menu.classList.toggle("translate-y-[-110%]")
    footer.classList.toggle("translate-footer")
    screen.classList.toggle("h-full")
    screen.classList.toggle("w-full")
    screen.classList.toggle("opacity-0")
    screen.classList.toggle("opacity-50")
  }

const tooltipIcon = "<i class='fa-solid fa-circle-info ml-2'></i>"
 
document.addEventListener("DOMContentLoaded", (event) => {

  const toggleMobileBtn = document.getElementById("toggle-mobile-btn")
  toggleMobileBtn.addEventListener("click", function () {
    const menu = document.getElementById("menu")
    menu.classList.toggle("translate-x-[-150%]")

  });

  window.onclick = function (event) {
    let leftSubmenu = document.querySelectorAll(".dropdown")
    leftSubmenu.forEach(function (el) {
      if (el.id === "submenu" + event.target.textContent.trim()) {
        el.classList.toggle("hidden");
      } else {
        el.classList.add("hidden");
      }
    });
  };

  document.onkeyup = function (e) {
    if (event.ctrlKey && e.which == 77) {
      toggleDmenu();
    }
  }

  tippy(".home-btn", {
    content: "GO BACK HOME" + tooltipIcon,
    allowHTML: true,
  });

  tippy("#download-btn", {
    content: "GET MANJARO INSTALL MEDIA" + tooltipIcon,
    allowHTML: true,
  });

  tippy("#menu-btn", {
    content: "TOGGLE MENU - CTRL + M" + tooltipIcon,
    allowHTML: true,
  });

  tippy("#top-btn", {
    content: "BACK TO TOP" + tooltipIcon,
    allowHTML: true,
  });
});
