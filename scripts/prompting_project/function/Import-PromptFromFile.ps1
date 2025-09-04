function Import-PromptFromFile {
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath
    )
    
    if (-not (Test-Path $FilePath)) {
        throw "File not found: $FilePath"
    }
    
    try {
        $jsonData = Get-Content -Path $FilePath -Raw -Encoding UTF8 | ConvertFrom-Json
        
        $prompt = [Prompt]::new()
        
        # Required fields
        $prompt.Role = $jsonData.Role
        $prompt.Task = $jsonData.Task
        $prompt.OutputFormat = $jsonData.OutputFormat
        
        # Optional fields
        $prompt.Reasoning = $jsonData.Reasoning
        $prompt.StopConditions = $jsonData.StopConditions
        $prompt.Paths = $jsonData.Paths
        $prompt.Requirements = $jsonData.Requirements
        
        return $prompt
    }
    catch {
        Write-Error "Failed to load prompt from file: $($_.Exception.Message)"
        return $null
    }
}