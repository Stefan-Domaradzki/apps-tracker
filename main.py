import win32gui
from time import sleep
from tracker_kafka_producer import window_producer, window_producer2



def get_active_window_title():
    active_window = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(active_window)
    return window_title

'''
def get_active_window_obj():

    active_window = win32gui.GetForegroundWindow()

    #window_object = win32gui.GetObjectType(active_window)

    #print(f"Aktywne okno (obiekt): {window_object}")

    return window_info
    #return window_object
'''

if __name__ == "__main__":

    for i in range(200):
        active_program = get_active_window_title()
        window_producer2(active_program,username='Domianik', topic_name="used_apps_all_users3")
        #print("Obecnie używany program:", active_program)
        sleep(1)



    for i in range(200):
        active_program = get_active_window_title()
        window_producer2(active_program,username='Luna', topic_name="used_apps_all_users3")
        #print("Obecnie używany program:", active_program)
        sleep(1)


