import time
import json

from datetime import datetime

from kafka import KafkaProducer


def serializer(message):
    return json.dumps(message).encode('utf-8')


def window_producer2(msg, topic_name='used_apps_all_users', username='test', kafka_bootstrap_servers='localhost:9092'):


    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
    )

    message = {
        'user': username,
        'message': msg,
        'date': datetime.now().isoformat()
    }

    # print(f' User: {username}, using {msg} @ {datetime.now()} | Sending to {topic_name}')
    print(f' User: {username}, using {msg} @ {datetime.now()} | to kafka topic {topic_name}')
    producer.send(topic_name, message)
    producer.flush()


def window_producer(msg, topic='', username='test', kafka_bootstrap_servers='localhost:9092'):
    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,  # local host należy zmienić na IP urządzenia służącego jako kafka broker
        value_serializer=serializer
    )

    topic_name = username + '_used_apps_' + topic

    print(f' User: {username}, using {msg} @ {datetime.now()} | Sending to {topic_name}')
    producer.send(topic_name, msg)
    producer.flush()

