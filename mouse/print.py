import pyautogui

def print_mouse_state():
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position - X: {x}, Y: {y}")

        buttons = pyautogui.mouseInfo()
        print("Mouse buttons:", buttons)

print_mouse_state()
