raw = LOAD '/data/eventos_crudos.csv' USING PigStorage(',') AS (
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

limpios = FILTER raw BY ID_evento IS NOT NULL AND tipo IS NOT NULL AND ciudad IS NOT NULL;

deduplicados = DISTINCT limpios;

STORE deduplicados INTO 'data/eventos_filtrados' USING PigStorage(',');

