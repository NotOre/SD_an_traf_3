#!/bin/bash

rm -rf /app/data/clasificacion_por_tipo
rm -rf /app/data/analisis_espacial_temporal
rm -rf /app/data/eventos_filtrados

echo "Ejecutando limpieza y filtrado con Pig..."
pig -x local pig/scripts/limpieza_filtrado.pig

echo "Ejecutando clasificación con Pig..."
pig -x local pig/scripts/clasificacion_incidentes.pig

echo "Ejecutando análisis espacial-temporal con Pig..."
pig -x local pig/scripts/analisis_espacial_temporal.pig

echo "Procesamiento Pig completado."

