import os
from datetime import datetime

# Constants
LOG_FILE_PATH = "C:/atari-monk/code/apollo/content/Database/log_project.md"
INITIAL_CONTENT = "# Log Project\n"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def initialize_log_file():
    """Check if the log file exists; if not, create it with initial content."""
    if not os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'w') as file:
            file.write(INITIAL_CONTENT)
        print(f"Log file created: {LOG_FILE_PATH}")
    else:
        print(f"Log file already exists: {LOG_FILE_PATH}")

def get_project_name():
    """Prompt the user to input a valid project name."""
    while True:
        project_name = input("Enter the project name: ").strip()
        if project_name:
            return project_name
        print("Project name cannot be empty. Please try again.")

def log_project_entry(project_name):
    """Log the project entry to the markdown file."""
    timestamp = datetime.now().strftime(DATE_FORMAT)
    entry = f"{timestamp} {project_name}\n"
    
    with open(LOG_FILE_PATH, 'a') as file:
        file.write(entry)
    
    print(f"Logged: {entry.strip()}")

def main():
    """Main function to handle the project logging."""
    initialize_log_file()
    
    project_name = get_project_name()
    log_project_entry(project_name)

if __name__ == "__main__":
    main()
