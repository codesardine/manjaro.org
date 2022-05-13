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


    const cursorHoverA = document.querySelectorAll("a");
    const cursorHoverP = document.querySelectorAll("p");
    const cursorHoverBtn = document.querySelectorAll("button");

    cursorHoverA.forEach(a => {
        a.addEventListener("mouseover", function(e) {
            cursor.classList.add("enlarge")
            if (a.classList.contains("cursor-difference")) {
                cursor.classList.add("cursor-difference")
            } else if (a.classList.contains("cursor-saturation")) {
                cursor.classList.add("cursor-saturation")
            } else if (a.classList.contains("no-mouse-effect")) {
                cursor.classList.add("hidden")
            }
        })
    });

    cursorHoverA.forEach(a => {
        a.addEventListener("mouseout", function(e) {
            cursor.classList.remove("enlarge","cursor-difference","cursor-saturation","hidden")
        })
    });

    cursorHoverP.forEach(p => {
        p.addEventListener("mouseover", function(e) {
            console.log(p.textContent.length)
            if (p.classList.contains("no-zoom") === false && p.textContent.trim() != 0) {
                cursor.classList.add("enlarge-p")
            } else {
                p.classList.add("no-zoom")
            }
            
        })
    });

    cursorHoverP.forEach(p => {
        p.addEventListener("mouseout", function(e) {
            cursor.classList.remove("enlarge-p")
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

    document.querySelectorAll('code').forEach((el) => {
        hljs.highlightElement(el);
    });

})