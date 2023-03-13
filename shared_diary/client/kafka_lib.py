from confluent_kafka import Producer, Consumer, KafkaError
import json

class MileageDiaryConsumer:

    def __init__(self, bootstrap_server, kafka_topic, group_id) -> None:
        self.bootstrap_server = bootstrap_server
        self.kafka_topic = kafka_topic
        self.group_id = group_id
        self.consumer = Consumer({
            'bootstrap.servers': self.bootstrap_server,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([self.kafka_topic])
        self.running = True

    def consume_messages(self):
        while self.running:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if not message.error():
                yield message.value().decode('utf-8')
            elif message.error().code() != KafkaError._PARTITION_EOF:
                print(f'Error while consuming messages: {message.error()}')
        self.consumer.close()

    def stop(self):
        self.running = False



class MileageDiaryProducer:

    def __init__(self, bootstrap_server, kafka_topic) -> None:
        self.bootstrap_server = bootstrap_server
        self.kafka_topic = kafka_topic
        self.producer_config = {
            "bootstrap.servers": self.bootstrap_server
        }
        self.producer = Producer(self.producer_config)

    def send_entry(self, message: dict):
        # Convert message to JSON string
        json_message = json.dumps(message)

        # Send message to Kafka topic
        self.producer.produce(self.kafka_topic, key=None, value=json_message)

        # Flush producer buffer to ensure all messages are sent
        self.producer.flush()