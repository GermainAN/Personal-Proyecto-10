#!/usr/bin/env bash

cd "$(dirname "$0")/.." || exit

errores=0 

echo "Ejecutando flake8"
if flake8 src/ tests/ ./*.py --max-line-length=88 --select=E,W,F; then
  echo "No se encontraron errores con flake8"
else
  echo "flake8 encontro errores"
  errores=1
fi

echo "*********************"
echo "Ejecutando shellcheck"
if shellcheck scripts/* hooks/*; then 
  echo "No se encontraron errores con shellcheck"
else
  echo "shellcheck encontro errores"
  errores=1
fi

echo "*********************"
echo "Ejecutando tflint"
if [ -d "iac" ]; then
  if tflint --enable-all iac/; then
    echo "No se encontraron errores con tflint"
  else
    echo "tflint encontro errores"
    errores=1
  fi
else
  echo "No se encontro el directorio de IaC"
fi

echo "*********************"
echo "Resultado Final:"
if [ $errores -eq 1 ]; then
  echo "Se encontraron errores"
  exit 1
else
  echo "Todos los lint pasaron correctamente"
  exit 0
fi