import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo



# =====================================================================================
# FUNCIÓN PARA GENERAR PDF EN BUFFER
# =====================================================================================
def crear_tabla_modelo_atencion_buffer(espontaneo: dict, 
                                       inducidos: dict, 
                                       conduccion_oxitocica: dict, 
                                       libertad_movimiento: dict,
                                       regimen_hidrico_amplio: dict,
                                       analgesias: dict,
                                       posiciones: dict,
                                       episiotomia: dict,
                                       acompaniamiente: dict):

    # ------------------ ESTILOS ------------------
    styles = getSampleStyleSheet()

    cell_left = ParagraphStyle(
        "cell_left",
        fontSize=7,
        leading=9,
        alignment=TA_LEFT
    )

    cell_center = ParagraphStyle(
        "cell_center",
        fontSize=7,
        leading=9,
        alignment=TA_CENTER
    )

    header_center = ParagraphStyle(
        "header_center",
        fontSize=8,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.black
    )


    # ------------------ ENCABEZADO ------------------
    encabezado = [
        "",
        Paragraph("<b>TOTAL</b>", header_center),
        Paragraph("<b>&lt;28 semanas</b>", header_center),
        Paragraph("<b>28 a 37 semanas</b>", header_center),
        Paragraph("<b>38 semanas y más</b>", header_center),
    ]


    # ------------------ TABLA COMPLETA ------------------
    tabla = [
        encabezado,

        [
            Paragraph("ESPONTANEO", cell_left), 
            espontaneo.get('total'), 
            espontaneo.get('28_sem'), 
            espontaneo.get('28_37_sem'),
            espontaneo.get('partos_38_sem')],

        [Paragraph("INDUCIDOS", cell_left), "", "", "", ""],
        ["      MECÁNICA", 
            inducidos.get('mecanicamente').get('total'), 
            inducidos.get('mecanicamente').get('28_sem'),  
            inducidos.get('mecanicamente').get('28_37_sem'), 
            inducidos.get('mecanicamente').get('partos_38_sem')],
        ["      FARMACOLÓGICA", 
            inducidos.get('farmacologicamente').get('total'), 
            inducidos.get('farmacologicamente').get('28_sem'), 
            inducidos.get('farmacologicamente').get('28_37_sem'), 
            inducidos.get('farmacologicamente').get('partos_38_sem')],

        [Paragraph("CONDUCCIÓN OXITÓCICA", cell_left), 
         conduccion_oxitocica.get('total'), 
         conduccion_oxitocica.get('28_sem'), 
         conduccion_oxitocica.get('28_37_sem'), 
         conduccion_oxitocica.get('partos_38_sem')],

        [Paragraph("LIBERTAD DE MOVIMIENTO", cell_left), 
         libertad_movimiento.get('total'), 
         libertad_movimiento.get('28_sem'), 
         libertad_movimiento.get('28_37_sem'), 
         libertad_movimiento.get('partos_38_sem')],

        [Paragraph("RÉGIMEN HÍDRICO AMPLIO", cell_left), 
         regimen_hidrico_amplio.get('total'), 
         regimen_hidrico_amplio.get('28_sem'), 
         regimen_hidrico_amplio.get('28_37_sem'), 
         regimen_hidrico_amplio.get('partos_38_sem')],

        [Paragraph("Manejo del dolor", cell_left), "", "", "", ""],
        ["      No farmacológico", 
         analgesias.get('no_farmacologico').get('total'), 
         analgesias.get('no_farmacologico').get('28_sem'), 
         analgesias.get('no_farmacologico').get('28_37_sem'), 
         analgesias.get('no_farmacologico').get('partos_38_sem')],
        ["      Farmacológico", 
         analgesias.get('farmacologico').get('total'), 
         analgesias.get('farmacologico').get('28_sem'), 
         analgesias.get('farmacologico').get('28_37_sem'), 
         analgesias.get('farmacologico').get('partos_38_sem')],

        [Paragraph("POSICIÓN AL MOMENTO DEL EXPULSIVO", cell_left), "", "", "", ""],
        ["      LITOTOMÍA", 
         posiciones.get('litotomia').get('total'), 
         posiciones.get('litotomia').get('28_sem'), 
         posiciones.get('litotomia').get('28_37_sem'), 
         posiciones.get('litotomia').get('partos_38_sem')],
        ["      OTRAS POSICIONES",
         posiciones.get('otras').get('total'), 
         posiciones.get('otras').get('28_sem'), 
         posiciones.get('otras').get('28_37_sem'), 
         posiciones.get('otras').get('partos_38_sem')],

        [Paragraph("EPISIOTOMIA", cell_left), 
        episiotomia.get('total'), 
         episiotomia.get('28_sem'), 
         episiotomia.get('28_37_sem'), 
         episiotomia.get('partos_38_sem')],

        [Paragraph("ACOMPAÑAMIENTO", cell_left), "", "", "", ""],
        ["      DURANTE EL TRABAJO DE PARTO",
        acompaniamiente.get('trabajo_parto').get('total'), 
         acompaniamiente.get('trabajo_parto').get('28_sem'), 
         acompaniamiente.get('trabajo_parto').get('28_37_sem'), 
         acompaniamiente.get('trabajo_parto').get('partos_38_sem')],
        ["      SOLO EN EL EXPULSIVO", 
        acompaniamiente.get('expulsivo').get('total'), 
         acompaniamiente.get('expulsivo').get('28_sem'), 
         acompaniamiente.get('expulsivo').get('28_37_sem'), 
         acompaniamiente.get('expulsivo').get('partos_38_sem')],
    ]


    # ------------------ ANCHOS DE COLUMNA ------------------
    col_widths = [250, 60, 70, 70, 70]


    # ------------------ CREAR BUFFER ------------------
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)

    story = []

    story.extend(construir_header_logo())

    # TÍTULO
    story.append(
        Paragraph("<b>CARACTERISTICAS DEL MODELO DE ATENCIÓN</b>", styles["Title"])
    )
    story.append(Spacer(1, 10))


    # ------------------ TABLA REPORTLAB ------------------
    t = Table(tabla, colWidths=col_widths)

    t.setStyle(TableStyle([
        ("BACKGROUND", (1, 0), (-1, 0), colors.lightblue),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(t)

    # Construir PDF
    pdf.build(story)
    buffer.seek(0)

    return buffer



# -----------------------------------------------------------------------
# PRUEBA LOCAL OPCIONAL
# -----------------------------------------------------------------------
if __name__ == "__main__":
    buf = crear_tabla_modelo_atencion_buffer()
    with open("tabla_modelo_atencion_buffer.pdf", "wb") as f:
        f.write(buf.read())
    print("PDF generado correctamente.")
