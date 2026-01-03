document.addEventListener('DOMContentLoaded', function () {
    const newPasswordInput = document.getElementById('new-password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const submitButton = document.getElementById('submit-btn');

    // Si los campos de contraseña no existen en la página, detenemos el script.
    if (!newPasswordInput || !confirmPasswordInput || !submitButton) {
        console.error("No se encontraron los campos de contraseña o el botón de envío.");
        return;
    }

    const requirements = {
        length: document.getElementById('req-length'),
        lower: document.getElementById('req-lower'),
        upper: document.getElementById('req-upper'),
        number: document.getElementById('req-number'),
        special: document.getElementById('req-special'),
        match: document.getElementById('req-match')
    };

    const strengthBar = document.querySelector('.strength-meter-bar');
    const strengthText = document.querySelector('.strength-meter-text');

    const validations = {
        length: val => val.length >= 8,
        lower: val => /[a-z]/.test(val),
        upper: val => /[A-Z]/.test(val),
        number: val => /[0-9]/.test(val),
        special: val => /[^A-Za-z0-9]/.test(val)
    };

    const strengthLevels = {
        0: { text: 'Fortaleza', class: '' },
        1: { text: 'Muy Débil', class: 'strength-20' },
        2: { text: 'Débil', class: 'strength-40' },
        3: { text: 'Buena', class: 'strength-60' },
        4: { text: 'Fuerte', class: 'strength-80' },
        5: { text: 'Excelente', class: 'strength-100' }
    };

    function checkFormValidity() {
        const allValid = Object.values(requirements).every(el => el && el.classList.contains('valid'));
        submitButton.disabled = !allValid;
    }

    function validatePassword() {
        const password = newPasswordInput.value;
        let score = 0;

        // Valida cada requisito y actualiza la lista en la UI.
        for (const key in validations) {
            const requirementElement = requirements[key];
            // Se añade una comprobación para asegurar que el elemento del requisito existe antes de manipularlo.
            if (requirementElement) {
                if (validations[key](password)) {
                    requirementElement.classList.add('valid');
                    score++;
                } else {
                    requirementElement.classList.remove('valid');
                }
            }
        }

        // Actualiza la barra de fortaleza, comprobando si los elementos existen.
        if (strengthBar) {
            strengthBar.className = 'strength-meter-bar'; // Resetea las clases de fortaleza.
            if (password.length > 0) {
                const level = strengthLevels[score];
                if (level && level.class) {
                    strengthBar.classList.add(level.class);
                }
                if (strengthText && level) {
                    strengthText.textContent = level.text;
                }
            } else {
                if (strengthText) {
                    strengthText.textContent = 'Fortaleza';
                }
            }
        }

        // Vuelve a comprobar si las contraseñas coinciden.
        validatePasswordMatch();
    }

    function validatePasswordMatch() {
        const password = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const matchElement = requirements.match;

        // Se añade una comprobación para asegurar que el elemento de coincidencia existe.
        if (matchElement) {
            if (confirmPassword.length > 0 && password === confirmPassword) {
                matchElement.classList.add('valid');
            } else {
                matchElement.classList.remove('valid');
            }
        }
        // Después de cada validación, comprobamos si el formulario es válido para activar/desactivar el botón.
        checkFormValidity();
    }

    // --- Event Listeners ---
    newPasswordInput.addEventListener('input', validatePassword);
    confirmPasswordInput.addEventListener('input', validatePasswordMatch);

    // --- Lógica para mostrar/ocultar contraseña ---
    const toggleButtons = document.querySelectorAll('.toggle-password');
    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetInputId = button.dataset.target;
            const targetInput = document.getElementById(targetInputId);
            if (targetInput) {
                const type = targetInput.getAttribute('type') === 'password' ? 'text' : 'password';
                targetInput.setAttribute('type', type);
                // Cambia el ícono para dar feedback.
                button.textContent = type === 'password' ? '👁️' : '🙈';
            }
        });
    });

    // Ejecutar una vez al cargar por si el navegador autocompleta los campos.
    validatePassword();
});