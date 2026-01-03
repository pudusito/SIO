import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo



# =====================================================================================
# FUNCIÓN PARA GENERAR LA TABLA EN MEMORIA (BUFFER)
# =====================================================================================
def crear_tabla_hepatitis_b_buffer():

    # =================================================================
    # 1. ESTILOS
    # =================================================================
    styles = getSampleStyleSheet()

    cell = ParagraphStyle(
        "cell",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    header = ParagraphStyle(
        "header",
        fontSize=7,
        leading=8,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    titulo_seccion = ParagraphStyle(
        "titulo_seccion",
        fontSize=15,
        leading=24,
        alignment=1,  # centrado
        textColor=colors.HexColor("#000000"),
        spaceAfter=12
    )


    # =================================================================
    # 2. ENCABEZADOS Y FILAS
    # =================================================================
    encabezado = [
        Paragraph("Total", header),
        Paragraph("Pueblos Originarios", header),
        Paragraph("Migrantes", header),
    ]

    fila_1 = ["0", "0", "0"]
    fila_2 = ["0", "0", "0"]

    fila_1 = [Paragraph(str(x), cell) for x in fila_1]
    fila_2 = [Paragraph(str(x), cell) for x in fila_2]


    desc_1 = Paragraph(
        "Recién nacidos hijos de madre Hepatitis B positiva, nacidos en el periodo",
        cell
    )

    desc_2 = Paragraph(
        "Recién nacidos hijos de madre Hepatitis B positiva que recibieron profilaxis completa, según la normativa vigente",
        cell
    )


    # =================================================================
    # 3. ARMAR TABLA COMPLETA
    # =================================================================
    tabla = [
        ["", encabezado[0], encabezado[1], encabezado[2]],
        [desc_1, fila_1[0], fila_1[1], fila_1[2]],
        [desc_2, fila_2[0], fila_2[1], fila_2[2]],
    ]

    col_widths = [260, 70, 70, 70]


    # =================================================================
    # 4. CREAR BUFFER
    # =================================================================
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)

    story = []

    story.extend(construir_header_logo())

    # TÍTULO
    story.append(Paragraph(
        "<b>SECCIÓN J: PROFILAXIS DE TRANSMISIÓN VERTICAL APLICADA AL RECIÉN NACIDO, "
        "HIJO DE MADRE HEPATITIS B POSITIVA</b> <b>''REM A 11''</b>",
        titulo_seccion
    ))
    story.append(Spacer(1, 12))


    # =================================================================
    # 5. CREAR OBJETO TABLA
    # =================================================================
    t = Table(tabla, colWidths=col_widths)

    t.setStyle(TableStyle([

        ("BACKGROUND", (1,0), (-1,0), colors.limegreen),

        ("GRID", (0,0), (-1,-1), 1, colors.black),

        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))

    story.append(t)

    # =================================================================
    # 6. GENERAR PDF EN BUFFER
    # =================================================================
    pdf.build(story)
    buffer.seek(0)

    return buffer



# =====================================================================================
# PRUEBA LOCAL OPCIONAL
# =====================================================================================
if __name__ == "__main__":
    buf = crear_tabla_hepatitis_b_buffer()
    with open("tabla_hepatitis_b_buffer.pdf", "wb") as f:
        f.write(buf.read())
    print("PDF generado correctamente.")
