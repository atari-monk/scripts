import time
import sys
from pathlib import Path
from datetime import datetime
from typing import List

def load_tasks(file_path: Path) -> List[str]:
    """Load tasks from a text file, one per line."""
    if not file_path.is_file():
        print(f"Error: Task list file '{file_path}' not found.")
        sys.exit(1)
    with file_path.open('r', encoding='utf-8') as f:
        tasks = [line.strip() for line in f if line.strip()]
    return tasks

def init_log_file(log_path: Path) -> None:
    """Initialize the log file with headers."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open('w', encoding='utf-8') as f:
        f.write("Task Log with Timestamps\n")
        f.write("="*30 + "\n")

def append_to_log(log_path: Path, task: str, timestamp: str) -> None:
    """Append a single task entry to the log file."""
    with log_path.open('a', encoding='utf-8') as f:
        f.write(f"{task} -> {timestamp}\n")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: productivity-log <task_list_file.txt>")
        sys.exit(1)
    
    task_file = Path(sys.argv[1])
    tasks = load_tasks(task_file)
    
    # Create log path
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = (
        task_file.resolve().parent 
        / "log" 
        / f"{task_file.stem}_log_{timestamp_str}.txt"
    )
    
    # Initialize log file
    init_log_file(log_path)
    
    print(f"== Productivity Session for '{task_file}' ==")
    print(f"Log will be saved incrementally to: {log_path}")
    print("Press Enter to start or complete each task and log the timestamp.\n")
    
    for i, task in enumerate(tasks, start=1):
        input(f"Task {i}/{len(tasks)}: {task}\nPress Enter when ready to log timestamp...")
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        append_to_log(log_path, task, timestamp)
        print(f"✅ Timestamp logged: {timestamp}")
        print(f"💾 Entry appended to '{log_path}'\n")
    
    print("Session completed successfully!")

if __name__ == "__main__":
    main()