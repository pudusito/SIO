const btn = document.getElementById("themeToggle");
const icon = document.getElementById("themeIcon");
const iconosDataSet = document.getElementById("iconos-ruta");

// Actualizar icono según el estado actual
function updateIcon() {
    if (document.body.classList.contains("dark")) {
        icon.src = iconosDataSet.dataset.soon; // Oscuro → Sol
    } else {
        icon.src = iconosDataSet.dataset.moon; // Claro → Luna
    }
}

// Ejecutar cuando la página carga
updateIcon();

btn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    updateIcon();
});
