# focus.py

- Script to define lists of tasks and collect their time stats
- Goal is to improve focus on task

## Cli api

```sh
focus create-list TaskListName Description # create new TaskList
focus create-task TaskListName Task # add task to named TaskList
focus start TaskListName # print first task, update stats
focus stop # stop current task
focus resume TaskListName LogName # Resumes TaskList with named log
focus next # print next task, update stats
focus list # print TaskList names and their log names
focus stats TaskListName LogName # print stats for named
focus file # open file in editor
```

Define also shorter aliases for commands

## Workflow:
1. `focus start -s TaskListName`
   - Sets active log
   - Creates log entry with Start time for **first task** (index 0)
   - Prints the first task

2. `focus next -n`
   - Checks for active log 
   - Writes Stop time for **current task**
   - Calculates Minutes for completed task
   - Moves to next task (increment CurrentTaskIndex)
   - Writes Start time for **new current task**
   - Prints the new current task

3. Repeat `focus next -n` until all tasks completed

This gives a **complete log chain** where each task gets its full Start→Stop→Minutes data automatically.  
When state is worng next informs there is no session.  
When all tasks in a list are completed:
- Set `Active: false` when `CurrentTaskIndex` reaches the end
- Inform user that session is complete
Make sure we can stop current task and resume later.  
That means task can have many log records with it's index.

## File

- C:\Atari-Monk\scripts\data\focus-tasks.json
- C:\Atari-Monk\scripts\data\focus-logs.json
- Names are unique
- TaskList in Logs is Name form TaskList
- Each task has it's log record

focus-tasks.json - tasks dictionary

```json
[
    {
        "Name": "",
        "Description": "",
        "Tasks": [
            {
                "Task": ""
            }
        ]
    }
]
```

focus-logs.json - loging on session with task list

```json
[
    {
        "Name": "",
        "TaskList":"",
        "Active": true,
        "CurrentTaskIndex": 0,
        "Logs": [
                {
                    "TaskIndex": 0, 
                    "Start": "YYYY-MM-DD HH:MM",
                    "Stop": "YYYY-MM-DD HH:MM",
                    "Minutes": 0
                }
            ]
    }
]
```
