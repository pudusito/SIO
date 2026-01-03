window.renderKpiProfesional1 = function () {
    const el = document.getElementById("kpi_profesional_1");
    if (!el) return;

    const valor = el.dataset.value || 10;
    el.innerHTML = valor;
};

window.renderKpiProfesional2 = function () {
    const el = document.getElementById("kpi_profesional_2");
    if (!el) return;

    const valor = el.dataset.value || 30;
    el.innerHTML = valor;
};


/* helper para color segun tema */
function getChartTextColor() {
    return document.body.classList.contains('dark') ? '#ffffff' : '#000000';
}


window.renderChartProfesional1 = function () {
    const div = document.getElementById("chart_profesional_1");
    if (!div) return;

    const meses = JSON.parse(div.dataset.meses || `["Matrona","Medico obstetra", "Enfermera", "Anestesista", "Pediatra"]`);
    const valores = JSON.parse(div.dataset.values || `[6, 4, 6, 3, 2]`);

    const chart = echarts.init(div);

    const palette = ['#73C0DE', '#5470C6', '#91CC75', '#EE6666', '#FAC858'];
    const textColor = getChartTextColor();

    const option = {
        textStyle: { color: textColor },
        tooltip: { trigger: "axis", textStyle: { color: textColor } },
        xAxis: { type: "category", data: meses, axisLabel: { color: textColor } },
        yAxis: { type: "value", axisLabel: { color: textColor } },
        series: [{
            type: "bar",
            data: valores,
            center: ['50%', '50%'], //centra el grafico
            itemStyle: {
                color: function(params) {
                    return palette[params.dataIndex % palette.length];
                }
            },
            label: {
                show: true,
                position: 'top',
                color: textColor
            }
        }],
        legend: { textStyle: { color: textColor } },
        color: palette
    };

    chart.setOption(option);
    chart.resize();
};


/* tabla */
window.renderTableProfesional = function () {
    const tbody = document.getElementById("tabla_profesional");
    if (!tbody) return;

    let tabla = [];
    try {
        tabla = JSON.parse(tbody.dataset.value || '[{"Nombre":"Dr. Juan","Area":"Pabellon","Especialidad":"Matron"}]');
    } catch (e) {
        console.error('Error parseando tabla_profesional dataset:', e);
        tabla = [];
    }

    tbody.innerHTML = '';

    tabla.forEach(profesional => {
        const row = document.createElement("tr");

        const cellNombre = document.createElement("td");
        cellNombre.textContent = profesional.Nombre;
        row.appendChild(cellNombre);

        const cellArea = document.createElement("td");
        cellArea.textContent = profesional.Area;
        row.appendChild(cellArea);

        const cellEspecialidad = document.createElement("td");
        cellEspecialidad.textContent = profesional.Especialidad;
        row.appendChild(cellEspecialidad);

        tbody.appendChild(row);
    });
};
