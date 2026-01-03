document.addEventListener("DOMContentLoaded", function () {
    const timerSpan = document.getElementById("timer");
    if (!timerSpan) return;

    // Obtiene texto tipo "02:15"
    let [min, sec] = timerSpan.textContent.trim().split(":").map(Number);
    let totalSeconds = min * 60 + sec;

    function updateTimer() {
        if (totalSeconds <= 0) {
            timerSpan.textContent = "00:00";
            timerSpan.style.color = "red";
            timerSpan.parentNode.innerHTML += "<br><a href=''>Solicitar nuevo codigo</a>";
            return;
        }

        totalSeconds--;

        const m = String(Math.floor(totalSeconds / 60)).padStart(2, "0");
        const s = String(totalSeconds % 60).padStart(2, "0");

        timerSpan.textContent = `${m}:${s}`;

        setTimeout(updateTimer, 1000);
    }

    updateTimer();
});