import pathlib

def addIgnorePath(path):
    # Buscar el archivo .gitignore
    gitignore = pathlib.Path('.gitignore')
    
    # Si no existe, crearlo
    if not gitignore.exists():
        gitignore.open('w').write(f"{path}\n")
    
    else:
        # Leer el archivo y comprobar si la ruta ya existe
        with gitignore.open('r') as file:
            lines = file.readlines()
            if path not in lines:
                lines.append(f"\n{path}\n")
        
        # Escribir el archivo
        with gitignore.open('w') as file:
            file.writelines(lines)