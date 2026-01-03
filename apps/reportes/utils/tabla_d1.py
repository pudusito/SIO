import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo



# =====================================================================================
# FUNCIÓN PARA CREAR LA TABLA D.1 EN MEMORIA (BUFFER)
# =====================================================================================
def crear_tabla_d1_buffer(total_rn, rn_menor_500, rn_500_999, rn_1000_1499, rn_1500_1999, rn_2000_2499, rn_2500_2999, rn_3000_3999, rn_4000, rn_con_anomalia_congenita, start_date, end_date):

    # Cargamos estilos base (Title, Normal, etc.)
    styles = getSampleStyleSheet()

    # =====================================================================================
    # DEFINICIÓN DE ESTILOS PERSONALIZADOS PARA CELDAS Y ENCABEZADOS
    # =====================================================================================

    # Estilo para celdas del cuerpo (datos)
    cell_center = ParagraphStyle(
        "cell_center",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    # Estilo para encabezados (texto blanco sobre fondo rojo)
    header_center = ParagraphStyle(
        "header_center",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    descripcion_rango_fechas = ParagraphStyle(
        "descripcion_rango_fechas",
        fontSize=12,
        leading=8,
        alignment=TA_CENTER
    )

    # =====================================================================================
    # DATOS DE LA TABLA — EXACTOS AL EXCEL
    # =====================================================================================

    encabezado = [
        "TIPO","TOTAL","Menos de 500","500 a 999","1.000 a 1.499",
        "1.500 a 1.999","2.000 a 2.499","2.500 a 2.999",
        "3.000 a 3.999","4.000 y más","Anomalía Congénita"
    ]

    fila_datos = [
        "NACIDOS VIVOS", total_rn, rn_menor_500, rn_500_999, rn_1000_1499, rn_1500_1999, rn_2000_2499, rn_2500_2999, rn_3000_3999, rn_4000, rn_con_anomalia_congenita
    ]

    # Convertimos cada celda a Paragraph
    encabezado = [Paragraph(str(x), header_center) for x in encabezado]
    fila_datos = [Paragraph(str(x), cell_center) for x in fila_datos]

    # =====================================================================================
    # 1. Crear un buffer en memoria donde se guardará el PDF
    # =====================================================================================
    buffer = io.BytesIO()

    # =====================================================================================
    # 2. Crear el documento PDF usando el buffer (NO archivo físico)
    # =====================================================================================
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)

    story = []  # Contenedor de elementos del PDF


    story.extend(construir_header_logo())

    # =====================================================================================
    # 3. AGREGAR TÍTULO SUPERIOR
    # =====================================================================================

    story.append(Paragraph(
        "<b>SECCIÓN D.1: INFORMACIÓN GENERAL DE RECIÉN NACIDOS VIVOS</b> "
        "<b>''REM A 24''</b>",
        styles["Title"]
    ))
    

    texto = f"Desde {start_date}" if start_date else "" + f" - Hasta {end_date}" if end_date else ""
    texto_decorado = "<p>" + texto + "</p>"

    story.append(Paragraph(
        texto_decorado,
        descripcion_rango_fechas, 
    ))

    story.append(Spacer(1, 12))

    # =====================================================================================
    # 4. CREAR TABLA
    # =====================================================================================

    tabla = [encabezado, fila_datos]

    # Ancho total para mantener proporción exacta
    ancho_total = 540
    col = ancho_total / len(encabezado)

    t = Table(tabla, colWidths=[col] * len(encabezado))

    # =====================================================================================
    # 5. ESTILOS VISUALES DE LA TABLA
    # =====================================================================================

    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(0xE63137)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),

        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(t)

    # =====================================================================================
    # 6. Generar PDF dentro del buffer
    # =====================================================================================
    pdf.build(story)

    # Rebobinar buffer al inicio
    buffer.seek(0)

    # =====================================================================================
    # 7. Devolver buffer para que Django lo envíe por FileResponse
    # =====================================================================================
    return buffer




# SOLO PARA PRUEBA LOCAL SIN DJANGO
if __name__ == "__main__":
    buffer_pdf = crear_tabla_d1_buffer()
    with open("tabla_d1_buffer.pdf", "wb") as f:
        f.write(buffer_pdf.read())
    print("PDF generado correctamente.")
