#!/usr/bin/env python3
"""
focus.py - Script to define lists of tasks and collect their time stats
Goal is to improve focus on task
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, List, Dict, Optional

# File paths
TASKS_FILE = Path("C:/Atari-Monk/scripts/data/focus-tasks.json")
LOGS_FILE = Path("C:/Atari-Monk/scripts/data/focus-logs.json")

# Type aliases
TaskListType = List[Dict[str, Any]]
LogsType = List[Dict[str, Any]]

def load_json(file_path: Path) -> List[Dict[str, Any]]:
    """Load JSON data from file, return empty list if file doesn't exist"""
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(file_path: Path, data: List[Dict[str, Any]]) -> None:
    """Save data to JSON file"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_current_time() -> str:
    """Return current time in YYYY-MM-DD HH:MM format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def create_task_list(name: str, description: str) -> None:
    """Create a new task list"""
    tasks: TaskListType = load_json(TASKS_FILE)
    
    # Check if name already exists
    if any(task_list["Name"] == name for task_list in tasks):
        print(f"Task list '{name}' already exists")
        return
    
    new_list: Dict[str, Any] = {
        "Name": name,
        "Description": description,
        "Tasks": []
    }
    tasks.append(new_list)
    save_json(TASKS_FILE, tasks)
    print(f"Created task list: {name}")

def add_task_to_list(list_name: str, task: str) -> None:
    """Add a task to an existing task list"""
    tasks: TaskListType = load_json(TASKS_FILE)
    
    for task_list in tasks:
        if task_list["Name"] == list_name:
            task_list["Tasks"].append({"Task": task})
            save_json(TASKS_FILE, tasks)
            print(f"Added task to {list_name}: {task}")
            return
    
    print(f"Task list '{list_name}' not found")

def start_session(list_name: str) -> None:
    """Start a new focus session with a task list"""
    tasks_data: TaskListType = load_json(TASKS_FILE)
    logs_data: LogsType = load_json(LOGS_FILE)
    
    # Find the task list
    task_list: Optional[Dict[str, Any]] = next(
        (tl for tl in tasks_data if tl["Name"] == list_name), None
    )
    if not task_list:
        print(f"Task list '{list_name}' not found")
        return
    
    if not task_list["Tasks"]:
        print(f"Task list '{list_name}' has no tasks")
        return
    
    # Check if there's already an active session
    active_session: Optional[Dict[str, Any]] = next(
        (log for log in logs_data if log.get("Active", False)), None
    )
    if active_session:
        print(f"Already active session: {active_session['Name']}")
        print("Use 'focus stop' to stop current session or 'focus next' to continue")
        return
    
    # Create new log entry
    log_name = f"{list_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    new_log: Dict[str, Any] = {
        "Name": log_name,
        "TaskList": list_name,
        "Active": True,
        "CurrentTaskIndex": 0,
        "Logs": []
    }
    
    # Initialize log for first task only
    new_log["Logs"].append({
        "TaskIndex": 0,
        "Start": get_current_time(),
        "Stop": "",
        "Minutes": 0
    })
    
    logs_data.append(new_log)
    save_json(LOGS_FILE, logs_data)
    
    print(f"Started session: {log_name}")
    print(f"Current task: {task_list['Tasks'][0]['Task']}")

