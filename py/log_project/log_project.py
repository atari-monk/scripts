import os
import json
import subprocess  # Import subprocess module
from datetime import datetime

# Constants
CONVERS_SCRIPT_PATH = "convert.py"
DATABASE_FOLDER = "C:/atari-monk/code/apollo/content/Database"
LOG_FILE_NAME = "log_project.txt"
PROJECT_LIST_NAME = "projects.json"
STATE_FILE_NAME = "state.json"
DATE_FORMAT = "%Y-%m-%d %H:%M"

# Combine folder and file names
LOG_FILE_PATH = os.path.join(DATABASE_FOLDER, LOG_FILE_NAME)
PROJECT_LIST_PATH = PROJECT_LIST_NAME
STATE_FILE_PATH = STATE_FILE_NAME

# Initialize the log file if it doesn't exist
def initialize_log_file():
    """Check if the log file exists; if not, create it with initial content."""
    os.makedirs(DATABASE_FOLDER, exist_ok=True)  # Ensure the folder exists
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w') as file:
            file.write("")  # Ensure there is an empty string written to the file
        print(f"Log file created: {LOG_FILE_PATH}")
    else:
        print(f"Log file already exists: {LOG_FILE_PATH}")

# Load project list from JSON file
def load_project_list():
    """Load the project list from the JSON file."""
    if os.path.exists(PROJECT_LIST_PATH):
        with open(PROJECT_LIST_PATH, 'r') as file:
            return json.load(file)
    else:
        print(f"Error: {PROJECT_LIST_PATH} not found.")
        return {}

# Validate user input against the project list
def validate_project_name(project_list):
    """Prompt the user to input a valid project name from the JSON project list."""
    while True:
        project_name = input("Enter the project name: ").strip()
        if project_name in project_list:
            return project_name
        else:
            print(f"Invalid project name. Please choose from: {', '.join(project_list.keys())}")

# Load or initialize internal state (whether a project is starting or ending)
def load_state():
    """Load the project state from the state JSON file or initialize it."""
    if os.path.exists(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, 'r') as file:
                return json.load(file) or {}  # Return empty dict if file is empty
        except json.JSONDecodeError:
            print(f"Warning: {STATE_FILE_PATH} is empty or corrupted. Initializing new state.")
            return {}
    else:
        return {}

# Save the current state to a file
def save_state(state):
    """Save the internal state back to the state JSON file."""
    with open(STATE_FILE_PATH, 'w') as file:
        json.dump(state, file)

# Log the project entry (either active or off)
def log_project_entry(project_name, action):
    """Log the project start or end entry to the markdown file."""
    timestamp = datetime.now().strftime(DATE_FORMAT)
    entry = f"{timestamp} {project_name} ({action})\n"
    
    with open(LOG_FILE_PATH, 'a') as file:
        file.write(entry)
    
    print(f"Logged: {entry.strip()}")
    
    # Run the convert.py script after logging
    try:
        subprocess.run(["python",CONVERS_SCRIPT_PATH], check=True)  # Update the path to convert.py as needed
        print("Successfully ran convert.py.")
    except subprocess.CalledProcessError as e:
        print(f"Error running convert.py: {e}")

def check_active_project(state):
    """Check if any project is currently active."""
    for project, status in state.items():
        if status == "active":
            return project
    return None

def main():
    """Main function to handle project logging."""
    initialize_log_file()
    
    # Load the project list
    project_list = load_project_list()
    if not project_list:
        return  # Exit if the project list couldn't be loaded

    # Load the internal state
    state = load_state()

    # Check if any project is currently active
    active_project = check_active_project(state)

    # Get and validate the project name
    project_name = validate_project_name(project_list)
    
    # Handle the project state transitions
    project_state = state.get(project_name, "off")  # Default to "off" if not in the state

    if project_state == "off":
        if active_project:
            print(f"Error: Project '{active_project}' is currently active. Please stop it before starting a new project.")
        else:
            action = "active"
            state[project_name] = "active"
            log_project_entry(project_name, action)
    elif project_state == "active":
        action = "off"
        state[project_name] = "off"
        log_project_entry(project_name, action)

    # Save the updated state
    save_state(state)

if __name__ == "__main__":
    main()
