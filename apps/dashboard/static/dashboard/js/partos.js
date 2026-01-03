window.renderKpiParto1 = function () {
    const el = document.getElementById("kpi_parto_1");
    if (!el) return;

    const valor = el.dataset.value || 10;
    el.innerHTML = valor;
};

window.renderKpiParto2 = function () {
    const el = document.getElementById("kpi_parto_2");
    if (!el) return;

    const valor = el.dataset.value || 15;
    el.innerHTML = String(valor) + '%';
};

window.renderKpiParto3 = function () {
    const el = document.getElementById("kpi_parto_3");
    if (!el) return;
    const valor = el.dataset.value || 15;
    el.innerHTML = valor;
};

/* helper para color segun tema */
function getChartTextColor() {
    return document.body.classList.contains('dark') ? '#ffffff' : '#000000';
}



/* graficos */
window.renderChartParto1 = function () {
    const div = document.getElementById("chart_parto_1");
    if (!div) return;

    val1= `["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]`
    val2 = `[10,20,30,50,100,400,200,150,300,250,350,450]`

    const meses = JSON.parse(div.dataset.meses || val1);
    const valores = JSON.parse(div.dataset.values || val2);

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
            type: "scatter",
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

window.renderChartParto2 = function () {
    const div = document.getElementById("chart_parto_2");
    if (!div) return;

    // categorías y valores (permitir override desde dataset)
    let categorias = ["Partos", "Cesareas"];
    let valores = [40, 60]; // por defecto: Partos 40%, Cesareas 60%

    try {
        categorias = JSON.parse(div.dataset.valY || div.dataset.meses || JSON.stringify(categorias));
    } catch (e) { /* keep default */ }

    try {
        valores = JSON.parse(div.dataset.values || JSON.stringify(valores));
    } catch (e) { /* keep default */ }

    const chart = echarts.init(div);

    const palette = ['#FAA18F', '#F863A8', '#C83737', '#DD7EB1'];
    const textColor = getChartTextColor();

    const option = {
        textStyle: { color: textColor },
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            formatter: params => {
                const p = params[0];
                return `${p.name}<br/>${p.seriesName}: ${p.data}%`;
            }
        },
        legend: { textStyle: { color: textColor } },
        xAxis: {
            type: 'value',
            min: 5,
            max: 100,
            axisLabel: { color: textColor, formatter: v => `${v}%` }
        },
        yAxis: { type: 'category', data: categorias, axisLabel: { color: textColor } },
        series: [
            {
                name: 'Porcentaje',
                type: 'bar',
                barWidth: 24,
                label: { show: true, position: 'right', color: textColor, formatter: v => `${v.value}%` },
                emphasis: { focus: 'series' },
                data: valores,
                itemStyle: {
                    color: function(params) {
                        return palette[params.dataIndex % palette.length];
                    }
                }
            }
        ],
        color: palette
    };

    chart.setOption(option);
    chart.resize();
};

window.renderChartParto3 = function () {
    const div = document.getElementById("chart_parto_3");
    if (!div) return;

    val1= `["Hemorragia", "Preeclampsia", "Infección", "Parto Prematuro", "Otros"]`
    val2=  `[15, 8, 12, 5, 10]`

    const labels = JSON.parse(div.dataset.labels || val1);
    const values = JSON.parse(div.dataset.values || val2);

    const chart = echarts.init(div);

    const palette = ['#e67475', '#5470C6', '#91CC75', '#FAC858', '#73C0DE'];
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
window.renderTableParto = function () {
    const tbody = document.getElementById("tabla_parto");
    if (!tbody) return;

    const rows=  '[{"Profesional":"Dr. Juan Perez","TipoParto":"Natural","HoraParto":"14:30"},{"Profesional":"Dra. Maria Gomez","TipoParto":"Cesárea","HoraParto":"09:15"},{"Profesional":"Dr. Carlos Ruiz","TipoParto":"Natural","HoraParto":"22:45"}]'

    let tabla = [];
    try {
        tabla = JSON.parse(tbody.dataset.value || rows);
    } catch (e) {
        console.error('Error parseando tabla_parto dataset:', e);
        tabla = [];
    }

    // limpiar contenido previo
    tbody.innerHTML = '';

    tabla.forEach(parto => {
        const row = document.createElement("tr");

        const cellProfesional = document.createElement("td");
        cellProfesional.textContent = parto.Profesional;
        row.appendChild(cellProfesional);

        const cellTipoParto = document.createElement("td");
        cellTipoParto.textContent = parto.TipoParto;
        row.appendChild(cellTipoParto);

        const cellHoraParto = document.createElement("td");
        cellHoraParto.textContent = parto.HoraParto;
        row.appendChild(cellHoraParto);

        tbody.appendChild(row);
    });
};
