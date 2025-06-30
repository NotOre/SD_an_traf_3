from scraper.scraper import scrape_events
from storage.storage import EventStorage
from traffic_gen.traffic_gen import traffic_generator
from cache.cache import Cache
from filter.filter import filtrar_y_homogeneizar
import time
import csv
import json
import os


def guardar_como_json(eventos, archivo_path):
    with open(archivo_path, 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)
    print(f"Eventos guardados en el archivo JSON: {archivo_path}")

def guardar_como_csv(eventos, archivo_path):
    if not eventos:
        return
    campos = eventos[0].keys()
    with open(archivo_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(eventos)
    print(f"Eventos guardados en el archivo CSV: {archivo_path}")
    

def main():
    # Scrapeamos eventos desde Waze
    eventos = scrape_events()
    
    print(f"Fin de funcion Scraper")
    time.sleep(2)
    
    print(f"Inicio de funcion filtro")
    time.sleep(2)
    
    #Filtro
    eventos_filtrados = filtrar_y_homogeneizar(eventos)
    
    print(f"Fin de funcion filtro")
    time.sleep(2)
    
    # Almacenamos los eventos en Redis
    storage = EventStorage()
    for evento in eventos_filtrados:
        storage.save_event(evento)
    print(f" {len(eventos_filtrados)} eventos almacenados.")
    
    guardar_como_json(eventos_filtrados, 'eventos_filtrados.json')
    guardar_como_csv(eventos_filtrados, 'eventos_filtrados.csv')

    # Generamos tráfico de consultas y obtenemos los eventos consultados 
    traffic_gen = traffic_generator()
    eventos_consultados = traffic_gen.generar_trafico()
    print(f" {len(eventos_consultados)} eventos fueron consultados.")

    # Cacheamos solo eventos consultados
    cache = Cache()
    for evento in eventos_consultados:
        cache.save_to_cache(evento)
    print(f" {len(eventos_consultados)} eventos cacheados.")
    
    # Imprimimos que datos estan almacenados en cache (solo para verificar)
    cache.get_all_cache()
    
if __name__ == "__main__":
    main()
