document.addEventListener("DOMContentLoaded", (event) => {
  const toggleMobileBtn = document.getElementById("toggle-mobile-btn")
  toggleMobileBtn.addEventListener("click", function () {
    toggleMmenu()
    dimScreen()
  })

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

