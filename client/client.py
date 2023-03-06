from kafka import KafkaProducer, KafkaConsumer
import kafka
import json
import os

BOOTSTRAP_SERVER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
GROUP_ID = os.environ.get('GROUP_ID')

print(f"Got the following bootstrap address: {BOOTSTRAP_SERVER}")
print(f"Got the following topic: {KAFKA_TOPIC}")

# create a Kafka producer
success = False
while not success:
    try:
        producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVER])
    except kafka.errors.NoBrokersAvailable:
        continue
    else:
        success = True
# publish a message to a topic

producer.send(KAFKA_TOPIC, key=b'key', value=json.dumps({'message': 'hello world'}).encode('utf-8'))

# create a Kafka consumer
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[BOOTSTRAP_SERVER], group_id=GROUP_ID)

# consume messages from the topic
for message in consumer:
    print(message)
