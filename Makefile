COMPOSE=docker-compose
PROJECT_NAME=entrega3
ENV_FILE=.env

.PHONY: help build up down logs shell elastic index reset clean

help:
	@echo "Comandos disponibles:"
	@echo "  make build        - Construye los servicios de Docker"
	@echo "  make up           - Levanta los servicios"
	@echo "  make down         - Detiene los servicios"
	@echo "  make logs         - Muestra los logs"
	@echo "  make shell        - Abre una shell en el contenedor app"
	@echo "  make elastic      - Prueba conexión a Elasticsearch"
	@echo "  make index        - Indexa datos en Elasticsearch"
	@echo "  make reset        - Elimina contenedores y volúmenes"
	@echo "  make clean        - Borra archivos de salida y volúmenes"

build:
	$(COMPOSE) --env-file $(ENV_FILE) build

up:
	$(COMPOSE) --env-file $(ENV_FILE) up -d

down:
	$(COMPOSE) --env-file $(ENV_FILE) down

logs:
	$(COMPOSE) --env-file $(ENV_FILE) logs -f

shell:
	docker exec -it scraper-storage-app bash

elastic:
	curl -X GET http://localhost:9200

index:
	docker exec -it scraper-storage-app python elastic_indexer/index_to_elastic.py

reset:
	$(COMPOSE) --env-file $(ENV_FILE) down -v --remove-orphans

clean:
	rm -f data/*.csv data/*.json eventos_filtrados.* *.log

