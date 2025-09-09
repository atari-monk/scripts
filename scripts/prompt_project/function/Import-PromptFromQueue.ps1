function Import-PromptFromQueue {
    param(
        [Parameter(Mandatory=$true)]
        [string]$QueuePath
    )
    
    if (-not (Test-Path $QueuePath)) {
        throw "Queue file not found: $QueuePath"
    }
    
    try {
        $queueData = Get-Content -Path $QueuePath -Raw -Encoding UTF8 | ConvertFrom-Json
        
        if (-not $queueData -or $queueData.Count -eq 0) {
            Write-Warning "Queue is empty: $QueuePath"
            return $null
        }
        
        $queueItem = $queueData[0]
        
        $prompt = [Prompt]::new()
        
        if ($queueItem.PSObject.Properties['Task']) { $prompt.Task = $queueItem.Task }
        if ($queueItem.PSObject.Properties['Requirements']) { $prompt.Requirements = $queueItem.Requirements }
        if ($queueItem.PSObject.Properties['Paths']) { $prompt.Paths = $queueItem.Paths }
        if ($queueItem.PSObject.Properties['Role']) { $prompt.Role = $queueItem.Role }
        if ($queueItem.PSObject.Properties['OutputFormat']) { $prompt.OutputFormat = $queueItem.OutputFormat }
        if ($queueItem.PSObject.Properties['Reasoning']) { $prompt.Reasoning = $queueItem.Reasoning }
        if ($queueItem.PSObject.Properties['StopConditions']) { $prompt.StopConditions = $queueItem.StopConditions }
        if ($queueItem.PSObject.Properties['IncludeClipboard']) { $prompt.IncludeClipboard = $queueItem.IncludeClipboard }
        
        return $prompt
    }
    catch {
        Write-Error "Failed to load prompt from queue: $($_.Exception.Message)"
        return $null
    }
}