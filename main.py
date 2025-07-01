from scraper.scraper import scrape_events
from storage.storage import EventStorage
from elastic_indexer.index_to_elastic import crear_indice_si_no_existe, indexar_eventos, cargar_eventos_desde_pig_output
import subprocess
import os
import json
import csv

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)


def guardar_como_csv(eventos, archivo_path):
    if not eventos:
        print("No hay eventos para guardar en CSV.")
        return

    if os.path.isdir(archivo_path):
        raise IsADirectoryError(f"'{archivo_path}' es un directorio, se esperaba un archivo CSV.")

    campos = set()
    for evento in eventos:
        campos.update(evento.keys())
    campos = sorted(campos)

    with open(archivo_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(eventos)

    print(f"Eventos guardados en CSV: {archivo_path}")

def guardar_como_json(eventos, archivo_path):
    with open(archivo_path, 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)
    print(f"Eventos guardados en JSON: {archivo_path}")

def main():


    print("Iniciando scraping desde Waze...")
    eventos = scrape_events()
    print(f"Scraping finalizado: {len(eventos)} eventos obtenidos.")

    print("Almacenando eventos en Redis...")
    storage = EventStorage()
    eventos_guardados = 0
    for evento in eventos:
        storage.save_event(evento)
        eventos_guardados += 1
    print(f"{eventos_guardados} eventos almacenados en Redis.")

    print("Guardando eventos crudos...")
    guardar_como_csv(eventos, os.path.join(DATA_DIR, 'eventos_crudos.csv'))
    guardar_como_json(eventos, os.path.join(DATA_DIR, 'eventos_crudos.json'))

    print("Ejecutando procesamiento con Apache Pig...")
    subprocess.run(["bash", "pig/run_pig.sh"])
    print("Procesamiento con Pig completado.")

    print("Indexando eventos procesados en Elasticsearch...")
    crear_indice_si_no_existe()
    eventos_procesados = cargar_eventos_desde_pig_output(os.path.join(DATA_DIR, 'eventos_filtrados'))
    indexar_eventos(eventos_procesados)
    print("Indexación completada.")

if __name__ == "__main__":
    main()

