from kafka_connector import *


if __name__ == "__main__":

    test_topic = 'apps3'
    test_user = 'luna'
    test_timeout = timedelta(days=0, seconds=10)

    window_producer3(username=test_user, topic_name=test_topic)
    print(window_consumer_2(topic=test_topic))