def stop_session() -> None:
    """Stop the current active session"""
    logs_data: LogsType = load_json(LOGS_FILE)
    
    # Find active session
    active_session: Optional[Dict[str, Any]] = next(
        (log for log in logs_data if log.get("Active", False)), None
    )
    if not active_session:
        print("No active session found")
        return
    
    tasks_data: TaskListType = load_json(TASKS_FILE)
    task_list: Optional[Dict[str, Any]] = next(
        (tl for tl in tasks_data if tl["Name"] == active_session["TaskList"]), None
    )
    if not task_list:
        print("Error: Task list not found")
        return
    
    current_idx: int = active_session["CurrentTaskIndex"]
    
    # Update current task with stop time and calculate minutes
    if current_idx < len(active_session["Logs"]):
        current_log: Dict[str, Any] = active_session["Logs"][-1]  # Get last log entry
        if current_log["Start"] and not current_log["Stop"]:
            current_log["Stop"] = get_current_time()
            
            # Calculate minutes
            try:
                start_time = datetime.strptime(str(current_log["Start"]), "%Y-%m-%d %H:%M")
                stop_time = datetime.strptime(str(current_log["Stop"]), "%Y-%m-%d %H:%M")
                current_log["Minutes"] = int((stop_time - start_time).total_seconds() / 60)
            except ValueError:
                current_log["Minutes"] = 0
    
    # Deactivate session
    active_session["Active"] = False
    save_json(LOGS_FILE, logs_data)
    print(f"Stopped session: {active_session['Name']}")

def resume_session(list_name: str, log_name: str) -> None:
    """Resume a previously stopped session"""
    tasks_data: TaskListType = load_json(TASKS_FILE)
    logs_data: LogsType = load_json(LOGS_FILE)
    
    # Find the task list
    task_list: Optional[Dict[str, Any]] = next(
        (tl for tl in tasks_data if tl["Name"] == list_name), None
    )
    if not task_list:
        print(f"Task list '{list_name}' not found")
        return
    
    # Find the log
    log_entry: Optional[Dict[str, Any]] = next(
        (log for log in logs_data if log["Name"] == log_name and log["TaskList"] == list_name), None
    )
    if not log_entry:
        print(f"Log '{log_name}' not found for task list '{list_name}'")
        return
    
    if log_entry.get("Active", False):
        print(f"Session '{log_name}' is already active")
        return
    
    # Check if there's already an active session
    active_session: Optional[Dict[str, Any]] = next(
        (log for log in logs_data if log.get("Active", False)), None
    )
    if active_session:
        print(f"Already active session: {active_session['Name']}")
        print("Use 'focus stop' to stop current session first")
        return
    
    # Reactivate session
    log_entry["Active"] = True
    
    # If current task has no start time, start it
    current_idx: int = log_entry["CurrentTaskIndex"]
    if current_idx >= len(log_entry["Logs"]):
        # Need to create new log entry for current task
        log_entry["Logs"].append({
            "TaskIndex": current_idx,
            "Start": get_current_time(),
            "Stop": "",
            "Minutes": 0
        })
    else:
        current_log: Dict[str, Any] = log_entry["Logs"][-1]
        if not current_log["Start"]:
            current_log["Start"] = get_current_time()
        elif current_log["Stop"]:
            # Task was completed, need to start next task
            log_entry["Logs"].append({
                "TaskIndex": current_idx,
                "Start": get_current_time(),
                "Stop": "",
                "Minutes": 0
            })
    
    save_json(LOGS_FILE, logs_data)
    print(f"Resumed session: {log_name}")
    print(f"Current task: {task_list['Tasks'][current_idx]['Task']}")

def next_task() -> None:
    """Move to the next task in the active session"""
    logs_data: LogsType = load_json(LOGS_FILE)
    
    # Find active session
    active_session: Optional[Dict[str, Any]] = next(
        (log for log in logs_data if log.get("Active", False)), None
    )
    if not active_session:
        print("No active session found. Use 'focus start' to begin a session.")
        return
    
    tasks_data: TaskListType = load_json(TASKS_FILE)
    task_list: Optional[Dict[str, Any]] = next(
        (tl for tl in tasks_data if tl["Name"] == active_session["TaskList"]), None
    )
    if not task_list:
        print("Error: Task list not found")
        return
    
    current_idx: int = active_session["CurrentTaskIndex"]
    
    # Update current task with stop time and calculate minutes
    if current_idx < len(task_list["Tasks"]):
        # Find or create log entry for current task
        current_log: Optional[Dict[str, Any]] = next(
            (log for log in active_session["Logs"] if log["TaskIndex"] == current_idx), None
        )
        
        if current_log and current_log["Start"] and not current_log["Stop"]:
            current_log["Stop"] = get_current_time()
            
            # Calculate minutes
            try:
                start_time = datetime.strptime(str(current_log["Start"]), "%Y-%m-%d %H:%M")
                stop_time = datetime.strptime(str(current_log["Stop"]), "%Y-%m-%d %H:%M")
                current_log["Minutes"] = int((stop_time - start_time).total_seconds() / 60)
            except ValueError:
                current_log["Minutes"] = 0
    
    # Move to next task
    active_session["CurrentTaskIndex"] += 1
    next_idx: int = active_session["CurrentTaskIndex"]
    
    if next_idx < len(task_list["Tasks"]):
        # Create new log entry for next task
        active_session["Logs"].append({
            "TaskIndex": next_idx,
            "Start": get_current_time(),
            "Stop": "",
            "Minutes": 0
        })
        save_json(LOGS_FILE, logs_data)
        print(f"Next task: {task_list['Tasks'][next_idx]['Task']}")
    else:
        # Session complete
        active_session["Active"] = False
        save_json(LOGS_FILE, logs_data)
        print("Session complete! All tasks finished.")

