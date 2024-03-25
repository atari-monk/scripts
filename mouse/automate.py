import time
import pyautogui
import json
from pynput import mouse

stop_execution = False

def on_click(x, y, button, pressed):
    global stop_execution
    if button == mouse.Button.right:
        print("Execution stopped by user.")
        stop_execution = True
        return False

def execute_mouse_commands_with_repeats(commands, repeats):
    global stop_execution
    for _ in range(repeats):
        if stop_execution:
            break
        for command in commands:
            if stop_execution:
                break
            if command.get("note"):
                print("Note:", command["note"])
            if command.get("command"):
                if command["command"] == "move":
                    pyautogui.moveTo(command["x"], command["y"], duration=command["duration"])
                elif command["command"] == "click":
                    pyautogui.click(button=command["button"], duration=command["duration"])
                elif command["command"] == "ctrl_v":
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(command["duration"])
                elif command["command"] == "enter":
                    pyautogui.press('enter')
                    time.sleep(command["duration"])
                time.sleep(command["duration"])

try:
    repeats = int(input("Enter the number of repeats: "))
except ValueError:
    print("Invalid input. Please enter a valid number.")
    repeats = 0

with open('data/video_list/data.json', 'r') as file:
    mouse_commands = json.load(file)

with mouse.Listener(on_click=on_click) as listener:
    execute_mouse_commands_with_repeats(mouse_commands, repeats)
    listener.join()
