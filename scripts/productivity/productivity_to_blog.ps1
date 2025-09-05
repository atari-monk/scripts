$ErrorActionPreference = "Stop"

function Remove-ExistingLogs {
    param (
        [string]$LogsPath
    )
    
    if (-not (Test-Path -Path $LogsPath)) {
        Write-Host "Logs directory does not exist, skipping removal."
        return
    }
    
    Get-ChildItem -Path $LogsPath -Filter "*.md" | ForEach-Object {
        try {
            Remove-Item -Path $_.FullName -Force
            Write-Host "Removed: $($_.FullName)"
        }
        catch {
            Write-Error "Failed to remove $($_.FullName): $($_.Exception.Message)"
            throw
        }
    }
}

function Move-LogFiles {
    param (
        [string]$SourcePath,
        [string]$DestinationPath
    )
    
    if (-not (Test-Path -Path $SourcePath)) {
        throw "Source directory does not exist: $SourcePath"
    }
    
    if (-not (Test-Path -Path $DestinationPath)) {
        New-Item -Path $DestinationPath -ItemType Directory -Force | Out-Null
        Write-Host "Created destination directory: $DestinationPath"
    }
    
    Get-ChildItem -Path $SourcePath -Filter "*.md" | ForEach-Object {
        try {
            $DestinationFile = Join-Path -Path $DestinationPath -ChildPath $_.Name
            Move-Item -Path $_.FullName -Destination $DestinationFile -Force
            Write-Host "Moved: $($_.FullName) to $DestinationFile"
        }
        catch {
            Write-Error "Failed to move $($_.FullName): $($_.Exception.Message)"
            throw
        }
    }
}

function Invoke-LogMigration {
    $SourceDirectory = "C:/Atari-Monk-Art/productivity/content/format-2"
    $DestinationDirectory = "C:/Atari-Monk-Art/dev-blog/content/projects/productivity/logs"
    
    try {
        Write-Host "Starting log migration process"
        Write-Host "Removing existing log files from: $DestinationDirectory"
        Remove-ExistingLogs -LogsPath $DestinationDirectory
        
        Write-Host "Moving new log files from: $SourceDirectory to: $DestinationDirectory"
        Move-LogFiles -SourcePath $SourceDirectory -DestinationPath $DestinationDirectory
        
        Write-Host "Log migration completed successfully"
    }
    catch {
        Write-Error "Log migration failed: $($_.Exception.Message)"
        exit 1
    }
}

Invoke-LogMigration