# Function to move top prompt from queue to history file
function Move-QueueToHistory {
    param(
        [Parameter(Mandatory=$true)]
        [string]$QueuePath,
        [Parameter(Mandatory=$true)]
        [string]$HistoryPath,
        [switch]$RemoveFromQueue
    )
    
    if (-not (Test-Path $QueuePath)) {
        Write-Warning "Queue file not found: $QueuePath"
        return $false
    }
    
    try {
        # Load queue data - handle empty file case
        $queueContent = Get-Content -Path $QueuePath -Raw -Encoding UTF8
        if ([string]::IsNullOrWhiteSpace($queueContent) -or $queueContent.Trim() -eq "[]") {
            $queueData = @()
        } else {
            $queueData = $queueContent | ConvertFrom-Json
            # Ensure it's always an array, even if single object
            if ($queueData -isnot [array]) {
                $queueData = @($queueData)
            }
        }
        
        if (-not $queueData -or $queueData.Count -eq 0) {
            Write-Warning "Queue is empty: $QueuePath"
            return $false
        }
        
        # Get the top item (first in array)
        $topItem = $queueData[0]
        
        # Load or create history - handle empty file case
        $historyData = @()
        if (Test-Path $HistoryPath) {
            $historyContent = Get-Content -Path $HistoryPath -Raw -Encoding UTF8
            if (-not [string]::IsNullOrWhiteSpace($historyContent) -and $historyContent.Trim() -ne "[]") {
                $existingHistory = $historyContent | ConvertFrom-Json
                if ($existingHistory -is [array]) {
                    $historyData = $existingHistory
                } elseif ($existingHistory -ne $null) {
                    # Convert single object to array
                    $historyData = @($existingHistory)
                }
            }
        }
        
        # Add timestamp and empty Result field to the prompt item
        $topItemWithTimestamp = $topItem | Select-Object *
        $topItemWithTimestamp | Add-Member -NotePropertyName "ProcessedDate" -NotePropertyValue (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        $topItemWithTimestamp | Add-Member -NotePropertyName "Result" -NotePropertyValue ""
        
        # Add to history at the BOTTOM/END of the array
        $historyData = @($historyData) + @($topItemWithTimestamp)
        
        # FORCE history to always be an array, even with one item
        $jsonOutput = if ($historyData.Count -eq 0) {
            "[]"
        } else {
            ConvertTo-Json -InputObject @($historyData) -Depth 5
        }
        
        $jsonOutput | Out-File -FilePath $HistoryPath -Encoding UTF8 -Force
        
        # Remove from queue if requested
        if ($RemoveFromQueue) {
            $remainingQueue = $queueData | Select-Object -Skip 1
            # Ensure queue remains as array, even if empty
            $queueOutput = if ($remainingQueue.Count -eq 0) {
                "[]"
            } else {
                ConvertTo-Json -InputObject @($remainingQueue) -Depth 5
            }
            $queueOutput | Out-File -FilePath $QueuePath -Encoding UTF8 -Force
            Write-Host "Moved top item to history and removed from queue. Remaining items: $($remainingQueue.Count)" -ForegroundColor Green
        } else {
            Write-Host "Added top item to history. Queue remains unchanged." -ForegroundColor Green
        }
        
        return $true
    }
    catch {
        Write-Error "Failed to move queue item to history: $($_.Exception.Message)"
        return $false
    }
}