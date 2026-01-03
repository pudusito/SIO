const dbMock = {
            hasPuerperio: false,
            participantes: [
                { nombre: "Dr. Juan Pérez", cargo: "Ginecólogo" },
                { nombre: "Mat. Ana Gómez", cargo: "Matrona" }
            ],
            recienNacidos: []
        };

        document.addEventListener('DOMContentLoaded', () => {
            renderPuerperio();
            renderParticipantes();
            renderRecienNacidos();
        });

        function renderPuerperio() {
            const container = document.getElementById('content-puerperio');
            if (dbMock.hasPuerperio) {
                container.innerHTML = `
                    <div class="detalle-grid-3">
                         <div class="dato-box"><span class="dato-label">Periné</span><span class="dato-valor">Intacto</span></div>
                         <div class="dato-box"><span class="dato-label">Sangrado</span><span class="dato-valor">Normal</span></div>
                    </div>
                    <div style="text-align:right; margin-top:1rem;">
                        <button class="btn-secondary">Editar Puerperio</button>
                    </div>`;
            } else {
                container.innerHTML = `
                    <div style="text-align: center; padding: 1.5rem;">
                        <p style="color:var(--text-muted); margin-bottom:1rem;">Sin registro de puerperio.</p>
                        <button class="btn-primary" onclick="simularGuardado('puerperio')">Registrar Puerperio</button>
                    </div>`;
            }
        }

        function renderParticipantes() {
            const container = document.getElementById('content-participantes');
            if (dbMock.participantes.length > 0) {
                let html = '<ul class="lista-clean">';
                dbMock.participantes.forEach(p => {
                    html += `<li><span class="dato-valor">${p.nombre}</span><span class="stat-label">${p.cargo}</span></li>`;
                });
                html += '</ul><div style="text-align:right; margin-top:1rem;"><button class="btn-secondary" onclick="simularGuardado(\'participante\')">Gestionar Equipo</button></div>';
                container.innerHTML = html;
            } else {
                 container.innerHTML = `<div style="text-align:center; padding:1.5rem;"><button class="btn-primary" onclick="simularGuardado('participante')">Asignar Equipo</button></div>`;
            }
        }

        function renderRecienNacidos() {
             const container = document.getElementById('content-rn');
             if (dbMock.recienNacidos.length > 0) {
                // ... lógica similar ...
             } else {
                container.innerHTML = `
                    <div style="text-align: center; padding: 1.5rem;">
                        <p style="color:var(--text-muted); margin-bottom:1rem;">No hay recién nacidos registrados.</p>
                        <button class="btn-primary" onclick="simularGuardado('rn')">Registrar Nacimiento</button>
                    </div>`;
             }
        }

        function simularGuardado(tipo) {
            if(confirm("¿Simular guardado y recarga?")) {
                if(tipo === 'puerperio') dbMock.hasPuerperio = true;
                if(tipo === 'participante') dbMock.participantes.push({nombre: "Nuevo", cargo: "TENS"});
                renderPuerperio(); renderParticipantes(); renderRecienNacidos();
                alert("Guardado. Datos actualizados.");
            }
        }

        function confirmarEliminacion() {
            if(confirm("¿Estás seguro de que deseas eliminar este parto? Esta acción no se puede deshacer.")) {
                alert("Registro eliminado (Simulación)");
                // window.location.href = 'lista_partos.html';
            }
        }