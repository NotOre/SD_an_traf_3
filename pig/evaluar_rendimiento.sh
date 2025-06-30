#!/bin/bash
set -e

ORIGINAL="../eventos_filtrados.csv"
TEST_DATA="../data_temp.csv"

TAMAÑOS=("1000" "5000" "10000")

echo "Evaluando rendimiento de Apache Pig..."
echo ""

for N in "${TAMAÑOS[@]}"; do
    echo "[+] Preparando muestra de $N eventos..."

    head -n 1 "$ORIGINAL" > "$TEST_DATA"
    tail -n +2 "$ORIGINAL" | head -n $N >> "$TEST_DATA"

    echo "[~] Ejecutando Pig con $N eventos..."

    START=$(date +%s)
    
    bash run_pig.sh "$TEST_DATA" > /dev/null 2>&1

    END=$(date +%s)
    DIFF=$(( END - START ))

    echo "  Tiempo para $N eventos: ${DIFF}s"
    echo "---------------------------------------"
done

echo "Evaluación completa."

