window.renderKpiRn1 = function () {
    const el = document.getElementById("kpi_rn_1");
    if (!el) return;

    const valor = el.dataset.value || 10;
    el.innerHTML = valor;
};

window.renderKpiRn2 = function () {
    const el = document.getElementById("kpi_rn_2");
    if (!el) return;

    const valor = el.dataset.value || 30;
    el.innerHTML = valor;
};

window.renderKpiRn3= function () {
    const el = document.getElementById("kpi_rn_3");
    if (!el) return;
    const valor = el.dataset.value || 15;
    el.innerHTML = valor;
};

/* helper para color segun tema */
function getChartTextColor() {
    return document.body.classList.contains('dark') ? '#ffffff' : '#000000';
}


/* gráficos */
window.renderChartRn1 = function () {
    const container = document.getElementById("chart_rn_1");
    if (!container) return;

    const chart = echarts.init(container);

    const labels = [
        'Complicaciones Neonatales',
        'Sin Complicaciones',
        'Ingreso UCI Neonatal',
    ];

    const values = [
        458,
        735,
        135,
    ];

    const chartData = labels.map((name, index) => ({
        name,
        value: values[index]
    }));

    const palette = ['#b37183', '#caa843', '#661518'];
    
    const option = {
        tooltip: { trigger: 'item' },
        legend: {
            bottom: '0%',
            left: 'center'
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '42%'],
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2,
                color: function(params) {
                    return palette[params.dataIndex % palette.length];
                }
            },
            label: { show: false },
            emphasis: {
                label: {
                    show: false,
                    fontSize: 16,
                    fontWeight: 'bold'
                }
            },
            labelLine: { show: false },
            data: chartData
        }]
    };

    chart.setOption(option);
    chart.resize();
};


window.renderChartRn2 = function () {
    const div = document.getElementById("chart_rn_2");
    if (!div) return;

    const meses = JSON.parse(div.dataset.meses || `["0","1","2","3","4","5"]`);
    const valores = JSON.parse(div.dataset.values || `["10","7","9","4","7","3"]`);

    const chart = echarts.init(div);

    const palette = ['#e67475', '#5470C6', '#91CC75', '#EE6666', '#FAC858'];
    const textColor = getChartTextColor();

    const option = {
        textStyle: { color: textColor },
        tooltip: { trigger: "axis", textStyle: { color: textColor } },
        xAxis: { type: "category", data: meses, axisLabel: { color: textColor } },
        yAxis: { type: "value", axisLabel: { color: textColor } },
        series: [{
            type: "line",
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

window.renderChartRn3 = function () {
    const div = document.getElementById("chart_rn_3");
    if (!div) return;

    const defaultLabels = ['Reanimación avanzada', 'Complicaciones Respiratorias', 'Infecciones Neonatales', 'Hipoglicemia', 'Ictericia'];
    const defaultValues = [89.3, 57.1, 74.4, 50.1, 89.7];

    const labels = JSON.parse(div.dataset.labels || JSON.stringify(defaultLabels));
    const values = JSON.parse(div.dataset.values || JSON.stringify(defaultValues));

    const chart = echarts.init(div);

    const palette = ['#EE6666', '#5470C6', '#91CC75', '#FAC858', '#73C0DE'];
    const textColor = getChartTextColor();

    const option = {
        textStyle: { color: textColor },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: { type: 'value', axisLabel: { color: textColor } },
        yAxis: { type: 'category', data: labels, axisLabel: { color: textColor }, inverse: true },
        visualMap: {
            show: false,
            min: Math.min(...values),
            max: Math.max(...values),
            dimension: 1,
            inRange: { color: palette }
        },
        series: [{
            type: 'bar',
            data: values,
            itemStyle: {
                color: (params) => palette[params.dataIndex % palette.length]
            },
            label: { show: true, position: 'right', color: textColor }
        }]
    };

    chart.setOption(option);
    chart.resize();
};



/* tabla */
window.renderTableRn = function () {
    const tbody = document.getElementById("tabla_rn");
    if (!tbody) return;

    let tabla = [];
    try {
        tabla = JSON.parse(tbody.dataset.value || '[{"NombreRN":"Ana Perez","Peso":2800,"EdadGestacional":38,"Apgar":"8/10","Reanimacion":"Si"}]');
    } catch (e) {
        console.error('Error parseando tabla_rn dataset:', e);
        tabla = [];
    }

    tbody.innerHTML = '';

    tabla.forEach(rn => {
        const row = document.createElement("tr");

        const cellNombreRN = document.createElement("td");
        cellNombreRN.textContent = rn.NombreRN;
        row.appendChild(cellNombreRN);

        const cellPeso = document.createElement("td");
        cellPeso.textContent = rn.Peso;
        row.appendChild(cellPeso);

        const cellEdadGestacional = document.createElement("td");
        cellEdadGestacional.textContent = rn.EdadGestacional;
        row.appendChild(cellEdadGestacional);

        const cellApgar = document.createElement("td");
        cellApgar.textContent = rn.Apgar;
        row.appendChild(cellApgar);

        const cellReanimacion = document.createElement("td");
        cellReanimacion.textContent = rn.Reanimacion;
        row.appendChild(cellReanimacion);

        tbody.appendChild(row);
    });
};
