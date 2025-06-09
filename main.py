from src.config_modifier import leer_json, incrementar_version

data = leer_json("config.json")
print(data)

numero_version = incrementar_version("config.json")
print(f"Nueva versión: {numero_version}")
