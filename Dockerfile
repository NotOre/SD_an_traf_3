# Usamos una imagen oficial de Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    git \
    openjdk-17-jre-headless \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta compartida para datos
RUN mkdir -p /data

# Copiar código fuente
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xvzf pig-0.17.0.tar.gz && \
    mv pig-0.17.0 /opt/pig && \
    ln -s /opt/pig/bin/pig /usr/local/bin/pig && \
    rm pig-0.17.0.tar.gz
    
ENV PIG_HOME=/opt/pig
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$PIG_HOME/bin:$PATH"


# Definir comando por defecto
ENTRYPOINT ["python"]
CMD ["main.py"]
