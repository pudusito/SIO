// js/manejo-errores.js

document.addEventListener('DOMContentLoaded', () => {
    // 1. Seleccionar todos los campos de entrada relevantes (inputs de texto, fecha, etc.)
    // Incluimos .input-field (que usas en los select) y los inputs de texto/número.
    const fields = document.querySelectorAll('input, textarea, select');
    
    // 2. Definir la clase de error que Django añade o que tú añades
    const errorClass = 'has-error';

    // Función que se ejecuta cuando el valor de un campo cambia
    const handleInputChange = (event) => {
        const field = event.target;
        // Subimos al contenedor principal (el .form-group) para remover la clase
        const formGroup = field.closest('.form-group');

        // Si el contenedor existe:
        if (formGroup) {
            // Verificamos si el campo tiene algún valor
            if (field.value.trim() !== '') {
                // Si el usuario escribe algo, removemos la clase de error del contenedor
                formGroup.classList.remove(errorClass);
                
                // Opcional: Remover mensajes de error que Django inyectó después del input
                const errorDisplay = formGroup.querySelector('.error-message');
                if (errorDisplay) {
                    errorDisplay.style.display = 'none';
                }
            } 
            // Si el campo se vacía después de tener un error, podríamos volver a poner la clase,
            // pero por lo general, se espera a que el formulario se envíe de nuevo.
        }
    };

    // 3. Adjuntar el listener a todos los campos
    fields.forEach(field => {
        // Usamos 'input' para inputs de texto (se dispara inmediatamente al escribir)
        // y 'change' para selects/checkboxes
        field.addEventListener('input', handleInputChange);
        field.addEventListener('change', handleInputChange); 
    });
});