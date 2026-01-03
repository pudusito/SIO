/* kpi */
window.renderKpiPaciente1 = function () {
    const el = document.getElementById("kpi_paciente_1");
    if (!el) return;

    const valor = el.dataset.value || 0;
    el.innerHTML = valor;
};


window.renderKpiPaciente2 = function () {
    const el = document.getElementById("kpi_paciente_2");
    if (!el) return;

    const valor = el.dataset.value || 0;
    el.innerHTML = valor;
};



window.renderKpiPaciente3 = function () {
    const el = document.getElementById("kpi_paciente_3");
    if (!el) return;
    
    const valor = el.dataset.value || 0;
    el.innerHTML = valor;;
};

/* helper para color segun tema */
function getChartTextColor() {
    return document.body.classList.contains('dark') ? '#ffffff' : '#000000';
}

/* graficos */
window.renderChartPaciente1 = function () {
    const div = document.getElementById("chart_paciente_1");
    if (!div) return;

    val1= `["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]`
    val2= div.dataset.value.split(",")

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
            type: "bar", /* AQUI CAMBIAMOS EL TIPO DE GRAFICO */
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

window.renderChartPaciente2 = function () {
    const div = document.getElementById("chart_paciente_2");
    if (!div) return;

    val1= `["18-25","26-35","36-45","56+"]`
    val2= div.dataset.value.split(',')
    console.log(val2)

    const meses = JSON.parse(div.dataset.meses || val1);
    const valores = JSON.parse(div.dataset.value || val2);

    const chart = echarts.init(div);

    const palette = ['#FAA18F', '#F863A8', '#C83737', '#DD7EB1'];
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

// PONE COMENTARIOS DE QUE HACE CADA COSA PARA NO TENER QUE IR ARCHIVO EN ARCHIVO
window.renderChartPaciente3 = function () {
    const div = document.getElementById("chart_paciente_3");
    if (!div) return;

    const chart = echarts.init(div);

    val1= ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
    val2= [3,5,8,10,13,15,18,20]
    
    const palette = ['#EE6666', '#5470C6', '#91CC75', '#FAC858', '#73C0DE'];
    const textColor = getChartTextColor();

    const option = {
          textStyle: { color: textColor },
          tooltip: { textStyle: { color: textColor } },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: val1,
            axisLabel: { color: textColor }
          },
          yAxis: {
            type: 'value',
            axisLabel: { color: textColor }
          },
          series: [
            {
              data: val2,
              type: 'line',
              areaStyle: {},
              lineStyle: { color: palette[0] },
              itemStyle: { color: palette[0] }
            }
          ],
          color: palette
        };
    chart.setOption(option);
    chart.resize();
};




// /* tabla con maximo 10 pacientes */
// window.renderTablePaciente = function () {
//     const tbody = document.getElementById("tabla_paciente");
//     if (!tbody) return;

//     let tabla = [];
//     try { /* Aqui debemos agregar el valor que definiremos abajo */
//          /* recordar poner la comillas y sin espacios al inyectar datos en bruto*/
//         tabla = JSON.parse(tbody.dataset.value.split(',') || '[{"nombre":"Ana Perez","edad":28},{"nombre":"Maria Gomez","edad":32}, {"nombre":"Luisa Fernandez","edad":45},{"nombre":"Carmen Rodriguez","edad":36},{"nombre":"Sofia Martinez","edad":29},{"nombre":"Elena Lopez","edad":40},{"nombre":"Marta Sanchez","edad":33}]');
//     } catch (e) {
//         console.error('Error parseando tabla_pacientes dataset:', e);
//         tabla = [];
//     }

//     // limpiar contenido previo
//     tbody.innerHTML = '';


//     tabla.forEach(paciente => {
//         const row = document.createElement("tr");

//         /* nombre tabla = para json */
//         const cellNombre = document.createElement("td");
//         cellNombre.textContent = paciente.nombre || paciente.nombre || ''; /* se puede validar */
//         row.appendChild(cellNombre);

//         /* edad */
//         const cellEdad = document.createElement("td");
//         cellEdad.textContent = paciente.edad;
//         row.appendChild(cellEdad);

//         tbody.appendChild(row);
//     });
// };
