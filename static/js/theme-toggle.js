const btn = document.getElementById("themeToggle");
const icon = document.getElementById("themeIcon");
const iconosDataSet = document.getElementById("iconos-ruta");

// 1. AL CARGAR: Verificar si ya había un tema guardado
// Si el usuario ya eligió "dark", lo aplicamos de inmediato
if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
}

// 2. Función para actualizar el icono (Sol o Luna)
function updateIcon() {
    if (document.body.classList.contains("dark")) {
        icon.src = iconosDataSet.dataset.sun; // Si es oscuro, mostrar sol
    } else {
        icon.src = iconosDataSet.dataset.moon; // Si es claro, mostrar luna
    }
}

// Ejecutamos para poner el icono correcto al inicio
updateIcon();

// 3. AL HACER CLICK: Alternar y guardar
btn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    
    // Guardar la preferencia en la memoria del navegador
    if (document.body.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
    
    updateIcon();
});