import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo


# =====================================================================================
# FUNCIÓN PARA CREAR LA TABLA D.2 EN BUFFER
# =====================================================================================
def crear_tabla_d2_buffer():

    # Cargamos estilos básicos (Title, Normal, Heading...)
    styles = getSampleStyleSheet()

    # =================================================================================
    # DEFINICIÓN DE ESTILOS PERSONALIZADOS PARA CELDAS
    # =================================================================================

    cell_center = ParagraphStyle(
        "cell_center",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    header_top = ParagraphStyle(
        "header_top",
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


    header_sub = ParagraphStyle(
        "header_sub",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    # =================================================================================
    # DATOS DEL ENCABEZADO NIVEL 1 (fila superior)
    # =================================================================================

    encabezado_n1 = [
        "TIPO",
        "PROFILAXIS", "PROFILAXIS",
        "TIPO DE PARTO", "TIPO DE PARTO", "TIPO DE PARTO", "TIPO DE PARTO"
        "APGAR", "APGAR",
        "Reanimación Básica",
        "Reanimación Avanzada",
        "EHI Grado II y III",
    ]

    # =================================================================================
    # DATOS DEL ENCABEZADO NIVEL 2 (fila inferior)
    # =================================================================================

    encabezado_n2 = [
        "",
        "Hepatitis B",
        "Ocular",
        "Parto Vaginal",
        "Parto Instrumental",
        "Cesárea",
        "Parto extrahospitalario",
        "Apgar ≤ 3 al minuto",
        "Apgar ≤ 6 a los 5 minutos",
        "",
        "",
    ]

    # Convertir a Paragraph
    encabezado_n1 = [Paragraph(x, header_top) for x in encabezado_n1]
    encabezado_n2 = [Paragraph(x, header_sub) for x in encabezado_n2]

    # =================================================================================
    # FILA PRINCIPAL DE DATOS
    # =================================================================================

    fila = [
        "NACIDOS VIVOS",
        143, 143, 73, 4, 66, 0, 3, 3, 16, 6, ""
    ]

    fila = [Paragraph(str(x), cell_center) for x in fila]

    # =================================================================================
    # TABLA SECUNDARIA (PARTOS DISTÓCICOS, VACUUM, ETC.)
    # =================================================================================

    tabla_inferior = [
        ["DISTOCICO", Paragraph("1", cell_center)],
        ["VACUUM", Paragraph("3", cell_center)],
        ["C. URGENCIA", Paragraph("39", cell_center)],
        ["C. ELECTIVA", Paragraph("27", cell_center)],
        ["TOTAL DE PARTOS", Paragraph("143", cell_center)],
    ]

    # =================================================================================
    # 1. Crear buffer en memoria para guardar el PDF
    # =================================================================================

    buffer = io.BytesIO()

    # =================================================================================
    # 2. Crear documento PDF usando el buffer
    # =================================================================================

    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)

    story = []  # Contenedor de elementos del PDF


    story.extend(construir_header_logo())

    # =================================================================================
    # 3. Título del documento
    # =================================================================================

    story.append(Paragraph(
        "<b>SECCIÓN D.2: ATENCIÓN INMEDIATA DEL RECIÉN NACIDO</b><br/>"
        "<b>''REM A 24''</b>",
        styles["Title"]
    ))

    story.append(Spacer(1, 12))

    # =================================================================================
    # 4. TABLA PRINCIPAL (encabezado 1 + encabezado 2 + fila)
    # =================================================================================

    tabla_principal = [
        encabezado_n1,
        encabezado_n2,
        fila
    ]

    ancho_total = 540
    col = ancho_total / len(encabezado_n1)

    t1 = Table(tabla_principal, colWidths=[col] * len(encabezado_n1))

    t1.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor(0xE63137)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), 
        ("BACKGROUND", (0,1), (-1,1), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))

    story.append(t1)

    story.append(Spacer(1, 30))

    # =================================================================================
    # 5. TABLA INFERIOR
    # =================================================================================

    t2 = Table(tabla_inferior, colWidths=[200, 80])

    t2.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    story.append(t2)

    # =================================================================================
    # 6. Construir PDF dentro del buffer
    # =================================================================================

    pdf.build(story)

    buffer.seek(0)  # Rebobinar

    return buffer




# SOLO PARA PRUEBAS LOCALES SIN DJANGO
if __name__ == "__main__":
    buf = crear_tabla_d2_buffer()
    with open("tabla_d2_buffer.pdf", "wb") as f:
        f.write(buf.read())
    print("PDF generado correctamente.")
