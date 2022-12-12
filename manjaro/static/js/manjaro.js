toggleMenu = () => {
  let mobileMenu = document.getElementById("mobile-menu")
  mobileMenu.classList.toggle("translate-x-[-150%]")
}

window.addEventListener("load", () => {
  const toggleMobileBtn = document.getElementById("toggle-mobile-btn")
  toggleMobileBtn.addEventListener("click", () => {
    toggleMenu()
  })

  window.onclick = (event) => {
    let leftSubmenu = document.querySelectorAll(".dropdown")
    leftSubmenu.forEach((el) => {
      if (el.id === "submenu" + event.target.textContent.trim()) {
        el.classList.toggle("hidden")
      } else {
        el.classList.add("hidden")
      }
    })
  }

  tippy(".home-btn", {
    content: "BACK HOME" + tooltipIcon,
    allowHTML: true,
  })

  tippy("#download-btn", {
    content: "GET INSTALL MEDIA" + tooltipIcon,
    allowHTML: true,
  })

  const node = document.getElementById("link-grid")
  const twiter = document.getElementsByClassName("twitter-timeline")
  twiter[0].setAttribute("height", node.offsetHeight)
})

