# mi_proyecto_individual

# Informacion Personal

**Apellidos y nombres:** Choquechambi Quispe Germain Ronald

**Correo institucional** germain.choquechambi.q@uni.pe

**Titulo del proyecto:** Proyecto 10: "Pull requests y revisión de código Automatizada con Hooks y Linters"

**Grupo:** 6

**URL del repositorio grupa:** [PC3Proyecto10](https://github.com/OliverHz28/PC3Proyecto10.git)

# Sprint 1
## Mi rol
- Me encargue de implementar un sistema de validacion automatica para asegurar la calidad del codigo antes de realizar un commits o pushear. 
- Contribui añadiendo un script lint_all.sh y configurando los hooks pre-push y commit-msg para verificar el estilo del codigo y validar el formato de los mensajes de commit.

## Instrucciones para clonar el repositorio repositorio y reproducir la parte de mi codigo:

## 1. Clonar el repositorio
```
git clone https://github.com/GermainAN/Personal-Proyecto-10.git
```

## 2. preparar el entorno virutal

```
python3 -m venv pc3
```
```
source pc3/bin/activate
```
## 3. Instalar herramientas de análisis
instalar flake8 para analizar el codigo python
```
pip install flake8
```

instalar shellcheck para analizar scrips bash
```
sudo apt update && sudo apt install shellcheck
```

instalar tflint para analizar el codigo terraform
```
curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
```

## 4. Copiar los hooks personalizados a la carpeta `.git/hooks`

```
cp hooks/commit-msg .git/hooks/commit-msg
```


```
cp hooks/pre-push .git/hooks/
```

## 5. Dar permisos de ejecucion a los hooks y al script de linting
```
chmod +x .git/hooks/commit-msg
```
```
chmod +x lint_all.sh
```
```
chmod +x .git/hooks/pre-push
```