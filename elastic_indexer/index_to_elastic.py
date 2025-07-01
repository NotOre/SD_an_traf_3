from elasticsearch import Elasticsearch, helpers
import json
import os
import csv
from dotenv import load_dotenv
load_dotenv()

ELASTIC_HOST = os.getenv('ELASTIC_HOST', 'elasticsearch')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))
ELASTIC_INDEX = os.getenv('ELASTIC_INDEX', 'eventos_waze')

es = Elasticsearch(
    f"http://{ELASTIC_HOST}:{ELASTIC_PORT}",
    headers={
        "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
        "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"
    }
)

def cargar_eventos_desde_json(archivo_path):
    with open(archivo_path, 'r', encoding='utf-8') as f:
        eventos = json.load(f)
    return eventos
    
def cargar_eventos_desde_pig_output(carpeta_path):
    eventos = []
    for filename in os.listdir(carpeta_path):
        filepath = os.path.join(carpeta_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    eventos.append(row)
    return eventos



def indexar_eventos(eventos):
    acciones = []

    for evento in eventos:
        accion = {
            "_index": ELASTIC_INDEX,
            "_id": evento['ID_evento'],
            "_source": evento
        }
        acciones.append(accion)


    helpers.bulk(es, acciones)
    print(f"{len(acciones)} eventos indexados en Elasticsearch.")

def crear_indice_si_no_existe():
    try:
        print(f"Chequeando si índice '{ELASTIC_INDEX}' existe...")
        
        try:
            print("Info de Elasticsearch:", es.info())
        except Exception as e:
            print("Error en es.info():", e)
        
        exists = es.indices.exists(index=ELASTIC_INDEX)
        print(f"Existe: {exists}")
        if not exists:
            
            es.indices.create(index=ELASTIC_INDEX)
            print(f"Índice '{ELASTIC_INDEX}' creado en Elasticsearch.")
        else:
            print(f"Índice '{ELASTIC_INDEX}' ya existe.")
    except Exception as e:
        print(f"Error al crear índice: {e}")
        if hasattr(e, 'body'):
            print("Error body (vía e.body):", e.body)
        elif hasattr(e, 'meta') and hasattr(e.meta, 'response') and hasattr(e.meta.response, 'text'):
            print("Error body (vía e.meta.response.text):", e.meta.response.text)
        raise

if __name__ == "__main__":
    ruta_csv_dir = "data/eventos_filtrados"
    if not os.path.exists(ruta_csv_dir):
        raise FileNotFoundError(f"No se encontró la carpeta: {ruta_csv_dir}")

    crear_indice_si_no_existe()
    eventos = cargar_eventos_desde_pig_output(ruta_csv_dir)
    indexar_eventos(eventos)

