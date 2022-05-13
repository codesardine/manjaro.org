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

    cursorHoverA.forEach(a => {
        a.addEventListener("mouseover", function(e) {
            if (!a.classList.contains("no-mouse-effects")) {              
                if (a.classList.contains("cursor-difference")) {
                    cursor.classList.add("cursor-difference")
                } else if (a.classList.contains("cursor-saturation")) {
                    cursor.classList.add("cursor-saturation")
                }
                if (!a.classList.contains("no-zoom")) {
                    cursor.classList.add("enlarge")
                }
            }
        })
    });

    cursorHoverA.forEach(a => {
        a.addEventListener("mouseout", function(e) {
            cursor.classList.remove("enlarge","cursor-difference","cursor-saturation","hidden")
        })
    });

    document.querySelectorAll('code').forEach((el) => {
        hljs.highlightElement(el);
    });

})