from kafka import KafkaProducer, KafkaConsumer
import kafka
import argparse
import time
import json
import os

BOOTSTRAP_SERVER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC')
GROUP_ID = os.environ.get('GROUP_ID')

def send_entry(producer, message: dict):

    try:
        producer.send(KAFKA_TOPIC, value=json.dumps(message).encode('utf-8')).get(timeout=10)
    except kafka.errors.KafkaError:
        # Decide what to do if produce request failed...
        print("Entry send failed, please retry")


def main(user: str):
    print(f"Got the following bootstrap address: {BOOTSTRAP_SERVER}")
    print(f"Got the following topic: {KAFKA_TOPIC}")

    # create a Kafka producer
    producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVER])
    # publish a message to a topic
    keep_going = True
    while keep_going:
        start = input("Please enter start kilometers: ")
        stop = input("Please enter stop kilometers: ")

        entry = {
            "user": user,
            "start": start,
            "stop": stop
        }

        send_entry(producer, entry)

        time.sleep(2)
        # # consume messages from the topic
        # print("Retrieving sent messages from topic")
        # # create a Kafka consumer
        # consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[BOOTSTRAP_SERVER], group_id=GROUP_ID,
            # auto_offset_reset='earliest',
            # enable_auto_commit=True,
            # value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        # for message in consumer:
        #     print(message.value)

        _keep_going = input("Do you want to keep going (y/n)?")
        if not _keep_going.lower() == "y":
            keep_going = False

parser = argparse.ArgumentParser()
parser.add_argument("--user", "-u", default="testuser", required=False)

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.user)