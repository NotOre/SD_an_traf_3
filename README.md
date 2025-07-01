# SD_an_traf_3

Este repositorio es la tercera y ultima entrega de un proyecto semestral para el ramo de 'Sistemas Distribuidos' de la 'Universidad Diego Portales', la primera entrega se encuentra en el siguiente link: https://github.com/NotOre/SD_Proyecto_Analisis_de_Trafico y la segunda en entrega en https://github.com/NotOre/SD_Proyecto_Analisis_de_Trafico_Ent_2

En este repositorio se encuentran los codigos y archivos requeridos para el uso de nuestro sistema de analisis de trafico, especificamente sobre la Region Metropolitana de Chile, basado en Docker, el cual funciona mediante un scraper utilizado sobre la plataforma Live-Map de Waze (https://www.waze.com/live-map), asi adquiriendo los eventos dentro del area establecida, almacenandolos en una base de datos y en un cache basados en Redis y, para determinar que almacena el cache, el sistema incluye un simulador de consultas el cual ayuda a definir los eventos almacenados en cache.

Este sistema esta orientado principalmente a usuarios que usen sistemas Unix-like (Linux o macOS), y se asume que dicho usuario ya tiene instaladas las dependencias y todo lo necesario para el uso de Docker y Python3.

Este proyecto sera dividido en 3 entregas que se iran actualizando con respecto a la realizacion de dichos avances.

# Entrega 3: Visualizacion
Para ejecutar el codigo de esta entrega se prepararon 2 opciones principales, al guiarte por una de estas opciones debe ser ejecutada mediante una terminal que debes abrir dentro de la carpeta que almacena todos los archivos de nuestro sistema:

## Opcion 1: Make
Este proyecto incluye un Makefile para facilitar la ejecución de tareas comunes y el manejo del entorno Docker. El uso de make estandariza los comandos necesarios para ejecutar, probar, limpiar y mantener el sistema, sin necesidad de recordar instrucciones complejas.

#### Construye los servicios definidos en Docker Compose.
```bash
make build
```

#### Inicia todos los servicios en segundo plano (-d).
```bash
make up
```

#### 	Detiene y elimina los contenedores sin borrar volúmenes.
```bash
make down
```
#### 	Muestra los logs de todos los servicios en tiempo real.
```bash
make logs
```

#### Abre una shell interactiva en el contenedor principal scraper-storage-app.
```bash
make shell
```

#### 	Prueba la conexión con Elasticsearch usando curl.
```bash
make elastic
```

#### 	Ejecuta el script index_to_elastic.py dentro del contenedor.
```bash
make index
```

#### 	Elimina contenedores, volúmenes y redes huérfanas del entorno.
```bash
make reset
```

#### 	Borra archivos generados (.csv, .json, .log) del directorio data/.
```bash
make clean
```

## Opcion 2: Docker-compose
Esta siendo la principal forma de iniciar un programa basado en Docker.

### Ejecucion

#### 1) Construir/reconstruir imagenes (Usar cada vez que se haya modificado el codigo o cuando recien se haya descargado el sistema)
```bash
docker-compose build
```
#### 2) Levantar contenedores (Inicia el sistema)
```bash
docker-compose up -d
```
### Detencion

#### Detener contenedores (Usar en caso de querer detener el sistema, como para modificar algo del codigo o en caso de alguna falla ocurrida)
```bash
docker-compose down
```
### Visualizacion

####  Ver logs en vivo (Usar para ver lo que ocurre durante la ejecucion del sistema)
```bash
docker-compose logs -f
```
