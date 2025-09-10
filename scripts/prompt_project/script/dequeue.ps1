. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\model\Prompt.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Import-PromptFromQueue.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Move-QueueToHistory.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Select-Project.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Get-ProjectFiles.ps1"

$projectsPath = "C:/Atari-Monk-Art/prompting"
$selectedProjectPath = Select-Project -ProjectsPath $projectsPath

if ($selectedProjectPath) {
    $projectFiles = Get-ProjectFiles -ProjectPath $selectedProjectPath
    $queuePath = $projectFiles.QueuePath
    $historyPath = $projectFiles.HistoryPath
    
    Write-Host "Project: $(Split-Path $selectedProjectPath -Leaf)" -ForegroundColor Cyan
    Write-Host "Queue: $queuePath" -ForegroundColor Cyan
    Write-Host "History: $historyPath" -ForegroundColor Cyan
    
    $queuePrompt = Import-PromptFromQueue -QueuePath $queuePath
    if ($queuePrompt) {
        $moved = Move-QueueToHistory -QueuePath $queuePath -HistoryPath $historyPath -RemoveFromQueue
        if ($moved) {
            Write-Host "Queue item moved to history" -ForegroundColor Green
        }
    }
}