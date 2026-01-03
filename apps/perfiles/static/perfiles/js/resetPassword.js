// ==== Mostrar/Ocultar contraseña ====
document.querySelectorAll(".toggle-password").forEach(btn => {
    btn.addEventListener("click", () => {
        const input = document.getElementById(btn.dataset.target);

        input.type = input.type === "password" ? "text" : "password";
        btn.classList.toggle("active");
    });
});

// ==== Validación en vivo ====
const pw1 = document.getElementById("new-password");
const pw2 = document.getElementById("confirm-password");
const errorBox = document.getElementById("reset-error");

function validate() {
    // Si uno está vacío → no mostrar nada todavía
    if (!pw1.value || !pw2.value) {
        pw1.classList.remove("error", "success");
        pw2.classList.remove("error", "success");
        errorBox.style.display = "none";
        return;
    }

    // Si coinciden → verde
    if (pw1.value === pw2.value) {
        pw1.classList.add("success");
        pw2.classList.add("success");
        pw1.classList.remove("error");
        pw2.classList.remove("error");
        errorBox.style.display = "none";
    }

    // Si NO coinciden → rojo
    else {
        pw1.classList.add("error");
        pw2.classList.add("error");
        pw1.classList.remove("success");
        pw2.classList.remove("success");
        errorBox.style.display = "block";
    }
}

pw1.addEventListener("input", validate);
pw2.addEventListener("input", validate);
