# Start with a base Ubuntu image
FROM ubuntu:latest

# Update packages and install required dependencies
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget netcat

# Download and install Kafka
ENV SCALA_VERSION=2.13
ENV KAFKA_VERSION=3.4.0
ENV FILENAME="https://dlcdn.apache.org/kafka/3.4.0/kafka_2.13-${KAFKA_VERSION}.tgz"
RUN wget ${FILENAME} && \
    mkdir -p /opt/kafka && \
    tar -xzf kafka_2.13-${KAFKA_VERSION}.tgz --strip-components=1 -C /opt/kafka && \
    ls /opt/kafka

RUN sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect=zookeeper:2181/' /opt/kafka/config/server.properties
# Expose required Kafka ports
EXPOSE 9092

# Start Kafka
CMD ["/opt/kafka/bin/kafka-server-start.sh", "/opt/kafka/config/server.properties"]