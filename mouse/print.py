import pyautogui

# Function to print mouse state
def print_mouse_state():
    while True:
        x, y = pyautogui.position()
        print(f"Mouse position - X: {x}, Y: {y}")

        buttons = pyautogui.mouseInfo()
        print("Mouse buttons:", buttons)

# Run the function to continuously print mouse state
print_mouse_state()
