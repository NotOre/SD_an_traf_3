eventos = LOAD '/app/data/eventos_filtrados.csv' USING PigStorage(',') AS (
    ID_evento:chararray,
    tipo:chararray,
    ciudad:chararray,
    calle:chararray,
    velocidad_kmh:chararray,
    severidad:chararray,
    descripcion_bloqueo:chararray,
    pubMillis:chararray,
    timestamp:chararray,
    location_lat:chararray,
    location_lon:chararray,
    location_fin_lat:chararray,
    location_fin_lon:chararray,
    tipo_alerta:chararray,
    subtipo_alerta:chararray,
    descripcion_reporte:chararray,
    confianza:chararray
);

por_tipo = GROUP eventos BY tipo;

conteo_tipo = FOREACH por_tipo GENERATE group AS tipo_evento, COUNT(eventos) AS cantidad;

STORE conteo_tipo INTO '/app/data/clasificacion_por_tipo' USING PigStorage(',');

