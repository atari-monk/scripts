import win32gui
import win32con

def minimize_console_window():
    console_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console_window, win32con.SW_MINIMIZE)

def bring_console_window_to_front():
    console_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console_window, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(console_window)
