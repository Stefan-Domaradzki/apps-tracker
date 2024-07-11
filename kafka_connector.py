import json

from datetime import datetime

import pandas as pd

from kafka import KafkaProducer
from kafka import KafkaConsumer


def check_topics(kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(bootstrap_servers= kafka_bootstrap_servers,
                             auto_offset_reset='latest',
                             value_deserializer=lambda x: x.decode('utf-8'))

    return consumer.topics()


def all_users(df):
    return df['user'].unique()


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

    print(f' User: {username}, using {msg} @ {datetime.now()} | to kafka topic {topic_name}')
    producer.send(topic_name, message)
    producer.flush()


def window_producer3(msg, topic_name='used_apps_keys_topic', username='test', kafka_bootstrap_servers='localhost:9092'):

    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        key_serializer=lambda v: v.encode('utf-8')
    )

    date = datetime.now().isoformat()

    message = {
        'message': msg,
        'date': date
    }

    print(f' User: {username}, using {msg} @ {datetime.now()} | to kafka topic {topic_name}')

    producer.send(topic=topic_name,
                  key=username,
                  value=message)

    producer.flush()


def window_consumer_2(topic='', group_id='app-gui', kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    consumer.subscribe([topic])

    messages = []

    try:
        for message in consumer:

            user = message.key
            value = message.value

            value = user | value
            messages.append(value)

            # print(f'Received message: {value}')

            msg = value['message']
            date = value['date']

            #print(f'User: {user}, Message: {msg}, Date: {date}')

        #time.sleep(1)  # Przerwa przed ponownym sprawdzeniem

    except KeyboardInterrupt:
        consumer.close()

    print("Tracker Consumer closed successfully")

    df = pd.DataFrame(messages)

    return df


def window_consumer_single_topic(topic='', kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=5000
    )

    consumer.subscribe([topic])
    print(f'Subscribed to {topic}')

    messages = []

    try:
        for message in consumer:

            value = message.value

            messages.append(value)

            # print(f'Received message: {value}')

            user = value['user']
            msg = value['message']
            date = value['date']

            #print(f'User: {user}, Message: {msg}, Date: {date}')

        #time.sleep(1)  # Przerwa przed ponownym sprawdzeniem

    except KeyboardInterrupt:
        consumer.close()

    finally:
        print("Tracker Consumer closed successfully")

    df = pd.DataFrame(messages)

    return df
