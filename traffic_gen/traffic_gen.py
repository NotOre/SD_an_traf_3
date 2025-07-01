import redis
import os
import json
import time
import random
import numpy as np

LAMBDA_POISSON = 100
ALPHA_PARETO = 2.0
SCALE_PARETO = 0.2

class traffic_generator:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))

        for _ in range(10):
            try:
                self.client = redis.Redis(host=redis_host, port=redis_port, db=0)
                self.client.ping()
                print("Iniciando Generador de Tráfico")
                break
            except redis.exceptions.ConnectionError:
                print("Esperando a Redis...")
                time.sleep(2)
        else:
            raise Exception("No se pudo conectar a Redis después de varios intentos.")
    
    def random_alternator(self):
        if random.random() < 0.5:
            return np.random.exponential(1 / LAMBDA_POISSON)
        else:
            return SCALE_PARETO * (1 + np.random.pareto(ALPHA_PARETO))

    def generar_trafico(self):
        eventos_consultados = []
        max_eventos = 5000

        while len(eventos_consultados) < max_eventos:
            total_eventos = self.client.llen('eventos')
            if total_eventos == 0:
                print("¿No hay eventos?... Esperando...")
                time.sleep(1)
                continue

            index = random.randint(0, total_eventos - 1)
            evento_json = self.client.lindex('eventos', index)

            if evento_json:
                try:
                    evento = json.loads(evento_json)
                    # Validación básica
                    if all(k in evento for k in ['ID_evento', 'timestamp', 'location']):
                        eventos_consultados.append(evento)
                except Exception as e:
                    print(f"Error al decodificar evento: {e}")
                    continue

            if len(eventos_consultados) % 500 == 0:
                print(f"Eventos consultados: {len(eventos_consultados)} / {max_eventos}")

            time.sleep(self.random_alternator())

        return eventos_consultados

