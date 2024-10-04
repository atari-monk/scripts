import os
import json
from datetime import datetime

# Constants
LOG_FILE_PATH = "project_log.md"
PROJECT_LIST_PATH = "projects.json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
INITIAL_CONTENT = "# Log Project\n"
STATE_FILE = "state.json"

# Initialize the log file if it doesn't exist
def initialize_log_file():
    """Check if the log file exists; if not, create it with initial content."""
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w') as file:
            file.write(INITIAL_CONTENT)
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
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Save the current state to a file
def save_state(state):
    """Save the internal state back to the state JSON file."""
    with open(STATE_FILE, 'w') as file:
        json.dump(state, file)

# Log the project entry (either start or end)
def log_project_entry(project_name, is_start):
    """Log the project start or end entry to the markdown file."""
    timestamp = datetime.now().strftime(DATE_FORMAT)
    action = "start" if is_start else "end"
    entry = f"{timestamp} {project_name} ({action})\n"
    
    with open(LOG_FILE_PATH, 'a') as file:
        file.write(entry)
    
    print(f"Logged: {entry.strip()}")

def main():
    """Main function to handle project logging."""
    initialize_log_file()
    
    # Load the project list
    project_list = load_project_list()
    if not project_list:
        return  # Exit if the project list couldn't be loaded

    # Load the internal state
    state = load_state()

    # Get and validate the project name
    project_name = validate_project_name(project_list)
    
    # Determine if the project is starting or ending
    if project_name not in state:
        is_start = True  # Start the project if it's not in the state
        state[project_name] = 'start'
    else:
        is_start = state[project_name] == 'start'
        state[project_name] = 'end' if is_start else 'start'  # Toggle the state

    # Log the entry
    log_project_entry(project_name, is_start)

    # Save the updated state
    save_state(state)

if __name__ == "__main__":
    main()
