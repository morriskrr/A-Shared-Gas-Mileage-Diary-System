from kafka import KafkaProducer, KafkaConsumer
import os
import json

BOOTSTRAP_SERVER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
GROUP_ID = os.environ.get('GROUP_ID')


consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[BOOTSTRAP_SERVER], group_id=GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

print("Retrieving sent messages from topic")
for message in consumer:
    print(message.value)