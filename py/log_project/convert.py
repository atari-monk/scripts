import os
from datetime import datetime

# Constants
INPUT_FOLDER = 'C:/atari-monk/code/apollo/content/Database'  # Update to your input folder
INPUT_FILE = 'log_project.txt'  # Replace with your actual log file name
OUTPUT_FILE = 'log_project.md'

def convert_log_format(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Initialize a dictionary to store project data
    project_data = {}

    # Parse log lines directly
    for line in lines:
        if line.strip():  # Check if the line is not empty
            try:
                date_time_str, project_status = line.strip().split(' ', 1)
                project_name, status = project_status.rsplit(' ', 1)

                # Convert to datetime object
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
                year = date_time.year
                month = date_time.month
                time = date_time.strftime('%H:%M')

                if project_name not in project_data:
                    project_data[project_name] = []
                
                # Append start/end time based on status
                if status == '(active)':
                    project_data[project_name].append(f"{time} - ")
                else:
                    if project_data[project_name] and project_data[project_name][-1].endswith('- '):
                        project_data[project_name][-1] += time

            except ValueError as e:
                print(f"Error parsing line: {line.strip()}. Error: {e}")

    # Generate output
    output_lines = [f"# Log Project\n\n## {year}\n\n# {month}\n"]
    for i, (project_name, times) in enumerate(project_data.items(), start=1):
        time_ranges = ''.join(times).strip()
        output_lines.append(f"{i}. {project_name}\n\n{time_ranges.strip(', ')}\n")

    # Write output to file
    with open(output_file, 'w') as file:
        file.writelines(output_lines)

if __name__ == "__main__":
    input_file_path = os.path.join(INPUT_FOLDER, INPUT_FILE)
    convert_log_format(input_file_path, OUTPUT_FILE)
    print(f"Converted log has been saved to {OUTPUT_FILE}.")
