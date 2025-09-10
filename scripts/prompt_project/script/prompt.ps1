. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\model\Prompt.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Select-Template.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Import-PromptFromFile.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Import-PromptFromQueue.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Move-QueueToHistory.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Select-Project.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Get-ProjectFiles.ps1"
. "C:\Atari-Monk-Art\scripts\scripts\prompt_project\function\Merge-PromptFromQueue.ps1"

$selectedFile = Select-Template -TemplatePath "C:/Atari-Monk-Art/prompting/template" -FileFilter "*.json"
if ($selectedFile) {
    $prompt = Import-PromptFromFile -FilePath $selectedFile
    if ($prompt) {
        Write-Host "Loaded from template: Role=$($prompt.Role)" -ForegroundColor Green
        
        $projectsPath = "C:/Atari-Monk-Art/prompting"
        $selectedProjectPath = Select-Project -ProjectsPath $projectsPath
        
        if ($selectedProjectPath) {
            $projectFiles = Get-ProjectFiles -ProjectPath $selectedProjectPath
            $queuePath = $projectFiles.QueuePath
            $historyPath = $projectFiles.HistoryPath
            
            Write-Host "Project: $(Split-Path $selectedProjectPath -Leaf)" -ForegroundColor Cyan
            Write-Host "Queue: $queuePath" -ForegroundColor Cyan
            Write-Host "History: $historyPath" -ForegroundColor Cyan
            
            $prompt = Merge-PromptFromQueue -TemplatePrompt $prompt -QueuePath $queuePath -HistoryPath $historyPath
        } else {
            Write-Host "No project selected. Using template only." -ForegroundColor Yellow
        }
        
        $prompt = Ensure-TaskFromTemplate -Prompt $prompt -TemplateFilePath $selectedFile
        $prompt.Execute()
    }
}