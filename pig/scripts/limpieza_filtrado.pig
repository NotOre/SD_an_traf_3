%default input_file 'eventos_filtrados.csv'
%default output_dir 'filtrado_output'

raw = LOAD '/data/$input_file' USING PigStorage(',')
    AS (id:chararray, type:chararray, street:chararray, city:chararray, pubmillis:long);

filtered = FILTER raw BY 
    (type IS NOT NULL AND type != '' AND
     city IS NOT NULL AND city != '' AND
     pubmillis IS NOT NULL);

normalized = FOREACH filtered GENERATE 
    id, 
    type, 
    street, 
    UPPER(city) AS city, 
    pubmillis;

DUMP normalized;
STORE normalized INTO '/data/$output_dir' USING PigStorage(',');
