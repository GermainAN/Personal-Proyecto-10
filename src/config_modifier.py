import json
import os


def leer_json(file_path):
    """
    Lee el archivo JSON desde el sistema de archivos y
    devuelve su contenido como un diccionario
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No existe el archivo '{file_path}'")

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"El archivo '{file_path}' no contiene un JSON válido")


def incrementar_version(file_path):
    """
    Incrementa el campo "version" del archivo JSON
    """

    config = leer_json(file_path)

    if "version" not in config:
        raise KeyError("No existe el campo 'version' en el archivo JSON")

    if not isinstance(config['version'], (int, float)):
        raise TypeError("El campo 'version' no es un número")

    config["version"] += 1
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    return config["version"]
