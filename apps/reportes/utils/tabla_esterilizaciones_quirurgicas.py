import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo



# =====================================================================================
# FUNCIÓN PARA GENERAR LA TABLA *EN BUFFER* PARA USO CON DJANGO
# =====================================================================================
def crear_tabla_esterilizaciones_buffer():

    # ============================================================
    # 1. ESTILOS
    # ============================================================
    styles = getSampleStyleSheet()

    cell_center = ParagraphStyle(
        "cell_center",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER
    )

    header_center = ParagraphStyle(
        "header_center",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    # ============================================================
    # 2. ENCABEZADOS (2 NIVELES)
    # ============================================================

    # NIVEL SUPERIOR (fila 0)
    encabezado_superior = [
        Paragraph("<b>SEXO</b>", header_center),
        Paragraph("<b>TOTAL</b>", header_center),
        Paragraph("<b>EDAD (en años)</b>", header_center),
        "",
        "",
        Paragraph("<b>Trans</b>", header_center),
        "",
    ]

    # NIVEL INFERIOR (fila 1)
    encabezado_inferior = [
        "",
        "",
        Paragraph("<b>Menor<br/>de 20 años</b>", header_center),
        Paragraph("<b>20 - 34 años</b>", header_center),
        Paragraph("<b>35 y más años</b>", header_center),
        Paragraph("<b>Masculino</b>", header_center),
        Paragraph("<b>Femenino</b>", header_center),
    ]

    # ============================================================
    # 3. FILAS DE DATOS
    # ============================================================

    datos = [
        ["MUJER", "33", "0", "19", "14", "0", "0"],
        ["HOMBRE", "0", "0", "0", "0", "0", "0"],
    ]

    filas_datos = [
        [Paragraph(str(x), cell_center) for x in fila]
        for fila in datos
    ]

    # ============================================================
    # 4. CREAR BUFFER
    # ============================================================
    buffer = io.BytesIO()

    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)
    story = []

    story.extend(construir_header_logo())

    # ============================================================
    # 5. TÍTULO DEL REPORTE
    # ============================================================
    story.append(
        Paragraph("<b>SECCIÓN G: ESTERILIZACIONES QUIRÚRGICAS</b>", styles["Title"])
    )
    story.append(Spacer(1, 12))

    # ============================================================
    # 6. ARMADO DE TABLA COMPLETA
    # ============================================================

    tabla = [
        encabezado_superior,
        encabezado_inferior,
    ] + filas_datos

    col_widths = [80, 60, 80, 80, 80, 80, 80]

    t = Table(tabla, colWidths=col_widths)

    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),     # Primera fila
        ("BACKGROUND", (0, 1), (-1, 1), colors.lightgreen),    # Segunda fila
        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        # FUSIONES DE CELDAS
        ("SPAN", (2, 0), (4, 0)),  # EDAD (en años)
        ("SPAN", (5, 0), (6, 0)),  # Trans

        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(t)

    # ============================================================
    # 7. CONSTRUIR PDF EN MEMORIA
    # ============================================================
    pdf.build(story)

    buffer.seek(0)   # Rebobinar

    return buffer



# =====================================================================================
# SOLO PARA PRUEBAS LOCALES
# =====================================================================================
if __name__ == "__main__":
    buf = crear_tabla_esterilizaciones_buffer()
    with open("tabla_esterilizaciones_buffer.pdf", "wb") as f:
        f.write(buf.read())
    print("PDF generado correctamente.")
