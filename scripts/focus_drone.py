import time
import os
import sys
from datetime import datetime
from typing import List, Tuple

def load_tasks(filename: str):
    """Load tasks from a text file, one per line."""
    if not os.path.isfile(filename):
        print(f"Error: Task list file '{filename}' not found.")
        sys.exit(1)
    with open(filename, 'r', encoding='utf-8') as f:
        tasks = [line.strip() for line in f if line.strip()]
    return tasks

def save_log(filename: str, timestamps: List[Tuple[str, str]]):
    """Save timestamps to a log file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Task Log with Timestamps\n")
        f.write("="*30 + "\n")
        for task, timestamp in timestamps:
            f.write(f"{task} -> {timestamp}\n")
    print(f"\n✅ Log saved to '{filename}'")

def main():
    if len(sys.argv) < 2:
        print("Usage: productivity-log <task_list_file.txt>")
        sys.exit(1)
    task_file = sys.argv[1]

    tasks = load_tasks(task_file)
    timestamps: List[Tuple[str, str]] = []
    
    print(f"== Productivity Session for '{task_file}' ==")
    print("Press Enter to start or complete each task and log the timestamp.\n")
    
    for i, task in enumerate(tasks, start=1):
        input(f"Task {i}/{len(tasks)}: {task}\nPress Enter when ready to log timestamp...")
        timestamps.append((task, time.strftime('%Y-%m-%d %H:%M:%S')))
        print(f"✅ Timestamp logged: {timestamps[-1][1]}\n")
    
    # Get the directory of the input file
    input_dir = os.path.dirname(os.path.abspath(task_file))
    base_name = os.path.splitext(os.path.basename(task_file))[0]
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(input_dir, f"{base_name}_log_{timestamp_str}.txt")
    
    save_log(log_filename, timestamps)

if __name__ == "__main__":
    main()