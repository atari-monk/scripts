# Function to get project file paths
function Get-ProjectFiles {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ProjectPath
    )
    
    $queuePath = Join-Path $ProjectPath "queue.json"
    $historyPath = Join-Path $ProjectPath "history.json"
    
    return @{
        QueuePath = $queuePath
        HistoryPath = $historyPath
        ProjectPath = $ProjectPath
    }
}