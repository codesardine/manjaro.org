toggleMenu = () => {
  let mobileMenu = document.getElementById("mobile-menu")
  mobileMenu.classList.toggle("translate-x-[-150%]")
  let menuDocs = document.getElementById("menu-docs")
  if (menuDocs) {
    menuDocs.classList.add("translate-x-[-150%]")
  }
}

window.addEventListener("load", () => {
  const loading = document.getElementById("loading")
  loading.classList.add("hidden")
  const toggleMobileBtn = document.getElementById("toggle-mobile-btn")
  toggleMobileBtn.addEventListener("click", () => {
    toggleMenu()
  })
  
  const queryMsg = "Input a query to search for"
  const searchBtn = document.getElementById("search-form")
  searchBtn.addEventListener("submit", (event) => {
    let search = document.getElementById("search-query")
    if (search.value == 0) {
      event.preventDefault();
      alert(queryMsg)
    } else {
      loading.classList.remove("hidden")
    }
  })

  const searchBtnM = document.getElementById("search-form-mobile")
  searchBtnM.addEventListener("submit", (event) => {
    let search = document.getElementById("search-query-mobile")
    if (search.value == 0) {
      event.preventDefault();
      alert(queryMsg)
    }
  })

  const leftMenu = document.querySelector("#left-menu")
  const buttons = leftMenu.querySelectorAll("button")
  buttons.forEach((btn) => {
    let submenu = btn.parentElement.querySelector(".dropdown")
    btn.onmouseenter = function () {  
      let subMenus = document.querySelectorAll(".dropdown")    
      subMenus.forEach((el) => {
        el.classList.add("hidden")
      })
      submenu.classList.remove("hidden")
    }
    submenu.onmouseleave = function () {      
      submenu.classList.add("hidden")
    }
    submenu.onmouseenter = function () {
      clearTimeout(navTimeout);
    }
    btn.onmouseleave = function () {
      navTimeout = setTimeout( function() {
        submenu.classList.add("hidden")
      }, 200);
    }
    btn.onclick = function () {
      submenu.classList.toggle("hidden")
    }
  })

  tippy(".home-btn", {
    content: "BACK HOME" + tooltipIcon,
    allowHTML: true,
  })

  tippy("#download-btn", {
    content: "DOWNLOAD INSTALL MEDIA" + tooltipIcon,
    allowHTML: true,
  })

  tippy("#donate-btn", {
    content: "SUPPORT THE PROJECT" + tooltipIcon,
    allowHTML: true,
  })

  const node = document.getElementById("link-grid")
})

