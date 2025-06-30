%default input_dir 'filtrado_output'
%default output_dir 'clasificacion_output'

filtered = LOAD '/data/$input_dir' USING PigStorage(',')
    AS (id:chararray, type:chararray, street:chararray, city:chararray, pubmillis:long);

grouped = GROUP filtered BY (type, city);

counted = FOREACH grouped GENERATE 
    group.type AS tipo, 
    group.city AS comuna, 
    COUNT(filtered) AS cantidad;

DUMP counted;
STORE counted INTO '/data/$output_dir' USING PigStorage(',');