def list_task_lists() -> None:
    """Print all task lists and their log names"""
    tasks_data: TaskListType = load_json(TASKS_FILE)
    logs_data: LogsType = load_json(LOGS_FILE)
    
    print("Task Lists and their Logs:")
    for task_list in tasks_data:
        logs: List[Dict[str, Any]] = [
            log for log in logs_data if log["TaskList"] == task_list["Name"]
        ]
        print(f"\n{task_list['Name']} - {task_list['Description']}")
        print(f"  Tasks: {len(task_list['Tasks'])}")
        
        if logs:
            print("  Logs:")
            for log in logs:
                status = "Active" if log.get("Active", False) else "Completed"
                print(f"    - {log['Name']} ({status})")
        else:
            print("  No logs yet")

def show_stats(list_name: Optional[str] = None, log_name: Optional[str] = None) -> None:
    """Show statistics for task lists and logs"""
    tasks_data: TaskListType = load_json(TASKS_FILE)
    logs_data: LogsType = load_json(LOGS_FILE)
    
    if not list_name and not log_name:
        list_task_lists()
    
    elif list_name and not log_name:
        # Show logs for specific task list
        task_list: Optional[Dict[str, Any]] = next(
            (tl for tl in tasks_data if tl["Name"] == list_name), None
        )
        if not task_list:
            print(f"Task list '{list_name}' not found")
            return
            
        logs: List[Dict[str, Any]] = [
            log for log in logs_data if log["TaskList"] == list_name
        ]
        
        print(f"Task List: {list_name}")
        print(f"Description: {task_list['Description']}")
        print(f"Tasks: {len(task_list['Tasks'])}")
        
        for i, task in enumerate(task_list["Tasks"], 1):
            print(f"  {i}. {task['Task']}")
        
        if logs:
            print(f"\nLogs for '{list_name}':")
            for log in logs:
                status = "Active" if log.get("Active", False) else "Completed"
                total_minutes = sum(task_log.get("Minutes", 0) for task_log in log["Logs"])
                completed_tasks = sum(1 for task_log in log["Logs"] if task_log.get("Stop"))
                print(f"  - {log['Name']} ({status}, {completed_tasks}/{len(task_list['Tasks'])} tasks, {total_minutes}min total)")
        else:
            print(f"\nNo logs found for task list '{list_name}'")
    
    elif list_name and log_name:
        # Show detailed stats for specific log
        log: Optional[Dict[str, Any]] = next(
            (l for l in logs_data if l["Name"] == log_name and l["TaskList"] == list_name), None
        )
        if not log:
            print(f"Log '{log_name}' not found for task list '{list_name}'")
            return
            
        task_list: Optional[Dict[str, Any]] = next(
            (tl for tl in tasks_data if tl["Name"] == list_name), None
        )
        if not task_list:
            print(f"Task list '{list_name}' not found")
            return
        
        print(f"Detailed stats for {log_name}:")
        print(f"Task List: {list_name}")
        print(f"Status: {'Active' if log.get('Active', False) else 'Completed'}")
        
        total_minutes: int = 0
        completed_tasks: int = 0
        
        for i, task in enumerate(task_list["Tasks"], 1):
            # Find all log entries for this task index
            task_logs = [tl for tl in log["Logs"] if tl["TaskIndex"] == i-1]
            
            if task_logs:
                task_total_minutes = sum(tl.get("Minutes", 0) for tl in task_logs)
                total_minutes += task_total_minutes
                
                completed = any(tl.get("Stop") for tl in task_logs)
                if completed:
                    completed_tasks += 1
                    status = f"Completed ({task_total_minutes}min)"
                elif any(tl.get("Start") and not tl.get("Stop") for tl in task_logs):
                    status = "In progress"
                else:
                    status = "Not started"
            else:
                status = "Not started"
            
            print(f"  Task {i}: {task['Task']} - {status}")
        
        print(f"\nSummary: {completed_tasks}/{len(task_list['Tasks'])} tasks completed")
        print(f"Total time: {total_minutes} minutes")

