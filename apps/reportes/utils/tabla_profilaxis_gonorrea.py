import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo



# =====================================================================================
# FUNCIÓN PARA CREAR EL PDF EN BUFFER (LISTO PARA DJANGO)
# =====================================================================================
def crear_tabla_profilaxis_gonorrea_buffer():
    
    styles = getSampleStyleSheet()

    # ---------------- ESTILOS ----------------
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
        alignment=1,
        textColor=colors.black,
        spaceAfter=12
    )

    # ---------------- ENCABEZADO ----------------
    encabezado = [
        Paragraph("Total", header),
        Paragraph("Pueblos Originarios", header),
        Paragraph("Migrantes", header),
    ]

    # ---------------- FILAS DE DATOS ----------------
    fila_1 = [Paragraph("143", cell), Paragraph("0", cell), Paragraph("7", cell)]
    fila_2 = [Paragraph("143", cell), Paragraph("0", cell), Paragraph("7", cell)]

    # ---------------- DESCRIPCIONES ----------------
    desc_1 = Paragraph(
        "Recién Nacidos vivos que reciben profilaxis ocular para gonorrea al nacer",
        cell
    )

    desc_2 = Paragraph(
        "Recién nacidos vivos",
        cell
    )

    # ---------------- CONSTRUIR TABLA ----------------
    tabla = [
        ["", encabezado[0], encabezado[1], encabezado[2]],
        [desc_1, fila_1[0], fila_1[1], fila_1[2]],
        [desc_2, fila_2[0], fila_2[1], fila_2[2]],
    ]

    # ---------------- ANCHOS ----------------
    col_widths = [260, 70, 70, 70]

    # ---------------- CREAR BUFFER ----------------
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)

    story = []

    story.extend(construir_header_logo())

    # ---------------- TÍTULO ----------------
    story.append(Paragraph(
        "<b>SECCIÓN D: APLICACIÓN DE PROFILAXIS OCULAR PARA GONORREA EN RECIÉN NACIDOS</b> "
        "<b>''REM A 11''</b>",
        titulo_seccion
    ))

    story.append(Spacer(1, 12))  # espacio


    # ---------------- TABLA ----------------
    t = Table(tabla, colWidths=col_widths)

    t.setStyle(TableStyle([
        ("BACKGROUND", (1, 0), (-1, 0), colors.salmon),
        ("TEXTCOLOR", (1, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(t)

    # ---------------- GENERAR PDF ----------------
    pdf.build(story)
    buffer.seek(0)

    return buffer



# ---------------- PRUEBA LOCAL ----------------
if __name__ == "__main__":
    pdf_buffer = crear_tabla_profilaxis_gonorrea_buffer()
    with open("tabla_profilaxis_gonorrea_buffer.pdf", "wb") as f:
        f.write(pdf_buffer.read())
    print("PDF generado correctamente.")
