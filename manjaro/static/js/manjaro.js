document.addEventListener('DOMContentLoaded', (event) => {
    
    const btnCloseMenu = document.getElementById("btn-close-menu")
    const btnOpenMenu = document.getElementById("btn-open-menu")

    btnCloseMenu.addEventListener("click", function() {
        const menu = document.getElementById("menu")
        menu.classList.add("hidden")
    })

    btnOpenMenu.addEventListener("click", function() {
        const menu = document.getElementById("menu")
        menu.classList.remove("hidden")
    })

    const cursor = document.getElementById("cursor");
    document.addEventListener("mousemove", function(e) {
        cursor.style.left = e.clientX + "px",
        cursor.style.top = e.clientY + "px";
    });


    const cursorHover = document.querySelectorAll("a");
    const cursorHoverBtn = document.querySelectorAll("button");
    cursorHover.forEach(a => {
        a.addEventListener("mouseover", function(e) {
            cursor.classList.add("enlarge")
        })
    });

    cursorHoverBtn.forEach(btn => {
        btn.addEventListener("mouseover", function(e) {
            cursor.classList.add("enlarge")
        })
    });


    cursorHoverBtn.forEach(btn => {
        btn.addEventListener("mouseout", function(e) {
            cursor.classList.remove("enlarge")
        })
    });

    cursorHover.forEach(a => {
        a.addEventListener("mouseout", function(e) {
            cursor.classList.remove("enlarge")
        })
    });

    document.querySelectorAll('code').forEach((el) => {
        hljs.highlightElement(el);
    });

})