def open_file() -> None:
    """Open the data file in editor"""
    # Let user choose which file to open
    print("Which file would you like to open?")
    print("1. Tasks file (focus-tasks.json)")
    print("2. Logs file (focus-logs.json)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        file_path = TASKS_FILE
    elif choice == "2":
        file_path = LOGS_FILE
    else:
        print("Invalid choice")
        return
    
    if file_path.exists():
        os.system(f'start "" "{file_path}"')  # Windows
        print(f"Opened: {file_path}")
    else:
        print(f"File not found: {file_path}")

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Focus task management tool",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # create-list command
    create_list_parser = subparsers.add_parser('create-list', aliases=['cl'], 
                                             help='Create new task list')
    create_list_parser.add_argument('name', help='Task list name')
    create_list_parser.add_argument('description', help='Task list description')
    
    # create-task command  
    create_task_parser = subparsers.add_parser('create-task', aliases=['ct'],
                                             help='Add task to task list')
    create_task_parser.add_argument('list_name', help='Task list name')
    create_task_parser.add_argument('task', help='Task description')
    
    # start command
    start_parser = subparsers.add_parser('start', aliases=['s'],
                                       help='Start focus session with task list')
    start_parser.add_argument('list_name', help='Task list name to start')
    
    # stop command
    subparsers.add_parser('stop', help='Stop current session')
    
    # resume command
    resume_parser = subparsers.add_parser('resume', aliases=['r'],
                                        help='Resume a session')
    resume_parser.add_argument('list_name', help='Task list name')
    resume_parser.add_argument('log_name', help='Log name to resume')
    
    # next command
    subparsers.add_parser('next', aliases=['n'],
                          help='Move to next task in active session')
    
    # list command
    subparsers.add_parser('list', aliases=['l'],
                          help='List task lists and their logs')
    
    # stats command
    stats_parser = subparsers.add_parser('stats', aliases=['st'],
                                       help='Show statistics')
    stats_parser.add_argument('list_name', nargs='?', help='Task list name')
    stats_parser.add_argument('log_name', nargs='?', help='Log name')
    
    # file command
    subparsers.add_parser('file', aliases=['f'],
                          help='Open data file in editor')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command in ['create-list', 'cl']:
            create_task_list(args.name, args.description)
        
        elif args.command in ['create-task', 'ct']:
            add_task_to_list(args.list_name, args.task)
        
        elif args.command in ['start', 's']:
            start_session(args.list_name)
        
        elif args.command == 'stop':
            stop_session()
        
        elif args.command in ['resume', 'r']:
            resume_session(args.list_name, args.log_name)
        
        elif args.command in ['next', 'n']:
            next_task()
        
        elif args.command in ['list', 'l']:
            list_task_lists()
        
        elif args.command in ['stats', 'st']:
            show_stats(args.list_name, args.log_name)
        
        elif args.command in ['file', 'f']:
            open_file()
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()