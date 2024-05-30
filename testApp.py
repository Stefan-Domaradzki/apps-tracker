import pygetwindow

def get_running_windows():
    # Uzyskanie listy obiektów okien
    windows = pygetwindow.getAllWindows()
    running_windows = []
    for window in windows:
        try:
            # Pobranie tytułu okna i odpowiadającego mu PID
            window_info = (window.title, window._hWnd)
            running_windows.append(window_info)
        except:
            pass
    return running_windows

print(get_running_windows())

