%default input_dir 'filtrado_output'
%default output_dir 'temporal_output'

filtered = LOAD '/data/$input_dir' USING PigStorage(',')
    AS (id:chararray, type:chararray, street:chararray, city:chararray, pubmillis:long);

by_hour = FOREACH filtered GENERATE
    id,
    type,
    city,
    (long)(pubmillis / 3600000) AS hour_bucket;

grouped = GROUP by_hour BY hour_bucket;

counted = FOREACH grouped GENERATE 
    group AS hora, 
    COUNT(by_hour) AS total_incidentes;

DUMP counted;
STORE counted INTO '/data/$output_dir' USING PigStorage(',');

