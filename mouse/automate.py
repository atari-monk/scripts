import time
import pyautogui
import json
import keyboard
import win32gui
import win32con

def minimize_console_window():
    console_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(console_window, win32con.SW_MINIMIZE)

def execute_mouse_commands_with_repeats(commands, repeats):
    for _ in range(repeats):
        for command in commands:
            if keyboard.is_pressed('esc'):
                print("Execution stopped by user.")
                return
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

minimize_console_window()

with open('data/video_list/data.json', 'r') as file:
    mouse_commands = json.load(file)

execute_mouse_commands_with_repeats(mouse_commands, repeats)
