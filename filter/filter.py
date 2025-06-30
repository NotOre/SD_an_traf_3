import json
from datetime import datetime

def filtrar_y_homogeneizar(eventos_raw):
    eventos_filtrados = []

    for evento in eventos_raw:
        try:
            
            if not all(key in evento for key in ('ID_evento', 'tipo', 'ciudad', 'pubMillis')):
                continue

            
            timestamp = datetime.fromtimestamp(int(evento['pubMillis']) / 1000).isoformat()

            evento_homogeneo = {
                'ID_evento': evento['ID_evento'],
                'tipo': evento['tipo'].strip().lower(),
                'comuna': evento['ciudad'].strip().lower(),
                'timestamp': timestamp,
                'descripcion': evento.get('descripcion_reporte', '').strip()
            }
            #Mirando en retrospectiva, siento que mi codigo ya hacia esto en la entrega 1 pero lo volvere a hacer en caso de que me equivoque

            eventos_filtrados.append(evento_homogeneo)

        except Exception as e:
            print(f"Error procesando evento: {e}")
            continue

    return eventos_filtrados
