import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo


# =====================================================================================
# FUNCIÓN PARA CREAR EL PDF EN MEMORIA (BUFFER) PARA DJANGO
# =====================================================================================
def crear_tabla_eutocico_distocico_buffer():

    # ---------------------------------------------------------
    # 1. ESTILOS
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # 2. ENCABEZADOS SUPERIOR E INFERIOR
    # ---------------------------------------------------------
    encabezado_superior = [
        Paragraph("<b>EUTÓCICO</b>", header_center), "", "",
        Paragraph("<b>DISTÓCICO</b>", header_center), "", ""
    ]

    encabezado_inferior = [
        Paragraph("<b>&lt;28 semanas</b>", header_center),
        Paragraph("<b>28 a 37 semanas</b>", header_center),
        Paragraph("<b>38 semanas y más</b>", header_center),
        Paragraph("<b>&lt;28 semanas</b>", header_center),
        Paragraph("<b>29 a 37 semanas</b>", header_center),
        Paragraph("<b>39 semanas y más</b>", header_center),
    ]

    # ---------------------------------------------------------
    # 3. DATOS (13 filas)
    # ---------------------------------------------------------
    datos_brutos = [
        [1,19,35,0,1,1],
        [0,0,0,0,0,0],
        [0,4,15,0,0,1],
        [1,19,48,0,1,2],
        [1,19,45,0,1,1],
        [0,16,40,0,1,2],
        [0,10,29,0,0,1],
        [0,9,28,0,0,2],
        [1,19,35,0,1,1],
        [0,"","",0,"",""],
        [0,0,0,0,0,0],
        [0,19,45,0,0,2],
        [0,22,46,0,0,2],
    ]

    filas_datos = [
        [Paragraph(str(x), cell_center) for x in fila]
        for fila in datos_brutos
    ]

    # ---------------------------------------------------------
    # 4. CREAR BUFFER
    # ---------------------------------------------------------
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)
    story = []

    story.extend(construir_header_logo())

    # ---------------------------------------------------------
    # 5. TÍTULO
    # ---------------------------------------------------------
    story.append(
        Paragraph(
            "<b>EUTÓCICO vs DISTÓCICO</b> <b>''REM A21''</b>",
            styles["Title"]
        )
    )
    story.append(Spacer(1, 12))

    # ---------------------------------------------------------
    # 6. CONSTRUIR LA TABLA COMPLETA
    # ---------------------------------------------------------
    tabla = [
        encabezado_superior,
        encabezado_inferior,
    ] + filas_datos

    colWidths = [90, 90, 90, 90, 90, 90]

    t = Table(tabla, colWidths=colWidths)

    # ---------------------------------------------------------
    # 7. ESTILOS DE LA TABLA
    # ---------------------------------------------------------
    t.setStyle(TableStyle([

        # Fondo para encabezado superior
        ("BACKGROUND", (0,0), (2,0), colors.lightgrey),
        ("BACKGROUND", (3,0), (5,0), colors.lightgrey),

        # Fondo encabezado inferior
        ("BACKGROUND", (0,1), (-1,1), colors.khaki),

        # Grid general
        ("GRID", (0,0), (-1,-1), 1, colors.black),

        # Alinear verticalmente
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

        # SPANS
        ("SPAN", (0,0), (2,0)),  # EUTÓCICO
        ("SPAN", (3,0), (5,0)),  # DISTÓCICO

        # FILA 9 con fondo rojo (índice contando desde 0)
        ("BACKGROUND", (0,9), (-1,9), colors.red),
    ]))

    story.append(t)

    # ---------------------------------------------------------
    # 8. CONSTRUIR PDF DENTRO DEL BUFFER
    # ---------------------------------------------------------
    pdf.build(story)
    buffer.seek(0)

    return buffer



# =====================================================================================
# PRUEBA LOCAL OPCIONAL
# =====================================================================================
if __name__ == "__main__":
    buf = crear_tabla_eutocico_distocico_buffer()
    with open("tabla_eutocico_distocico_buffer.pdf", "wb") as f:
        f.write(buf.read())
    print("PDF generado correctamente.")
