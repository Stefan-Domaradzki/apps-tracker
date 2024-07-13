import win32gui
from kafka_connector import *
from time import sleep

#test_topic = 'used_apps_keys_topic3'
test_topic = 'apps3'
test_user = 'luna'
test_timeout = timedelta(days=0,seconds=10)



#window_producer3(username=test_user, topic_name=test_topic)

print(window_consumer_single_topic(topic=test_topic))
print(window_consumer_2(topic=test_topic))







