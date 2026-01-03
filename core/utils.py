import random
import string
# secrets es mas seguro que random porque no usa la aletoridad a traves de una semilla
# si no que utiliza el generador de numeros aleatorios del S.O (como /dev/urandom en Linux o el CSRPG en Windows)
import secrets
from datetime import datetime

def generar_codigo_temporal():
    """
    Genera un código temporal único para pacientes sin documento.
    Ejemplo: TMP-2025-11-20-483920
    """
    fecha = datetime.now().strftime("%Y%m%d")
    rnd = random.randint(10000, 99999)
    return f"TMP-{fecha}-{rnd}"


def generar_password_aleatoria(max_length=15):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    new_password = [secrets.choice(caracteres) for _ in range(1, max_length + 1)]
    new_password = "".join(new_password)
    return new_password


if __name__ == '__main__':
    print(generar_password_aleatoria())