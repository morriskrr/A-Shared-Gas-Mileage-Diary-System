from flask import Flask, render_template, request
from time import sleep
from json import dumps, loads 
from kafka import KafkaProducer, KafkaConsumer

app = Flask(__name__)


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
)

consumer = KafkaConsumer(
    'topic_journal',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

KAFKA_TOPIC= 'topic_journal'





@app.route('/newrecord', methods = ['GET', 'POST'])
def main():

    
    if request.method == 'POST':
        Input = request.form['datainput']        
        producer.send(KAFKA_TOPIC,value= dumps({'message': Input}).encode('utf-8'))
        producer.flush()
        for event in consumer:
            event_data = event.value
            return "new data here " + event_data['message']
    return render_template('index.html')





