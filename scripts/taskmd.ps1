param([string]$command)

# ============================
# CONFIG
# ============================

$TaskFile = "C:\Atari-Monk\logs\task-2025.md"

# Map emojis to console colors
$EmojiColors = @{
    "🔴" = "Red"
    "🟡" = "Yellow"
    "🟢" = "Green"
    "🔵" = "Blue"
}

# ============================
# CORE DISPATCHER
# ============================

function Dispatch-TaskMagic {
    param($cmd)

    if (-not $cmd) {
        Show-Help
        exit 0
    }

    switch ($cmd.ToLower()) {
        "next"  { Show-NextTask $TaskFile }
        "done"  { Mark-NextTaskDone $TaskFile }
        "add"   { Add-TaskInteractive $TaskFile }
        "list"  { List-Tasks $TaskFile }
        default {
            Write-Host "Unknown command '$cmd'. Run the script with no arguments to see commands." -ForegroundColor Red
            exit 1
        }
    }
}

# ============================
# HELPER FUNCTIONS
# ============================

function Show-Help {
    Write-Host "Usage: magic task <command>" -ForegroundColor Cyan
    Write-Host "Commands:"
    Write-Host "- next  : Show the next incomplete task with priority"
    Write-Host "- done  : Mark the next incomplete task as done"
    Write-Host "- add   : Add a new task with optional emoji/label"
    Write-Host "- list  : List all tasks with color-coded priorities"
}

function Get-Tasks {
    param($file)
    if (-not (Test-Path $file)) {
        New-Item -Path $file -ItemType File | Out-Null
    }
    return Get-Content $file
}

function Write-Tasks {
    param($file, $tasks)
    Set-Content -Path $file -Value $tasks
}

function Get-EmojiColor {
    param($emoji)
    if ($EmojiColors.ContainsKey($emoji)) {
        return $EmojiColors[$emoji]
    } else {
        return "White"
    }
}

# ============================
# COMMAND FUNCTIONS
# ============================

function Show-NextTask {
    param($file)
    $tasks = Get-Tasks $file
    $next = $tasks | Where-Object { $_ -match "^\s*-\s\[\s\]\s" } | Select-Object -First 1
    if ($next) {
        $taskText = $next -replace "^\s*-\s\[\s\]\s", ""
        $emoji = ($taskText -match "^(.)\s") ? $matches[1] : ""
        $color = Get-EmojiColor $emoji
        Write-Host "🔹 Next task: $taskText" -ForegroundColor $color
    } else {
        Write-Host "✅ No incomplete tasks found!" -ForegroundColor Green
    }
}

function Mark-NextTaskDone {
    param($file)
    $tasks = Get-Tasks $file
    $found = $false
    for ($i=0; $i -lt $tasks.Count; $i++) {
        if ($tasks[$i] -match "^\s*-\s\[\s\]\s") {
            $taskText = $tasks[$i] -replace "^\s*-\s\[\s\]\s", ""
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
            $tasks[$i] = "- [x] $taskText (done: $timestamp)"
            Write-Tasks $file $tasks
            Write-Host "✅ Task completed: $taskText" -ForegroundColor Green
            $found = $true
            break
        }
    }
    if (-not $found) {
        Write-Host "No incomplete tasks to mark as done!" -ForegroundColor Cyan
    }
}

function Add-TaskInteractive {
    param($file)
    $emoji = Read-Host "Enter emoji/label for priority (🔴/🟡/🟢) or leave empty"
    $desc = Read-Host "Enter new task description"
    if (-not [string]::IsNullOrWhiteSpace($desc)) {
        $line = if ($emoji) { "- [ ] $emoji $desc" } else { "- [ ] $desc" }
        Add-Content $file $line
        Write-Host "➕ Task added: $line" -ForegroundColor Cyan
    } else {
        Write-Host "No task entered, nothing added." -ForegroundColor Yellow
    }
}

function List-Tasks {
    param($file)
    $tasks = Get-Tasks $file
    if ($tasks.Count -eq 0) {
        Write-Host "No tasks found." -ForegroundColor Cyan
        return
    }
    Write-Host "`nTasks in ${file}:" -ForegroundColor Cyan
    foreach ($line in $tasks) {
        if ($line -match "^\s*-\s\[\s\]\s") {
            $taskText = $line -replace "^\s*-\s\[\s\]\s", ""
            $emoji = ($taskText -match "^(.)\s") ? $matches[1] : ""
            $color = Get-EmojiColor $emoji
            Write-Host "🔹 $taskText" -ForegroundColor $color
        } elseif ($line -match "^\s*-\s\[x\]\s") {
            Write-Host "✅ $line" -ForegroundColor Green
        } else {
            Write-Host "$line"
        }
    }
}

# ============================
# RUN DISPATCHER
# ============================

Dispatch-TaskMagic $command
