#!/bin/bash
set -e

cd /data

INPUT_FILE=${1:-eventos_filtrados.csv}
OUTPUT_LIMPIEZA="filtrado_output"
OUTPUT_CLASIFICACION="clasificacion_output"
OUTPUT_TEMPORAL="temporal_output"

echo "Ejecutando limpieza y filtrado de eventos..."

pig -x local \
  -param input_file="$INPUT_FILE" \
  -param output_dir="$OUTPUT_LIMPIEZA" \
  pig/scripts/limpieza_filtrado.pig

echo ""

echo "Ejecutando clasificación de incidentes..."

echo ""

pig -x local \
  -param input_dir="$OUTPUT_LIMPIEZA" \
  -param output_dir="$OUTPUT_CLASIFICACION" \
  pig/scripts/clasificacion_incidentes.pig

echo ""
echo "Ejecutando análisis espacial y temporal..."
echo ""

pig -x local \
  -param input_dir="$OUTPUT_LIMPIEZA" \
  -param output_dir="$OUTPUT_TEMPORAL" \
  pig/scripts/analisis_espacial_temporal.pig

echo ""
echo "Todos los scripts de Apache Pig fueron ejecutados exitosamente."

