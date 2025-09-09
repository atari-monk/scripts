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
        $queueContent = Get-Content -Path $QueuePath -Raw -Encoding UTF8
        if ([string]::IsNullOrWhiteSpace($queueContent) -or $queueContent.Trim() -eq "[]") {
            $queueData = @()
        } else {
            $queueData = $queueContent | ConvertFrom-Json
            if ($queueData -isnot [array]) {
                $queueData = @($queueData)
            }
        }
        
        if (-not $queueData -or $queueData.Count -eq 0) {
            Write-Warning "Queue is empty: $QueuePath"
            return $false
        }
        
        $topItem = $queueData[0]
        
        $historyData = @()
        if (Test-Path $HistoryPath) {
            $historyContent = Get-Content -Path $HistoryPath -Raw -Encoding UTF8
            if (-not [string]::IsNullOrWhiteSpace($historyContent) -and $historyContent.Trim() -ne "[]") {
                $existingHistory = $historyContent | ConvertFrom-Json
                if ($existingHistory -is [array]) {
                    $historyData = $existingHistory
                } elseif ($existingHistory -ne $null) {
                    $historyData = @($existingHistory)
                }
            }
        }
        
        $topItemWithTimestamp = $topItem | Select-Object *
        $topItemWithTimestamp | Add-Member -NotePropertyName "ProcessedDate" -NotePropertyValue (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        $topItemWithTimestamp | Add-Member -NotePropertyName "Result" -NotePropertyValue ""
        
        $historyData = @($historyData) + @($topItemWithTimestamp)
        
        $jsonOutput = if ($historyData.Count -eq 0) {
            "[]"
        } else {
            ConvertTo-Json -InputObject @($historyData) -Depth 5
        }
        
        $jsonOutput | Out-File -FilePath $HistoryPath -Encoding UTF8 -Force
        
        if ($RemoveFromQueue) {
            $remainingQueue = $queueData | Select-Object -Skip 1
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