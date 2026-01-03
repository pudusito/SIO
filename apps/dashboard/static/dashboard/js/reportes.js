window.renderKpiReporte1 = function () {
    const el = document.getElementById("kpi_reporte_1");
    if (!el) return;

    const valor = el.dataset.value || 10;
    el.innerHTML = valor;
};

window.renderKpiReporte2 = function () {
    const el = document.getElementById("kpi_reporte_2");
    if (!el) return;

    const valor = el.dataset.value || 30;
    el.innerHTML = valor;
};

window.renderKpiReporte3 = function () {
    const el = document.getElementById("kpi_reporte_3");
    if (!el) return;
    const valor = el.dataset.value || 15;
    el.innerHTML = valor;
};

/* helper para color segun tema */
function getChartTextColor() {
    return document.body.classList.contains('dark') ? '#ffffff' : '#000000';
}


/* graficos */
window.renderChartReporte1 = function () {
    const div = document.getElementById("chart_reporte_1");
    if (!div) return;

    const meses = JSON.parse(div.dataset.meses || `["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]`);
    const valores = JSON.parse(div.dataset.values || `[10,20,30,50,100]`);

    const chart = echarts.init(div);

    const palette = ['#5470C6', '#91CC75', '#EE6666', '#FAC858', '#73C0DE', '#3BA272', '#E062AE'];
    const textColor = getChartTextColor();

    const option = {
        textStyle: { color: textColor },
        tooltip: { 
            trigger: "axis",
            textStyle: { color: textColor }
        },
        xAxis: { type: "category", data: meses, axisLabel: { color: textColor } },
        yAxis: { type: "value", axisLabel: { color: textColor } },
        series: [{
            type: "bar",
            data: valores,
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

window.renderChartReporte2 = function () {
    const div = document.getElementById("chart_reporte_2");
    if (!div) return;

    const meses = JSON.parse(div.dataset.meses || `["Ene","Feb","Mar"]`);
    const valores = JSON.parse(div.dataset.values || `[10,20,30]`);

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

window.renderChartReporte3 = function () {
    const div = document.getElementById("chart_reporte_3");
    if (!div) return;

    const labels = JSON.parse(div.dataset.labels || `["Hemorragia", "Preeclampsia", "Infección", "reporte Prematuro", "Otros"]`);
    const values = JSON.parse(div.dataset.values || `[15, 8, 12, 5, 10]`);

    const chart = echarts.init(div);

    const palette = ['#EE6666', '#5470C6', '#91CC75', '#FAC858', '#73C0DE'];
    const textColor = getChartTextColor();

    const pieData = labels.map((name, i) => ({ value: values[i] || 0, name }));

    const option = {
        textStyle: { color: textColor },
        tooltip: { trigger: 'item', textStyle: { color: textColor } },
        legend: { orient: 'vertical', left: 'left', textStyle: { color: textColor } },
        color: palette,
        series: [
          {
            name: 'Complicaciones',
            type: 'pie',
            radius: '50%',
            data: pieData,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            label: {
              formatter: '{b}: {c} ({d}%)',
              color: textColor
            }
          }
        ]
    };
    chart.setOption(option);
    chart.resize();
};




/* tabla */
window.renderTableReporte = function () {
    const tbody = document.getElementById("tabla_reporte");
    if (!tbody) return;

    let tabla = [];
    try {
        tabla = JSON.parse(tbody.dataset.value || '[{"Profesional":"Dr. Jose","NombreRN":"Ana","TipoReporte":"Cesarea","Apgar":8}]');
    } catch (e) {
        console.error('Error parseando tabla_reporte dataset:', e);
        tabla = [];
    }

    tbody.innerHTML = '';

    tabla.forEach(reporte => {
        const row = document.createElement("tr");

        const cellProfesional = document.createElement("td");
        cellProfesional.textContent = reporte.Profesional;
        row.appendChild(cellProfesional);

        const cellNombreRN = document.createElement("td");
        cellNombreRN.textContent = reporte.NombreRN;
        row.appendChild(cellNombreRN);

        const cellTipoReporte = document.createElement("td");
        cellTipoReporte.textContent = reporte.TipoReporte;
        row.appendChild(cellTipoReporte);

        const cellApgar = document.createElement("td");
        cellApgar.textContent = reporte.Apgar;
        row.appendChild(cellApgar);

        tbody.appendChild(row);
    });
};
