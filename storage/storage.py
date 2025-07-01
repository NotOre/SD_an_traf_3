import redis
import os
import json
import time

class EventStorage:
    def __init__(self):
        redis_host = os.getenv('REDIS_HOST', 'redis')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        
        for _ in range(10):
            try:
                self.client = redis.Redis(host=redis_host, port=redis_port, db=0)
                self.client.ping()
                print("Iniciando Storage")
                time.sleep(2)
                break
                
            except redis.exceptions.ConnectionError:
                print("Esperando a Redis...")
                time.sleep(2)
        else:
            raise Exception("No se pudo conectar a Redis después de varios intentos.")
            
        self.list_name = "eventos"

    def save_event(self, event):
        try:
            self.client.lpush(self.list_name, json.dumps(event))
        except redis.exceptions.RedisError as e:
            print(f"Error guardando evento en Redis: {e}")

    def get_events(self, start=0, end=-1):
        try:
            events = self.client.lrange(self.list_name, start, end)
            return [json.loads(event) for event in events]
        except redis.exceptions.RedisError as e:
            print(f"Error obteniendo eventos de Redis: {e}")
            return []

    def get_all_events(self):
        return self.get_events(0, -1)

    def count_events(self):
        try:
            return self.client.llen(self.list_name)
        except redis.exceptions.RedisError as e:
            print(f"Error contando eventos en Redis: {e}")
            return 0

    def clear_storage(self):
        try:
            self.client.delete(self.list_name)
        except redis.exceptions.RedisError as e:
            print(f"Error limpiando almacenamiento en Redis: {e}")

    def event_exists(self, evento_id):
        try:
            events = self.get_all_events()
            return any(event.get('ID_evento') == evento_id for event in events)
        except Exception as e:
            print(f"Error verificando existencia de evento: {e}")
            return False

