import time
from kafka import KafkaConsumer
from datetime import datetime


from kafka_connector import window_consumer_single_topic
from kafka_connector import check_topics
from data_transforming import clean_and_transform
#from data_transforming import user_activity_type_bar_chart


if __name__ == "__main__":
    print(check_topics())
    #topics=check_topics()

    test_df = window_consumer_single_topic(topic='used_apps_all_users3')
    current_time = datetime.now()
    filename = current_time.strftime("./data/data-%Y-%m-%d-%H.csv")

    test_df.to_csv(filename, index=False)

    print(f"Ramka danych została zapisana do pliku: {filename}")

    print('#################################################')
    print('                TEST-DATA-FRAME                  ')
    print('#################################################')
    print(test_df)

    print('#################################################')
    print('               TEST-DATA-TRANSFORM               ')
    print('#################################################')
    print(clean_and_transform(test_df))
