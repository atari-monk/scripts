import time
import pyautogui
from pynput import mouse
import window
from data_loader import load_positions, load_mouse_commands, join_positions_to_commands

stop_execution = False

def on_click(x, y, button, pressed):
    global stop_execution
    if button == mouse.Button.right:
        print("Execution stopped by user.")
        stop_execution = True
        return False

def execute_mouse_commands_with_repeats(repeats):
    global stop_execution
    
    positions = load_positions('data/video_list/positions_watch_later.json')
    mouse_commands = load_mouse_commands('data/video_list/data.json')
    mouse_commands = join_positions_to_commands(mouse_commands, positions)
    
    for repeat_number in range(1, repeats + 1):
        print(f"Repeat {repeat_number}")
        with open('execution.log', 'a') as log_file:
            log_file.write(f'Repeat {repeat_number}\n')
        step_number = 1
        if stop_execution:
            break
        for command in mouse_commands:
            if stop_execution:
                break
            if command.get("note"):
                print(f"Step {step_number}: {command['note']}")
                with open('execution.log', 'a') as log_file:
                    log_file.write(f'Step {step_number}: {command["note"]}\n')
                step_number += 1
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
                step_number += 1
                time.sleep(command["duration"])

try:
    repeats = int(input("Enter the number of repeats: "))
except ValueError:
    print("Invalid input. Please enter a valid number.")
    repeats = 0

window.minimize_console_window()

with mouse.Listener(on_click=on_click) as listener:
    execute_mouse_commands_with_repeats(repeats)
    listener.join()
