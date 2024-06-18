import sys
import string
from random import randint, choice

def generate_password(length: int = 16, special_chars: bool = True) -> str:
    """
    La función generate_password() genera una contraseña aleatoria de una longitud determinada. Esta contraseña no generará contraseñas con secuencias de caracteres repetidos, como 'aaaaaa' o '123456' o '12345678', etc. Using ASCCI

    Args:
        length (int): longitud de la contraseña esperada
        special_chars (bool): si se deben incluir caracteres especiales en la contraseña

    Returns:
        password (str): contraseña generada (sin caracteres repetidos)
    """
    password = ''

    while len(password) < length:
        # Generar un caracter aleatorio
        if special_chars:
            char = chr(randint(33, 126))
        else:
            sequence = [randint(48, 57), randint(65, 90), randint(97, 122)] # Números, letras mayúsculas y minúsculas
            char = chr(choice(sequence))

        # Comprobar si el caracter ya está en la contraseña
        if char not in password:
            password += char

    return password


def calcular_tiempo_descifrado(contrasena: str) -> tuple:
    """
    La función calcular_tiempo_descifrado() calcula el tiempo necesario para descifrar una contraseña mediante un ataque de fuerza bruta, tanto en un ordenador clásico como en un ordenador cuántico.

    Args:
        contrasena (str): contraseña a descifrar

    Returns:
        tiempo_clasico_horas (float): tiempo necesario para descifrar la contraseña en un ordenador clásico (horas)
        tiempo_cuantico_horas (float): tiempo necesario para descifrar la contraseña en un ordenador cuánt
    """
    alfabeto = string.ascii_letters + string.digits
    tamano_alfabeto = len(alfabeto)
    
    combinaciones_posibles = tamano_alfabeto ** len(contrasena)
    
    tiempo_clasico_segundos = (combinaciones_posibles / 2) / 1e9
    

    tiempo_cuantico_segundos = (combinaciones_posibles ** 0.5) / 1e6
    
    
    tiempo_clasico_horas = tiempo_clasico_segundos / 3600
    tiempo_cuantico_horas = tiempo_cuantico_segundos / 3600

    return tiempo_clasico_horas, tiempo_cuantico_horas
    

def validar_enteros(arg: str) -> bool:
    """
    La función validar_enteros() comprueba si un argumento es un número entero.

    Args:
        arg (str): argumento a comprobar

    Returns:
        bool: True si el argumento es un número entero, False en caso contrario
    """
    try:
        int(arg)
        return True
    except ValueError:
        return False
    
def validar_booleanos(arg: str) -> bool:
    """
    La función validar_booleanos() comprueba si un argumento es un booleano.

    Args:
        arg (str): argumento a comprobar

    Returns:
        bool: True si el argumento es un booleano, False en caso contrario.
    """
    return arg in ('0', '1')

def generar_booleano(arg: str) -> bool:
    """
    La función generar_booleano() convierte un argumento en un booleano.

    Args:
        arg (str): argumento a convertir

    Returns:
        bool: True si el argumento es '1', False si el argumento es '0', None en caso contrario.
    """
    return bool(int(arg)) if validar_booleanos(arg) else None


def main() -> None:
    """
    La función main() es la función principal del script. Se encarga de procesar los argumentos proporcionados por el usuario y de generar la contraseña.

    Args: None

    Returns: None
    """
    args = sys.argv

    first_argument: int = 16
    second_argument: bool = True

    if len(args) == 1:
        print("Uso: python generator.py <longitud> <caracteres_especiales>")
        print("Ejemplo: python generator.py 16 1")

    elif len(args) == 2: # Solo se proporcionó la longitud
        if validar_enteros(args[1]):
            first_argument = int(args[1])
            print(first_argument)

    elif len(args) == 3: # Se proporcionó la longitud y si se deben incluir caracteres especiales
        if validar_enteros(args[1]) and validar_booleanos(args[2]):
            first_argument = int(args[1])
            print(first_argument)
            second_argument = generar_booleano(args[2])
            print(second_argument)
    else:
        print("Demasiados argumentos proporcionados")
        print("Uso: python generator.py <longitud> <caracteres_especiales>")
        print("Ejemplo: python generator.py 16 1")

    contrasena = generate_password(first_argument, second_argument)
    print(f"\nContraseña generada: {contrasena}\n")

main()