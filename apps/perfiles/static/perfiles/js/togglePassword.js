document.addEventListener("DOMContentLoaded", () => {
    const togglePassword = document.querySelector('#togglePassword');
    
    // CAMBIO AQUÍ: Django usa 'id_' como prefijo por defecto
    const passwordInput = document.querySelector('#id_password'); 
    
    const eyeIcon = document.querySelector('.eye-icon');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            // ... resto de tu código igual ...
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            if (type === 'text') {
                eyeIcon.style.opacity = "1";
                eyeIcon.style.color = "var(--primary)";
            } else {
                eyeIcon.style.opacity = "0.5";
                eyeIcon.style.color = ""; 
            }
        });
    }
});