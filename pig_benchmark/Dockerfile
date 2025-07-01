FROM openjdk:11-jre-slim

RUN apt-get update && apt-get install -y wget curl && \
    wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xzf pig-0.17.0.tar.gz && mv pig-0.17.0 /opt/pig && \
    ln -s /opt/pig/bin/pig /usr/local/bin/pig

ENV PIG_HOME=/opt/pig
ENV PATH=$PATH:$PIG_HOME/bin

WORKDIR /pig
CMD ["bash", "run_pig.sh"]
