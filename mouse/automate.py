import time
import pyautogui
import json

def execute_mouse_commands_with_repeats(commands, repeats):
    for _ in range(repeats):
        for command in commands:
            if command["command"] == "move":
                pyautogui.moveTo(command["x"], command["y"], duration=command["duration"])
            elif command["command"] == "click":
                pyautogui.click(button=command["button"])
            time.sleep(command["duration"])

try:
    repeats = int(input("Enter the number of repeats: "))
except ValueError:
    print("Invalid input. Please enter a valid number.")
    repeats = 0

with open('mouse_commands.json', 'r') as file:
    mouse_commands = json.load(file)

execute_mouse_commands_with_repeats(mouse_commands, repeats)
