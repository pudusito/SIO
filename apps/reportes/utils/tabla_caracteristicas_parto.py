import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo




# ====================================================================================
# FUNCIÓN PARA GENERAR TABLA "CARACTERÍSTICAS DEL PARTO" EN MEMORIA (BUFFER)
# ====================================================================================

def crear_tabla_caracteristicas_parto_buffer(
    total_partos,
    vaginal,
    instrumental,
    cesarea_electiva,
    cesarea_urgencia
):
    """
    Genera la tabla CARACTERISTICAS DEL PARTO como PDF en memoria.
    Retorna un buffer BytesIO listo para enviar por HTTP.
    """

    # ======================================================
    # 1. Estilos básicos y personalizados
    # ======================================================
    styles = getSampleStyleSheet()

    cell_left = ParagraphStyle(
        "cell_left",
        fontSize=8,
        leading=10,
        alignment=TA_LEFT
    )

    cell_center = ParagraphStyle(
        "cell_center",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER
    )

    header_center = ParagraphStyle(
        "header_center",
        fontSize=10,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    # ======================================================
    # 2. Creamos BUFFER de memoria (NO archivo físico)
    # ======================================================
    buffer = io.BytesIO()

    # SimpleDocTemplate recibe el buffer en lugar de un archivo
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)
    story = []

    story.extend(construir_header_logo())

    # ======================================================
    # 3. TÍTULO
    # ======================================================
    story.append(
        Paragraph("<b>CARACTERISTICAS DEL PARTO</b> <b>''REM A24''</b>",
                  styles["Title"])
    )
    story.append(Spacer(1, 10))


    # ======================================================
    # 4. Encabezados de la tabla
    # ======================================================
    encabezado_1 = Paragraph("<b>CARACTERISTICAS DEL PARTO</b>", header_center)

    encabezado_2 = Paragraph(
        "Lactancia materna en los primeros<br/>"
        "60 minutos de vida (RN con peso<br/>"
        "de 2.500 grs. o más)",
        header_center
    )


    # ======================================================
    # 5. Contenido dinámico de la tabla (datos entregados por parámetros)
    # ======================================================
    tabla = [
        [encabezado_1, encabezado_2],
        [Paragraph("TOTAL PARTOS", cell_left), Paragraph(str(total_partos), cell_center)],
        [Paragraph("VAGINAL", cell_left), Paragraph(str(vaginal), cell_center)],
        [Paragraph("INSTRUMENTAL", cell_left), Paragraph(str(instrumental), cell_center)],
        [Paragraph("CESÁREA ELECTIVA", cell_left), Paragraph(str(cesarea_electiva), cell_center)],
        [Paragraph("CESÁREA URGENCIA", cell_left), Paragraph(str(cesarea_urgencia), cell_center)],
    ]

    col_widths = [300, 200]

    t = Table(tabla, colWidths=col_widths)

    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(0xE63137)),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(t)


    # ======================================================
    # 6. Finalizar PDF dentro del buffer
    # ======================================================
    pdf.build(story)

    # MUY importante: rebobinar buffer para poder leerlo
    buffer.seek(0)

    # Retornamos el PDF en memoria
    return buffer



# ======================================================
# 7. Prueba local si se ejecuta directamente
# ======================================================
if __name__ == "__main__":

    pdf_buffer = crear_tabla_caracteristicas_parto_buffer(
        total_partos=122,
        vaginal=65,
        instrumental=0,
        cesarea_electiva=26,
        cesarea_urgencia=31
    )

    with open("tabla_caracteristicas_parto_buffer.pdf", "wb") as f:
        f.write(pdf_buffer.read())

    print("PDF de prueba generado correctamente usando buffer.")
