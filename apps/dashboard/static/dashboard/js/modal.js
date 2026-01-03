(() => {
    const openButtons = document.querySelectorAll('.open-modal');
    const modals = document.querySelectorAll('.modal');

    let activeModal = null;

    const openModal = (id) => {
        const modal = document.getElementById(id);
        if (!modal || modal === activeModal) return;

        // Cerrar otro modal si existe
        if (activeModal) closeModal(activeModal);

        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.classList.add('overflow-hidden');

        activeModal = modal;
    };

    const closeModal = (modal) => {
        if (!modal) return;

        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.classList.remove('overflow-hidden');

        activeModal = null;
    };

    // =========================
    // ABRIR
    // =========================
    openButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            openModal(btn.dataset.modal);
        });
    });

    // =========================
    // CERRAR
    // =========================
    modals.forEach(modal => {

        // Click en overlay
        modal.addEventListener('click', e => {
            if (e.target === modal) closeModal(modal);
        });

        // Botones cerrar
        modal.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => closeModal(modal));
        });
    });

    // =========================
    // ESC
    // =========================
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && activeModal) {
            closeModal(activeModal);
        }
    });
})();
