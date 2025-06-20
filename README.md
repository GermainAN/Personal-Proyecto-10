# **Sprint 2**
* **Nombre:** Choquechambi Quispe, Germain Ronald
* **Proyecto:**  Pull requests y revision de codigo Automatizada con Hooks y Linters **(Proyecto 10)**
* **Grupo:** #6
* **Repositorio del proyecto:** https://github.com/OliverHz28/PC3Proyecto10.git


* **Instrucciones:** 

```
git clone https://github.com/OliverHz28/PC3Proyecto10.git
```
## **Descripcion:**
Repositorio donde documento mis contribuciones al `Proyecto 10: Pull requests y revisión de código Automatizada con Hooks y Linters` en sus respectivas ramas.

#### Demostracion en video
[Sprint 2 (Dia 8: 17/06/2025) Grupo 6 Proyecto 10 ](https://www.youtube.com/watch?v=CXj9d7sZ-J0)
#### **Mi Rol**
  * Sprint 2: Me encargue de:
    * La simulacion del pull_request local en el workflow (`pr_validation.yaml`) con `act` ejecutandoce en un contenedor de docker.
    * La mejora del archivo `lint_all.sh` sobre el manejo de errores.
    * Extender el workflow de Actions para Pull Request usando `matrix strategy` en `pr_validation.yaml`.

    * Automatizar la validación de Pull Requests mediante el check_pr.py para que analice los archivos de la PR (título, changelog, commits), ejecute linters y tests, y genere un reporte pr_report.md con los resultados de la validacion

    ```
        .
        ├───.scripts/
                └── check_pr.py
        ├─── tests/
                └── tests_check_pr.py
    ```
## Contribucion (solo codigo):

* Configure el scripts `check_pr` para ejecutar el `act` localmente segun lo especificado en el [Issue #21](https://github.com/OliverHz28/PC3Proyecto10/issues/21)

```python
import os
import re
import sys
import subprocess
from typing import Tuple, List


# Valida el titulo del Pull Request verificando que el archivo correspondiente exista
# y que cumpla con el patron esperado
def validar_titulo(carpeta_pr: str) -> Tuple[bool, str]:
    pr_id = os.path.basename(carpeta_pr)
    archivo_titulo = os.path.join(carpeta_pr, f"pr_{pr_id}_title.txt")

    if not os.path.isfile(archivo_titulo):
        return False, f"FAIL: Falta el archivo {archivo_titulo}"

    titulo = open(archivo_titulo, encoding="utf-8").read().strip()

    if not titulo:
        return False, f"FAIL: El archivo {archivo_titulo} esta vacio"
    patron = re.compile(
        r"^(feat|fix|docs|style|refactor|perf|test|chore|merge|)\[#\d+\]: .+")
    if patron.match(titulo):
        return True, "OK"

    return False, f"FAIL: '{titulo}' no cumple con el formato requerido"


# Verifica que el archivo CHANGELOG.md contenga una seccion para el PR actual
def verificar_changelog(carpeta_pr: str) -> Tuple[bool, str]:

    archivo_changelog = "../CHANGELOG.md"

    if not os.path.isfile(archivo_changelog):
        return False, "FAIL: no existe CHANGELOG.md"

    contenido = open(archivo_changelog, encoding="utf-8").read()
    seccion_pr = f"## PR {os.path.basename(carpeta_pr)}"

    if seccion_pr in contenido:
        return True, "OK"

    return False, f"FAIL: No se encontro la seccion '{seccion_pr}'"


# Verifica que todos los commits en commits.txt sigan un patron
def validar_commits(carpeta_pr: str) -> Tuple[bool, List[str]]:
    archivo_commits = os.path.join(carpeta_pr, "commits.txt")
    if not os.path.isfile(archivo_commits):
        return False, ["no existe el archivo commits.txt"]

    incorrectos: List[str] = []
    patron = re.compile(
        r"^(feat|fix|docs|style|refactor|perf|test|chore|merge)\[#\d+\]: .+")

    for fila, commit in enumerate(open(archivo_commits, encoding="utf-8"), 1):
        if not patron.match(commit.strip()):
            incorrectos.append(f"fila {fila}: '{commit.strip()}'")

    return (len(incorrectos) == 0, incorrectos)


# Ejecuta el script lint_all.sh para validar la calidad del codigo
def ejecutar_lint() -> Tuple[bool, str]:
    try:
        resultado = subprocess.run(
            ["bash", "lint_all.sh"],
            capture_output=True,
            text=True)
        if resultado.returncode == 0:
            return True, resultado.stdout.strip()
        else:
            return False, resultado.stderr.strip() or resultado.stdout.strip()
    except FileNotFoundError:
        return False, "no existe el script lint_all.sh"


# ejecuta los tests usando pytest y devuelve el resultado
def ejecutar_tests() -> Tuple[bool, str]:
    try:
        resultado = subprocess.run(
            ["pytest", "--maxfail=1", "--disable-warnings", "-q"],
            capture_output=True,
            text=True
        )
        if resultado.returncode == 0:
            return True, resultado.stdout.strip()
        else:
            return False, resultado.stdout.strip() + "\n" + resultado.stderr.strip()
    except FileNotFoundError:
        return False, "No se encontro pytest"


# Genera el reporte de validacion del PR en formato Markdown
def generar_pr_repor(ruta_report: str, titulo, changelog, commits, lint, tests):
    with open(ruta_report, "w", encoding="utf-8") as f:
        f.write("# Informe de Validacion\n\n")
        f.write("## Titulo\n")
        f.write(f"{titulo[1]}\n\n")

        f.write("## Changelog\n")
        f.write(f"{changelog[1]}\n\n")

        f.write("## Commits\n")
        if commits[0]:
            f.write("OK\n\n")
        else:
            f.write("FAIL: Commits con errores de formato:\n")
            for error in commits[1]:
                f.write(f"- {error}\n")
            f.write("\n")

        f.write("## Lint\n")
        f.write(f"{'OK' if lint[0] else 'FAIL'}\n")
        f.write(f"```\n{lint[1]}\n```\n\n")

        f.write("## Tests\n")
        f.write(f"{'OK' if tests[0] else 'FAIL'}\n")
        f.write(f"```\n{tests[1]}\n```\n")


def main():
    ruta_base = "../pr_simulation"
    if not os.path.isdir(ruta_base):
        print("No existe la carpeta pr_simulation")
        sys.exit(1)
    # iteramos sobre cada carpeta de PR y lo valida
    for nombre_carpeta in sorted(os.listdir(ruta_base)):
        ruta_pr = os.path.join(ruta_base, nombre_carpeta)
        if not os.path.isdir(ruta_pr):
            continue

        print(f"\nValidando PR {nombre_carpeta}")

        titulo = validar_titulo(ruta_pr)
        changelog = verificar_changelog(ruta_pr)
        commits = validar_commits(ruta_pr)
        lint = ejecutar_lint()
        tests = ejecutar_tests()

        generar_pr_repor(
            os.path.join(ruta_pr, "pr_report.md"),
            titulo,
            changelog,
            commits,
            lint,
            tests
        )
    # indica donde se guardo el pr_report.md
        print("pr_report.md generado en:", os.path.join(ruta_pr, "pr_report.md"))


if __name__ == "__main__":
    main()
            
```

#

* Mejorar el `lint_all.sh` para un mejor manejo de errores segun el [Issue #20](https://github.com/OliverHz28/PC3Proyecto10/issues/20)

```python
import os
import tempfile
from scripts.check_pr import (validar_titulo, verificar_changelog,
                              validar_commits, ejecutar_lint)
from unittest.mock import patch, MagicMock


# Test para verificar que el titulo de PR tiene el formato correcto
def test_titulo_valido():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "123"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)
        archivo = os.path.join(carpeta_pr, f"pr_{pr_id}_title.txt")

        with open(archivo, "w", encoding="utf-8") as f:
            f.write("feat[#123]: primer pull request")
        ok, msg = validar_titulo(carpeta_pr)
        assert ok is True


# No existe el archivo PR ID
def test_archivo_inexistente():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "124"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)

        ok, msg = validar_titulo(carpeta_pr)
        assert ok is False


# El archivo existe pero esta vacío
def test_titulo_vacio():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "125"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)
        archivo = os.path.join(carpeta_pr, f"pr_{pr_id}_title.txt")

        with open(archivo, "w", encoding="utf-8") as f:
            f.write("   \n")

        ok, msg = validar_titulo(carpeta_pr)
        assert ok is False


# Test para verificar que el titulo de PR no tiene el formato correcto
def test_titulo_mal_formato():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "124"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)
        archivo = os.path.join(carpeta_pr, f"pr_{pr_id}_title.txt")

        with open(archivo, "w", encoding="utf-8") as f:
            f.write("PR que no tiene el formato correcto")  # Mal formato

        ok, msg = validar_titulo(carpeta_pr)
        assert ok is False


# test para verificar que el archivo CHANGELOG.md contiene la seccion del PR actual
def test_changelog_contiene_pr():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "125"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)

        changelog_path = os.path.join(temp_dir, "CHANGELOG.md")
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write(f"# Cambios\n\n## PR {pr_id}\n- test PR\n")

        carpeta_actual = os.getcwd()
        os.chdir(os.path.join(temp_dir, pr_id))
        try:
            ok, _ = verificar_changelog(carpeta_pr)
        finally:
            os.chdir(carpeta_actual)

        assert ok


# No existe el archivo CHANGELOG.md
def test_changelog_no_existe():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "201"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)

        # No se crea CHANGELOG.md

        cwd_original = os.getcwd()
        os.chdir(carpeta_pr)
        try:
            ok, msg = verificar_changelog(carpeta_pr)
        finally:
            os.chdir(cwd_original)

        assert ok is False


# test para verificar que el archivo CHANGELOG.md no contiene la seccion del PR actual
def test_changelog_sin_seccion():
    with tempfile.TemporaryDirectory() as temp_dir:
        pr_id = "126"
        carpeta_pr = os.path.join(temp_dir, pr_id)
        os.makedirs(carpeta_pr)

        changelog_path = os.path.join(temp_dir, "CHANGELOG.md")
        with open(changelog_path, "w", encoding="utf-8") as f:
            f.write("# Cambios\n\n## PR 999\n- test PR\n")

        carpeta_actual = os.getcwd()
        os.chdir(carpeta_pr)
        try:
            ok, msg = verificar_changelog(carpeta_pr)
        finally:
            os.chdir(carpeta_actual)

        assert ok is False


# Test para verificar que los commits tienen el formato correcto
def test_commits_todos_validos():
    with tempfile.TemporaryDirectory() as temp_dir:
        carpeta_pr = os.path.join(temp_dir, "127")
        os.makedirs(carpeta_pr)

        commits = """feat[#123]: primer commit
                    fix[#124]: segundo commit
                    refactor[#125]: tercer commit"""
        with open(os.path.join(carpeta_pr, "commits.txt"), "w", encoding="utf-8") as f:
            f.write(commits)

        ok, errores = validar_commits(carpeta_pr)
        assert ok is True
        assert errores == []


# Test para verificar que los commits tienen errores de formato
def test_commits_con_errores():
    with tempfile.TemporaryDirectory() as temp_dir:
        carpeta_pr = os.path.join(temp_dir, "128")
        os.makedirs(carpeta_pr)

        commits = """commit sin formato
                    feat123: falta corchetes
                    fix[#789]: commit correcto"""
        with open(os.path.join(carpeta_pr, "commits.txt"), "w", encoding="utf-8") as f:
            f.write(commits)

        ok, errores = validar_commits(carpeta_pr)
        assert ok is False
        assert len(errores) == 2
        assert "fila 1" in errores[0]
        assert "fila 2" in errores[1]


# Archivo de commits no existe
def test_validar_commits_archivo_inexistente():
    with tempfile.TemporaryDirectory() as temp_dir:
        carpeta_pr = os.path.join(temp_dir, "303")
        os.makedirs(carpeta_pr)

        ok, errores = validar_commits(carpeta_pr)
        assert ok is False


# test para ejecutar el linter y verificar que se ejecuta correctamente
def test_ejecutar_lint_exito():
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Lint exitoso"
        mock_run.return_value = mock_result

        ok, salida = ejecutar_lint()
        assert ok is True


# test para verificar que el linter falla
def test_ejecutar_lint_error():
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error de linting"
        mock_run.return_value = mock_result

        ok, salida = ejecutar_lint()
        assert ok is False
  
      
```
#### [**Contribucciones**](CONTRIBUTIONS.md)