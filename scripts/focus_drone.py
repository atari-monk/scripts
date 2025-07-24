import time
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

def load_tasks(file_path: Path) -> List[str]:
    """Load tasks from a text file, one per line."""
    if not file_path.is_file():
        print(f"Error: Task list file '{file_path}' not found.")
        sys.exit(1)
    with file_path.open('r', encoding='utf-8') as f:
        tasks = [line.strip() for line in f if line.strip()]
    return tasks

def save_log(log_path: Path, timestamps: List[Tuple[str, str]]) -> None:
    """Save timestamps to a log file."""
    log_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    
    with log_path.open('w', encoding='utf-8') as f:
        f.write("Task Log with Timestamps\n")
        f.write("="*30 + "\n")
        for task, timestamp in timestamps:
            f.write(f"{task} -> {timestamp}\n")
    print(f"\n✅ Log saved to '{log_path}'")

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: productivity-log <task_list_file.txt>")
        sys.exit(1)
    
    task_file = Path(sys.argv[1])
    tasks = load_tasks(task_file)
    timestamps: List[Tuple[str, str]] = []
    
    print(f"== Productivity Session for '{task_file}' ==")
    print("Press Enter to start or complete each task and log the timestamp.\n")
    
    for i, task in enumerate(tasks, start=1):
        input(f"Task {i}/{len(tasks)}: {task}\nPress Enter when ready to log timestamp...")
        timestamps.append((task, time.strftime('%Y-%m-%d %H:%M:%S')))
        print(f"✅ Timestamp logged: {timestamps[-1][1]}\n")
    
    # Create log path using Path operations
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = (
        task_file.resolve().parent 
        / "log" 
        / f"{task_file.stem}_log_{timestamp_str}.txt"
    )
    
    save_log(log_path, timestamps)

if __name__ == "__main__":
    main()