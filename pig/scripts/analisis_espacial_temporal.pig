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

extraido = FOREACH eventos GENERATE
    ciudad AS comuna,
    SUBSTRING(timestamp, 11, 2) AS hora;

agrupado = GROUP extraido BY (comuna, hora);

conteo = FOREACH agrupado GENERATE
    group.comuna AS comuna,
    group.hora AS hora,
    COUNT(extraido) AS cantidad_eventos;

STORE conteo INTO '/app/data/analisis_espacial_temporal' USING PigStorage(',');

