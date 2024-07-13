import os
import win32gui
from time import sleep
from kafka_connector import window_producer2, window_producer3


# user = os.getlogin()
user = 'Stefan'


def get_active_window_title():
    active_window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(active_window)
    return window_title


if __name__ == "__main__":

    window_producer3(topic_name='apps3')
    '''
    while True:
        active_program = get_active_window_title()
        window_producer2(active_program,username=user, topic_name="used_apps_all_users3")
        #print("Obecnie używany program:", active_program)
        sleep(1)
    '''
