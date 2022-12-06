function dimScreen() {
    let screen = document.querySelector("#dim-screen")
    screen.classList.toggle("h-full")
    screen.classList.toggle("w-full")
    screen.classList.toggle("backdrop-grayscale-0")
    screen.classList.toggle("backdrop-grayscale")
}

function toggleMmenu() {
  let mobileMenu = document.getElementById("mobile-menu")
  mobileMenu.classList.toggle("translate-x-[-150%]")
}

function hideIntro() {
  let intro = document.querySelector("#intro")
  if (intro !=null) {
    intro.classList.toggle("translate-y-[-110%]")
  }
}

function toggleDmenu() {
    let menu = document.querySelector("#desktop-menu")
    let footer = document.querySelector("#footer")
    menu.classList.toggle("translate-y-[-110%]")
    footer.classList.toggle("translate-footer")
    dimScreen()
    hideIntro()
  }

document.onkeyup = function (e) {
    if (event.ctrlKey && e.which == 77) {
        toggleDmenu()
    }
}
 
document.addEventListener("DOMContentLoaded", (event) => {

  const toggleMobileBtn = document.getElementById("toggle-mobile-btn")
  toggleMobileBtn.addEventListener("click", function () {
    toggleMmenu()
    dimScreen()
  })

  document.querySelector("#dim-screen").onclick = function () {
    dimScreen()
    let mobileMenu = document.getElementById("mobile-menu")
    let desktopMenu = document.getElementById("desktop-menu")
      mobileMenu.classList.add("translate-x-[-150%]")
      desktopMenu.classList.add("translate-y-[-110%]")
      let footer = document.querySelector("#footer")
      footer.classList.add("translate-footer")
      hideIntro()
  }

  window.onclick = function (event) {
    let leftSubmenu = document.querySelectorAll(".dropdown")
    leftSubmenu.forEach(function (el) {
      if (el.id === "submenu" + event.target.textContent.trim()) {
        el.classList.toggle("hidden")
      } else {
        el.classList.add("hidden")
      }
    })
  }

  tippy(".home-btn", {
    content: "GO BACK HOME" + tooltipIcon,
    allowHTML: true,
  })

  tippy("#download-btn", {
    content: "GET MANJARO INSTALL MEDIA" + tooltipIcon,
    allowHTML: true,
  })

  tippy("#menu-btn", {
    content: "TOGGLE MENU _ CTRL + M" + tooltipIcon,
    allowHTML: true,
  })
  const node = document.getElementById("link-grid")
  const twiter = document.getElementsByClassName("twitter-timeline")
  twiter[0].setAttribute("height", node.offsetHeight)
})

