import time
import pyautogui

# Define your list of mouse commands with timing
mouse_commands = [
    {"command": "move", "x": 1859, "y": 288, "duration": 0.2},
    {"command": "click", "button": "left", "duration": 0.1},
    {"command": "move", "x": 1801, "y": 441, "duration": 0.2},
    {"command": "click", "button": "left", "duration": 0.1},
    # Add more commands as needed
]

# Function to execute mouse commands with timing and repeats
def execute_mouse_commands_with_repeats(commands, repeats):
    for _ in range(repeats):
        for command in commands:
            if command["command"] == "move":
                pyautogui.moveTo(command["x"], command["y"], duration=command["duration"])
            elif command["command"] == "click":
                pyautogui.click(button=command["button"])
            # Add more conditions for other mouse commands

            # Introduce a delay based on duration
            time.sleep(command["duration"])

# Get the desired number of repeats from the user
try:
    repeats = int(input("Enter the number of repeats: "))
except ValueError:
    print("Invalid input. Please enter a valid number.")
    repeats = 0

# Execute the mouse commands with repeats
execute_mouse_commands_with_repeats(mouse_commands, repeats)
