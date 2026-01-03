// Este es el código que necesitas.
document.addEventListener('DOMContentLoaded', (event) => {
    // 1. Obtener los elementos DOM
    const selector = document.getElementById('id_documento');
    const inputValor = document.getElementById('id_identificacion');
    
    // 2. Definir la función de manejo (handler)
    const manejarDeshabilitacion = () => {
        const valorSeleccionado = selector.value;
        const valorCondicional = 'TMP'; // El valor que queremos que deshabilite
        
        // 3. Aplicar la lógica de deshabilitación
        if (valorSeleccionado === valorCondicional) {
            inputValor.disabled = true;
            inputValor.value = ''; // Limpiamos el valor al deshabilitar
            inputValor.placeholder = 'NO APLICA';
        } else {
            inputValor.disabled = false;
            inputValor.placeholder = 'Ingrese el Valor';
        }
    };

    // 4. Adjuntar el listener al evento 'change' del select
    selector.addEventListener('change', manejarDeshabilitacion);

    // Opcional: Ejecutar la función al inicio para reflejar el valor por defecto si existe.
    manejarDeshabilitacion();
});