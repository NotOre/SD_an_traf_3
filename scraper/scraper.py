import requests
import json
import random
import time
from datetime import datetime

def millis_a_iso8601(millis):

    return datetime.utcfromtimestamp(millis / 1000).isoformat() + "Z"

def scrape_events(max_eventos=1000):

    top = -32.9222
    bottom = -34.2917
    left = -71.7149
    right = -69.7702

    url = f"https://www.waze.com/live-map/api/georss?top={top}&bottom={bottom}&left={left}&right={right}&env=row&types=alerts,traffic"

    eventos_guardados = []
    
    while len(eventos_guardados) < max_eventos:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            events_alertas = data.get('alerts', [])
            events_trafico = data.get('jams', [])

            todos_los_eventos = [(event, 'trafico') for event in events_trafico] + [(event, 'alerta') for event in events_alertas]
            random.shuffle(todos_los_eventos)

            for event, tipo in todos_los_eventos:
                if len(eventos_guardados) >= max_eventos:
                    break

                pubMillis = event.get('pubMillis')
                if not pubMillis:
                    continue

                evento_id = f"{tipo}_{pubMillis}"

                if tipo == 'trafico' and 'line' in event:
                    coord_ini = event['line'][0]
                    coord_fin = event['line'][1]

                    evento_formateado = {
                        'ID_evento': evento_id,
                        'tipo': 'trafico',
                        'ciudad': event.get('city'),
                        'calle': event.get('street'),
                        'velocidad_kmh': event.get('speedKMH'),
                        'severidad': event.get('severity'),
                        'descripcion_bloqueo': event.get('blockDescription'),
                        'pubMillis': pubMillis,
                        'timestamp': millis_a_iso8601(pubMillis),
                        'location': {
                            'lat': coord_ini.get('y'),
                            'lon': coord_ini.get('x')
                        },
                        'location_fin': {
                            'lat': coord_fin.get('y'),
                            'lon': coord_fin.get('x')
                        }
                    }

                    eventos_guardados.append(evento_formateado)

                elif tipo == 'alerta' and 'location' in event:
                    coord = event['location']

                    evento_formateado = {
                        'ID_evento': evento_id,
                        'tipo': 'alerta',
                        'ciudad': event.get('city'),
                        'calle': event.get('street'),
                        'tipo_alerta': event.get('type'),
                        'subtipo_alerta': event.get('subtype'),
                        'descripcion_reporte': event.get('reportDescription'),
                        'confianza': event.get('reliability'),
                        'pubMillis': pubMillis,
                        'timestamp': millis_a_iso8601(pubMillis),
                        'location': {
                            'lat': coord.get('y'),
                            'lon': coord.get('x')
                        }
                    }

                    eventos_guardados.append(evento_formateado)

        else:
            print(f"Error en la solicitud: {response.status_code}")

        print(f" Eventos recolectados: {len(eventos_guardados)} / {max_eventos}")

        time.sleep(5)

    return eventos_guardados

