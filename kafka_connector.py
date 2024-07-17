import json
import win32gui
import pandas as pd
import logging

from datetime import datetime
from datetime import timedelta
from kafka import KafkaProducer
from kafka import KafkaConsumer


connector_logger = logging.getLogger(__name__)
connector_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('./logs/connector.log')
file_handler.setFormatter(formatter)

connector_logger.addHandler(file_handler)


def check_topics(kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(bootstrap_servers=kafka_bootstrap_servers,
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


def window_producer3(topic_name='used_apps_keys_topic',
                     producer_timeout_ms=timedelta(minutes=2),
                     username='test',
                     kafka_bootstrap_servers='localhost:9092'):
    def get_active_window_title():
        active_window = win32gui.GetForegroundWindow()
        window_title = win32gui.GetWindowText(active_window)
        return window_title

    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        key_serializer=lambda key: key.encode('utf-8'),
        value_serializer=lambda val: json.dumps(val).encode('utf-8'),
    )

    window_time = start_date = datetime.now()
    previous_window = get_active_window_title()

    while (datetime.now() - start_date) < producer_timeout_ms:

        date = datetime.now()
        window = get_active_window_title()

        if window != previous_window:

            time_spent = (date - window_time)

            message = {
                'message':    previous_window,
                'time_spent': time_spent.total_seconds(),
                'date':       date.isoformat()
            }

            producer.send(topic=topic_name,
                          key=username,
                          value=message)

            producer.flush()

            # sleep(1)

            previous_window = window
            window_time = date

    connector_logger.info("Tracker producer closed successfully")


def window_consumer_2(topic='', kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        key_deserializer=lambda key: key.decode('utf-8'),
        value_deserializer=lambda val: json.loads(val.decode('utf-8')),
        consumer_timeout_ms=3000
    )

    consumer.subscribe([topic])

    messages = []

    try:
        for message in consumer:

            user = {'user': message.key}
            value = message.value

            value = user | value
            messages.append(value)

            # msg = value['message']
            # time_spent = value['time_spent']
            # date = value['date']

    except KeyboardInterrupt:
        consumer.close()

    finally:
        connector_logger.info("Tracker Consumer closed successfully")

    df = pd.DataFrame(messages)

    current_time = datetime.now()
    filename = current_time.strftime("./data/test-data/data-%Y-%m-%d-%H.csv")
    df.to_csv(filename, index=False)

    return pd.DataFrame(messages)


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

            # user = value['user']
            # msg = value['message']
            # date = value['date']

            #print(f'User: {user}, Message: {msg}, Date: {date}')

        #time.sleep(1)  # Przerwa przed ponownym sprawdzeniem

    except KeyboardInterrupt:
        consumer.close()

    finally:
        print("Tracker Consumer closed successfully")

    df = pd.DataFrame(messages)

    return df
