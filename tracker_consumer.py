import time
from kafka import KafkaConsumer
import pandas as pd
import re
import json


def check_topics(kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(bootstrap_servers= kafka_bootstrap_servers,
                             auto_offset_reset='latest',
                             value_deserializer=lambda x: x.decode('utf-8'))

    return consumer.topics()


def window_consumer_single_topic(topic='', kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_bootstrap_servers,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=5000 # genialny parametr musze go potem zapisac sobie na przyszlosc
    )


     # Subskrypcja tematu
    consumer.subscribe([topic])
    print(f'Subscribed to {topic}')

    # Pobieranie i wyświetlanie najnowszej wiadomości

    messages = []

    try:
        for message in consumer:
            print(message)

            value = message.value

            messages.append(value)

            print(f'Received message: {value}')
            user = value['user']
            msg = value['message']
            date = value['date']

            print(f'User: {user}, Message: {msg}, Date: {date}')

            # print("Key: %s, Value: %s" % (message.key, message.value))

        #time.sleep(1)  # Przerwa przed ponownym sprawdzeniem

    except KeyboardInterrupt:
        consumer.close()

    finally:
        print("Tracker Consumer closed succesfully")

    df = pd.DataFrame(messages)
    return df

'''
def app_consumer_all_data(kafka_bootstrap_servers='localhost:9092'):

    consumer = KafkaConsumer(bootstrap_servers=kafka_bootstrap_servers,
                             auto_offset_reset='earliest',
                             value_deserializer=lambda x: x.decode('utf-8'))

    topics = consumer.topics()

    for topic in topics:
        print(topic)
        consumer.subscribe(topics=[topic])

        # Pobieranie i wyświetlanie najnowszej wiadomości
        try:

            for message in consumer:

                value = message.value
                value = json.loads(message.value)

                print(value)

                #print("Key: %s, Value: %s" % (message.key, message.value))
                break  # Przerwij pętlę po odczytaniu pierwszej (najnowszej) wiadomości

            time.sleep(1)  # Przerwa przed ponownym sprawdzeniem

        except KeyboardInterrupt:
            consumer.close()
'''