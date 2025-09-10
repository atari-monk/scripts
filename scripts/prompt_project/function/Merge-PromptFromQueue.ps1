function Merge-PromptFromQueue {
    param(
        [Parameter(Mandatory=$true)]
        [Prompt]$TemplatePrompt,
        [Parameter(Mandatory=$true)]
        [string]$QueuePath,
        [Parameter(Mandatory=$true)]
        [string]$HistoryPath
    )
    
    if (-not (Test-Path $QueuePath)) {
        Write-Host "Queue file not found in project." -ForegroundColor Yellow
        return $TemplatePrompt
    }
    
    $queueData = Get-Content -Path $QueuePath -Raw -Encoding UTF8 | ConvertFrom-Json
    if (-not $queueData -or $queueData.Count -eq 0) {
        Write-Host "Queue is empty." -ForegroundColor Yellow
        return $TemplatePrompt
    }
    
    Write-Host "Queue detected with $($queueData.Count) items. Merging queue data..." -ForegroundColor Yellow
    
    $queuePrompt = Import-PromptFromQueue -QueuePath $QueuePath
    if (-not $queuePrompt) {
        return $TemplatePrompt
    }
    
    if ($queuePrompt.Task) { $TemplatePrompt.Task = $queuePrompt.Task }
    if ($queuePrompt.Requirements) { $TemplatePrompt.Requirements = $queuePrompt.Requirements }
    if ($queuePrompt.Paths) { $TemplatePrompt.Paths = $queuePrompt.Paths }
    if ($queuePrompt.Reasoning) { $TemplatePrompt.Reasoning = $queuePrompt.Reasoning }
    if ($queuePrompt.StopConditions) { $TemplatePrompt.StopConditions = $queuePrompt.StopConditions }
    if ($queuePrompt.IncludeClipboard) { $TemplatePrompt.IncludeClipboard = $queuePrompt.IncludeClipboard }
    
    Write-Host "Merged queue data into template" -ForegroundColor Green
    Write-Host "Task: $($TemplatePrompt.Task)" -ForegroundColor Cyan
    Write-Host "Requirements: $($TemplatePrompt.Requirements.Count)" -ForegroundColor Cyan
    Write-Host "Paths: $($TemplatePrompt.Paths.Count)" -ForegroundColor Cyan
    Write-Host "Include Clipboard: $($TemplatePrompt.IncludeClipboard)" -ForegroundColor Cyan
    
    return $TemplatePrompt
}

function Ensure-TaskFromTemplate {
    param(
        [Parameter(Mandatory=$true)]
        [Prompt]$Prompt,
        [Parameter(Mandatory=$true)]
        [string]$TemplateFilePath
    )
    
    if ($Prompt.Task) {
        return $Prompt
    }
    
    $templatePrompt = Import-PromptFromFile -FilePath $TemplateFilePath
    if ($templatePrompt -and $templatePrompt.Task) {
        $Prompt.Task = $templatePrompt.Task
        Write-Host "Using template task: $($Prompt.Task)" -ForegroundColor Cyan
    }
    
    return $Prompt
}