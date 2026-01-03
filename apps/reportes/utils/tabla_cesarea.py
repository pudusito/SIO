import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from apps.reportes.utils.pdf_header import construir_header_logo












# =====================================================================================
# FUNCION PARA CREAR LA TABLA EN MEMORIA (BUFFER)
# =====================================================================================
def crear_tabla_cesarea_buffer(cesarea_electiva_total):
        # Cargamos estilos por defecto como Title, Normal, etc.
    styles = getSampleStyleSheet()
    # =====================================================================================
    # DEFINICIÓN DE ESTILOS PERSONALIZADOS PARA CELDAS Y ENCABEZADOS
    # =====================================================================================
    # Estilo para celdas con números (centrados)
    cell_center = ParagraphStyle(
        "cell_center",
        fontSize=8,       # Tamaño similar a Excel
        leading=10,       # Altura de línea
        alignment=TA_CENTER
    )

    hneader_center = ParagraphStyle(
        "header_center",
        fontSize=9,       # Un poco más grande que las celdas normales
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    # =====================================================================================
    # DATOS DE LA TABLA - ENCABEZADOS  
    # =====================================================================================
    # Encabezado principal dividido en dos grupos: URGENCIA Y ELECTIVA
    encabezado = [
        Paragraph("<b>URGENCIA</b>", hneader_center), 
        Paragraph("<b>ELECTIVA</b>", hneader_center)
    ]


    # FILA DE DATOS (11 FILAS)
    datos_brutos = [
        [0,cesarea_electiva_total],
        [0,0],
        [0,0],
        [0,0],
        [0,0],
        [5,2],
        [0,0],
        [5,2],
        [0,0],
        [0,0],
        [0,0],
    ]

    # convertimos los datos en Paragraphs para evitar problemas de formato
    filas_datos = [
        [Paragraph(str(celda), cell_center) for celda in fila]
        for fila in datos_brutos
    ]
    # 1. Creamos un buffer de memoria para almacenar el PDF binario
    buffer = io.BytesIO()

    # 2. Creamos el SimpleDocTemplate usando el buffer como "nombre de archivo"
    pdf = SimpleDocTemplate(buffer, pagesize=letter, topMargin=30)

    story = []

    story.extend(construir_header_logo())


    # titulo de la seccion
    story.append(Paragraph("<b>CESAREA</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    #====================================================================================
    # CREACIÓN DE LA TABLA
    #====================================================================================

    tabla =  [encabezado] + filas_datos

    #definir ancho de columnas
    colWidths=[80, 80 ]
    
    #crear tabla con sus columnas
    t = Table(tabla, colWidths=colWidths)

    #====================================================================================
    # ESTILO DE LA TABLA
    #====================================================================================

    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.orange),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ("GRID", (0,0), (-1,-1), 1, colors.black),  
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,5), (-1,5), colors.red), # Fila 5 (índice 5 de filas_datos + fila 0 de encabezado = fila 6, índice 5)
        ("BACKGROUND", (0,7), (-1,7), colors.red),
    ]))

    story.append(t)

    # 3. Generar el PDF, escribiéndolo en el buffer
    pdf.build(story)
    
    # 4. Es crucial "rebobinar" el buffer al inicio antes de leer su contenido
    buffer.seek(0)
    
    # 5. Devolvemos el buffer que contiene el PDF
    return buffer


# protege que si se importa como modulo no se ejecute y genere un archivo
if __name__ == "__main__":
    pdf_buffer = crear_tabla_cesarea_buffer()
    
    # Si quieres guardarlo para probar (en lugar de enviarlo por Django)
    with open("tabla_cesarea_buffer.pdf", "wb") as f:
        f.write(pdf_buffer.read())
        
    print("PDF de la tabla de cesáreas generado exitosamente en el buffer y guardado para prueba.")