// Función reutilizable para animar
function animarContador(elemento) {
    let startValue = 0;
    let endValue = parseInt(elemento.getAttribute("data-val"));
    let duration = 2000; // Duración en milisegundos (2 segundos)
    let startTime = null;

    function step(currentTime) {
        if (!startTime) startTime = currentTime;
        
        // Calcula cuánto tiempo ha pasado (0.0 a 1.0)
        let progress = Math.min((currentTime - startTime) / duration, 1);

        // Calcula el número actual basado en el progreso
        // Math.floor quita los decimales
        elemento.innerHTML = Math.floor(progress * (endValue - startValue) + startValue);

        // Si no ha terminado, pide el siguiente cuadro de animación
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    }

    // Inicia la animación
    window.requestAnimationFrame(step);
}

// Configuración del Observador
let observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Si el elemento es visible, ¡animar!
            animarContador(entry.target);
            // Dejar de observar para que no se repita
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 }); // Se activa cuando el 50% del elemento es visible

// Conectar el observador a los elementos
document.querySelectorAll('.contador').forEach(contador => {
    observer.observe(contador);
});