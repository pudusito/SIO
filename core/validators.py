from django.core.exceptions import ValidationError

def validar_rut(value: str):
    """
    Valida un RUT chileno usando el algoritmo oficial módulo 11.
    Se usa en Forms, ModelForms y Modelos (validators=[...]).
    """

    if not value:
        return 

    rut = value.replace(".", "").replace("-", "").upper()

    if len(rut) < 7:
        return (False, "El RUT debe tener al menos 7 dígitos en la parte numérica.")


    cuerpo = rut[:-1]
    dv_ingresado = rut[-1]

    if not cuerpo.isdigit():
        return (False, "El RUT debe contener solo números en la parte del cuerpo.")

    # Cálculo del DV
    mult = 2
    suma = 0

    for d in reversed(cuerpo):
        suma += int(d) * mult
        mult += 1
        if mult > 7:
            mult = 2

    dv_calculado = 11 - (suma % 11)

    if dv_calculado == 11:
        dv_calculado = "0"
    elif dv_calculado == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(dv_calculado)

    # Comparación final
    if dv_ingresado != dv_calculado:
        return (False, f"El RUT ingresado no es válido. DV Incorrecto")

    return (True, 'Rut Valido')