from reportlab.platypus import Image, Spacer, Table, TableStyle
from django.conf import settings
import os

def construir_header_logo(ancho_minsal=90, ancho_hospital=260):
    """
    Header institucional:
    - Logo MINSAL alineado totalmente a la IZQUIERDA
    - Logo Herminda Martín CENTRADO simétricamente
    - Columna derecha vacía para mantener el centro real
    """

    # ==============================
    # RUTAS A LAS IMÁGENES
    # ==============================
    ruta_minsal = os.path.join(settings.BASE_DIR, "static", "images", "minsal.png")
    ruta_hospital = os.path.join(settings.BASE_DIR, "static", "images", "HermindaMartin.png")

    # ==============================
    # CARGAR Y ESCALAR LOGO MINSAL
    # ==============================
    img_left = Image(ruta_minsal)

    factor_left = ancho_minsal / float(img_left.drawWidth)
    img_left.drawWidth = ancho_minsal
    img_left.drawHeight = img_left.drawHeight * factor_left

    # ==============================
    # CARGAR Y ESCALAR LOGO HERMINDAMARTÍN
    # ==============================
    img_center = Image(ruta_hospital)

    factor_center = ancho_hospital / float(img_center.drawWidth)
    img_center.drawWidth = ancho_hospital
    img_center.drawHeight = img_center.drawHeight * factor_center

    # ==============================
    # TABLA DE 3 COLUMNAS PARA CENTRAR
    # ==============================
    tabla_logos = Table(
        [[img_left, img_center, ""]],  # celda derecha vacía = equilibrio visual
        colWidths=[ancho_minsal + 30, ancho_hospital + 30, ancho_minsal + 30]
    )

    tabla_logos.setStyle(TableStyle([
        ("ALIGN", (0,0), (0,0), "LEFT"),       # logo MINSAL a la izquierda
        ("ALIGN", (1,0), (1,0), "CENTER"),     # logo Herminda Martín centrado
        ("ALIGN", (2,0), (2,0), "RIGHT"),      # celda vacía, pero alineada
        ("VALIGN", (0,0), (-1,-1), "TOP"),     # ambos logos arriba
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))

    # ==============================
    # RETORNAR EL HEADER FINAL
    # ==============================
    return [
        Spacer(1, 5),       # espacio superior suave y profesional
        tabla_logos,        # logos alineados
        Spacer(1, 20),      # espacio antes del título principal
    ]
