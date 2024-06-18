# Password Manager

Este es un gestor de contraseñas simple que permite almacenar y recuperar contraseñas cifradas para diferentes servicios.

## Requisitos

- Python 3.6 o superior
- Bibliotecas adicionales:
  - `cryptography`
  - `argparse` (usualmente incluida en la biblioteca estándar de Python)

Puedes instalar las dependencias necesarias ejecutando:

```sh
pip install -r requirements.txt
```

## Uso

### Añadir una contraseña

```sh
python main.py add <servicio> <usuario> <contraseña> <clave_maestra>
```

Ejemplo:

```sh
python main.py add facebook john_doe password123 mymasterkey
```

### Obtener una contraseña

```sh
python main.py get <servicio> <clave_maestra>
```

Ejemplo:

```sh
python main.py get facebook mymasterkey
```

### Listar todos los servicios

```sh
python main.py list
```

### Eliminar todas las contraseñas

```sh
python main.py drop
```

## Archivos

### `args.py`

Contiene la función `getArgs` que maneja los argumentos de la línea de comandos.

### `Passgen.py`

Contiene la clase `Passgen` que maneja la lógica de cifrado, descifrado, almacenamiento y recuperación de contraseñas.

### `main.py`

Archivo principal que ejecuta las operaciones según los argumentos proporcionados.

## Estructura del proyecto

```plaintext
├── gestor_contraseñas_env/
├── .env
├── .gitignore
├── args.py
├── main.py
├── Passgen.py
├── passwords.json
├── README.md
└── requirements.txt
```

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
