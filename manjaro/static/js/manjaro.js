document.addEventListener('DOMContentLoaded', (event) => {
    
    const btnCloseMenu = document.getElementById("btn-close-menu")
    const btnOpenMenu = document.getElementById("btn-open-menu")

    btnCloseMenu.addEventListener("click", function() {
        const menu = document.getElementById("menu")
        menu.classList.add("translate-x-[-150%]")
    })

    btnOpenMenu.addEventListener("click", function() {
        const menu = document.getElementById("menu")
        menu.classList.remove("translate-x-[-150%]")
    })

    document.querySelectorAll('code').forEach((el) => {
        hljs.highlightElement(el);
    });

})