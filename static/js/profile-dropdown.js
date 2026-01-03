/* scripts/profile-dropdown.js */

document.addEventListener("DOMContentLoaded", () => {
    const dropdownBtn = document.querySelector(".dropdown-btn");
    const dropdownMenu = document.querySelector(".profile-dropdown");
    const container = document.querySelector(".profile-container");

    // 1. Alternar visibilidad al hacer clic en el botón
    dropdownBtn.addEventListener("click", (e) => {
        e.stopPropagation(); // Evita que el click llegue al document
        dropdownMenu.classList.toggle("active");
        
        // Opcional: Rotar la flechita
        dropdownBtn.classList.toggle("active");
    });

    // 2. Cerrar si se hace clic fuera del contenedor del perfil
    document.addEventListener("click", (e) => {
        if (!container.contains(e.target)) {
            dropdownMenu.classList.remove("active");
            dropdownBtn.classList.remove("active");
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // 1. Obtenemos la ruta real actual (Ej: "/pacientes/listar" o "/")
    const currentPath = window.location.pathname;

    const navLinks = document.querySelectorAll(".sidebar .nav-link");

    navLinks.forEach(link => {
        // Limpiamos estados previos
        link.classList.remove("active");

        // Obtenemos el href que generó Django (Ej: "/" o "/pacientes/")
        const linkHref = link.getAttribute("href");

        // VALIDACIÓN DE SEGURIDAD: Si el href es nulo o vacío, saltamos
        if (!linkHref) return;

        // CASO 1: EL INICIO (Raíz)
        // Si el botón lleva a la raíz, exigimos que la URL sea EXACTAMENTE la raíz.
        // Así evitamos que se active cuando estás en "/pacientes"
        if (linkHref === "/" || linkHref === "") {
            if (currentPath === "/") {
                link.classList.add("active");
            }
        } 
        // CASO 2: LOS MÓDULOS (Pacientes, Partos, etc.)
        // Si no es la raíz, usamos "startsWith" para que "/pacientes/crear" active "/pacientes/"
        else if (currentPath.startsWith(linkHref)) {
            link.classList.add("active");
        }
    });
});