. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\model\Prompt.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\function\Select-Template.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\function\Import-PromptFromFile.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\function\Import-PromptFromQueue.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\function\Move-QueueToHistory.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\function\Select-Project.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompting_project\function\Get-ProjectFiles.ps1"

# First, load from template
$selectedFile = Select-Template -TemplatePath "C:/Atari-Monk-Art/prompting/template" -FileFilter "*.json"
if ($selectedFile) {
    $prompt = Import-PromptFromFile -FilePath $selectedFile
    if ($prompt) {
        Write-Host "Loaded from template: Role=$($prompt.Role)" -ForegroundColor Green
        
        # Select project folder
        $projectsPath = "C:/Atari-Monk-Art/prompting"
        $selectedProjectPath = Select-Project -ProjectsPath $projectsPath
        
        if ($selectedProjectPath) {
            # Get project file paths
            $projectFiles = Get-ProjectFiles -ProjectPath $selectedProjectPath
            $queuePath = $projectFiles.QueuePath
            $historyPath = $projectFiles.HistoryPath
            
            Write-Host "Project: $(Split-Path $selectedProjectPath -Leaf)" -ForegroundColor Cyan
            Write-Host "Queue: $queuePath" -ForegroundColor Cyan
            Write-Host "History: $historyPath" -ForegroundColor Cyan
            
            # Check if queue exists and has items
            if (Test-Path $queuePath) {
                $queueData = Get-Content -Path $queuePath -Raw -Encoding UTF8 | ConvertFrom-Json
                if ($queueData -and $queueData.Count -gt 0) {
                    Write-Host "Queue detected with $($queueData.Count) items. Merging queue data..." -ForegroundColor Yellow
                    
                    # Load from queue and merge with template
                    $queuePrompt = Import-PromptFromQueue -QueuePath $queuePath
                    if ($queuePrompt) {
                        # Override template fields with queue data
                        if ($queuePrompt.Task) { $prompt.Task = $queuePrompt.Task }
                        if ($queuePrompt.Requirements) { $prompt.Requirements = $queuePrompt.Requirements }
                        if ($queuePrompt.Paths) { $prompt.Paths = $queuePrompt.Paths }
                        if ($queuePrompt.Reasoning) { $prompt.Reasoning = $queuePrompt.Reasoning }
                        if ($queuePrompt.StopConditions) { $prompt.StopConditions = $queuePrompt.StopConditions }
                        
                        Write-Host "Merged queue data into template" -ForegroundColor Green
                        Write-Host "Task: $($prompt.Task)" -ForegroundColor Cyan
                        Write-Host "Requirements: $($prompt.Requirements.Count)" -ForegroundColor Cyan
                        Write-Host "Paths: $($prompt.Paths.Count)" -ForegroundColor Cyan
                        
                        # Move the processed item to history
                        $moved = Move-QueueToHistory -QueuePath $queuePath -HistoryPath $historyPath -RemoveFromQueue
                        if ($moved) {
                            Write-Host "Queue item moved to history" -ForegroundColor Green
                        }
                    }
                } else {
                    Write-Host "Queue is empty." -ForegroundColor Yellow
                }
            } else {
                Write-Host "Queue file not found in project." -ForegroundColor Yellow
            }
        } else {
            Write-Host "No project selected. Using template only." -ForegroundColor Yellow
        }
        
        # Process the prompt...
        $prompt.Execute()
    }
}