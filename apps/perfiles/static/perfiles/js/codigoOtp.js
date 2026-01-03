document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('otp-form');
    const boxes = document.querySelectorAll('.otp-box');
    const hiddenInput = document.getElementById('id_codigo'); // Usamos el ID que Django genera

    if (!form || boxes.length === 0 || !hiddenInput) return;

    const updateHiddenInputAndSubmit = () => {
        const code = Array.from(boxes).map(b => b.value).join('');
        hiddenInput.value = code;

        // Si el código tiene la longitud esperada, envía el formulario.
        if (code.length === boxes.length) {
            form.submit();
        }
    };

    boxes.forEach((box, index) => {
        box.addEventListener('input', (e) => {
            // Si se ingresa un valor, avanza al siguiente campo
            if (box.value.length === 1 && index < boxes.length - 1) {
                boxes[index + 1].focus();
            }
            updateHiddenInputAndSubmit();
        });

        box.addEventListener('keydown', (e) => {
            // Si se presiona Backspace en un campo vacío, retrocede al anterior
            if (e.key === 'Backspace' && box.value.length === 0 && index > 0) {
                boxes[index - 1].focus();
            }
        });

        box.addEventListener('paste', (e) => {
            e.preventDefault();
            const pasteData = e.clipboardData.getData('text').trim();
            
            // Si el dato pegado es numérico o alfanumérico y tiene la longitud correcta
            if (pasteData && pasteData.length > 0) {
                let currentBox = index;
                for (let i = 0; i < pasteData.length; i++) {
                    if (currentBox < boxes.length) {
                        boxes[currentBox].value = pasteData[i];
                        currentBox++;
                    }
                }

                // Mueve el foco al último campo llenado o al siguiente vacío
                if (currentBox < boxes.length) {
                    boxes[currentBox].focus();
                } else {
                    boxes[boxes.length - 1].focus();
                }

                updateHiddenInputAndSubmit();
            }
        });
    });
});
