import os
import re
from datetime import datetime

# Constants for folder and file names
LOG_FOLDER = "C:/atari-monk/code/apollo/content/Database"  # Replace with your log folder path
LOG_FILE = "log_project.txt"  # Replace with your log file name
OUTPUT_FILE = "log_project.md"  # Output file name

def convert_log_to_markdown(log_lines):
    # Initialize a dictionary to hold logs grouped by day
    logs_by_day = {}

    # Process each log line
    last_active_date = None  # Track the last date a project was active
    
    for line in log_lines:
        # Adjust regex to match time without seconds
        match = re.match(r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) (.+) \((active|off)\)', line.strip())
        if match:
            date_str, time_str, project, status = match.groups()
            time = datetime.strptime(time_str, "%H:%M").time()
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # If the task is marked as "off" and the time is after midnight
            if status == "off" and time < datetime.strptime("06:00", "%H:%M").time():
                # Check if there was an active project on the previous day
                if last_active_date is not None:
                    # Assign the task to the previous day's date
                    date = last_active_date

            # Add to the logs dictionary
            if date not in logs_by_day:
                logs_by_day[date] = []

            logs_by_day[date].append((time_str, project, status))

            # Update the last active date when a project becomes active
            if status == "active":
                last_active_date = date

    # Create Markdown output
    markdown_output = "# Log Project\n\n"

    for date in sorted(logs_by_day.keys()):
        month = date.strftime("%Y.%m")
        day = date.day

        markdown_output += f"## {month}\n\n### {day}\n\n"
        
        # Store projects with timestamps
        projects = {}
        for time_str, project, status in logs_by_day[date]:
            if project not in projects:
                projects[project] = []
            if status == "active":
                projects[project].append([time_str])  # Start a new interval
            elif status == "off":
                if projects[project] and isinstance(projects[project][-1], list):
                    projects[project][-1].append(time_str)  # Close the interval

        for idx, (project, intervals) in enumerate(projects.items(), 1):
            time_ranges = []
            for interval in intervals:
                if len(interval) == 2:
                    time_ranges.append(f"{interval[0]} - {interval[1]}")
                else:  # Should not happen, but just in case
                    time_ranges.append(interval[0])

            time_range_output = ', '.join(time_ranges)
            markdown_output += f"{idx}. {project}\n\n{time_range_output}\n\n"

    return markdown_output.strip()

def read_log_file(file_path):
    """Read log lines from the specified file."""
    with open(file_path, 'r') as file:
        return file.readlines()

def write_output_file(output_path, content):
    """Write the Markdown content to the specified output file."""
    with open(output_path, 'w') as file:
        file.write(content)

# Load log lines from the specified file
log_file_path = os.path.join(LOG_FOLDER, LOG_FILE)
log_lines = read_log_file(log_file_path)

# Convert to Markdown format
markdown_result = convert_log_to_markdown(log_lines)

# Print the Markdown output to console
print(markdown_result)

# Write the Markdown output to a file
output_file_path = os.path.join(LOG_FOLDER, OUTPUT_FILE)
write_output_file(output_file_path, markdown_result)

print(f"Output written to {output_file_path}")
