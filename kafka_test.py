import win32gui
from kafka_connector import *
from time import sleep

test_topic = 'used_apps_keys_topic'
test_user  = 'luna'


def get_active_window_title():
    active_window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(active_window)
    return window_title


while True:
    active_program = get_active_window_title()
    window_producer3(active_program, username=test_user, topic_name=test_topic)
    break


print(window_consumer_2(topic=test_topic))