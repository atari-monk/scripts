# Core Utilities Module
# Shared utilities for logging, filtering, validation, and common operations

# Configuration
$Script:LogLevels = @{
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
}

$Script:CurrentLogLevel = "INFO"

function Set-LogLevel {
    param([string]$Level)
    
    if ($Script:LogLevels.ContainsKey($Level.ToUpper())) {
        $Script:CurrentLogLevel = $Level.ToUpper()
        Write-Log "Log level set to: $Script:CurrentLogLevel" -Level DEBUG
    }
    else {
        Write-Log "Invalid log level: $Level. Available levels: $($Script:LogLevels.Keys -join ', ')" -Level ERROR
    }
}

function Write-Log {
    <#
    .SYNOPSIS
        Writes a log message with timestamp and level
    .DESCRIPTION
        Provides consistent logging with different levels and colors
    .EXAMPLE
        Write-Log "Operation completed" -Level INFO
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        
        [string]$Level = "INFO",
        
        [switch]$NoNewline
    )
    
    $levelUpper = $Level.ToUpper()
    
    # Check if we should log this message based on current log level
    if ($Script:LogLevels[$levelUpper] -lt $Script:LogLevels[$Script:CurrentLogLevel]) {
        return
    }
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $levelPadding = " " * (5 - $levelUpper.Length)
    $logMessage = "[$timestamp] $levelUpper$levelPadding $Message"
    
    # Color coding
    $color = switch ($levelUpper) {
        "DEBUG" { "Gray" }
        "INFO" { "White" }
        "WARN" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }
    
    if ($NoNewline) {
        Write-Host $logMessage -ForegroundColor $color -NoNewline
    }
    else {
        Write-Host $logMessage -ForegroundColor $color
    }
}

function Filter-Items {
    <#
    .SYNOPSIS
        Filters a collection of items based on substring matching
    .DESCRIPTION
        Provides case-insensitive filtering for strings or objects with Name property
    .EXAMPLE
        $filtered = $items | Filter-Items -FilterText "python"
    #>
    
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
        $Items,
        
        [string]$FilterText = "",
        
        [string]$PropertyName = "Name"
    )
    
    process {
        if ([string]::IsNullOrWhiteSpace($FilterText)) {
            return $Items
        }
        
        $filteredItems = @()
        
        foreach ($item in $Items) {
            $compareValue = if ($item -is [string]) {
                $item
            }
            elseif ($item.PSObject.Properties[$PropertyName]) {
                $item.$PropertyName
            }
            else {
                $item.ToString()
            }
            
            if ($compareValue -like "*$FilterText*") {
                $filteredItems += $item
            }
        }
        
        return $filteredItems
    }
}

function Confirm-Action {
    <#
    .SYNOPSIS
        Prompts user for confirmation before performing an action
    .DESCRIPTION
        Provides consistent confirmation prompts with default options
    .EXAMPLE
        if (Confirm-Action "Delete file?") { Remove-Item $file }
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message,
        
        [string]$Default = "n"
    )
    
    $choices = if ($Default -eq "y") {
        "[Y/n]"
    }
    else {
        "[y/N]"
    }
    
    do {
        $response = Read-Host "$Message $choices"
        
        if ([string]::IsNullOrWhiteSpace($response)) {
            $response = $Default
        }
        
        $response = $response.Trim().ToLower()
    } while ($response -notin @("y", "yes", "n", "no"))
    
    return $response -in @("y", "yes")
}

function Format-FileSize {
    <#
    .SYNOPSIS
        Formats file size in human-readable format
    .DESCRIPTION
        Converts bytes to KB, MB, GB, etc.
    .EXAMPLE
        $size = Format-FileSize -Bytes 1024
    #>
    
    param([long]$Bytes)
    
    if ($Bytes -ge 1GB) {
        return "{0:N2} GB" -f ($Bytes / 1GB)
    }
    elseif ($Bytes -ge 1MB) {
        return "{0:N2} MB" -f ($Bytes / 1MB)
    }
    elseif ($Bytes -ge 1KB) {
        return "{0:N2} KB" -f ($Bytes / 1KB)
    }
    else {
        return "$Bytes B"
    }
}

function Get-Timestamp {
    <#
    .SYNOPSIS
        Gets current timestamp in various formats
    .DESCRIPTION
        Useful for creating dated filenames or logging
    .EXAMPLE
        $timestamp = Get-Timestamp -Format "yyyyMMdd_HHmmss"
    #>
    
    param([string]$Format = "yyyy-MM-dd HH:mm:ss")
    
    return Get-Date -Format $Format
}

function Test-ValidFileName {
    <#
    .SYNOPSIS
        Validates a filename for invalid characters
    .DESCRIPTION
        Checks if filename contains characters invalid for file systems
    .EXAMPLE
        if (Test-ValidFileName "myfile.md") { ... }
    #>
    
    param([string]$FileName)
    
    if ([string]::IsNullOrWhiteSpace($FileName)) {
        return $false
    }
    
    $invalidChars = [System.IO.Path]::GetInvalidFileNameChars()
    return $FileName.IndexOfAny($invalidChars) -eq -1
}

function Sanitize-FileName {
    <#
    .SYNOPSIS
        Removes invalid characters from a filename
    .DESCRIPTION
        Replaces invalid filesystem characters with underscores
    .EXAMPLE
        $safeName = Sanitize-FileName "file:name.md"
    #>
    
    param([string]$FileName)
    
    if ([string]::IsNullOrWhiteSpace($FileName)) {
        return "untitled"
    }
    
    $invalidChars = [System.IO.Path]::GetInvalidFileNameChars()
    $pattern = "[{0}]" -f [regex]::Escape(($invalidChars -join ''))
    
    $sanitized = $FileName -replace $pattern, "_"
    $sanitized = $sanitized.Trim()
    
    # Ensure we don't end up with empty string
    if ([string]::IsNullOrWhiteSpace($sanitized)) {
        return "untitled"
    }
    
    return $sanitized
}

function Show-Spinner {
    <#
    .SYNOPSIS
        Shows a spinning progress indicator
    .DESCRIPTION
        Useful for long-running operations
    .EXAMPLE
        $spinner = Show-Spinner "Processing..."
        # Do work
        $spinner.Stop()
    #>
    
    param(
        [string]$Message = "Working...",
        [int]$DelayMs = 100
    )
    
    $spinnerChars = @('|', '/', '-', '\')
    $counter = 0
    $running = $true
    
    # Run spinner in background job
    $spinnerJob = Start-Job -ScriptBlock {
        param($Message, $DelayMs, $Chars)
        $counter = 0
        while ($true) {
            $char = $Chars[$counter % $Chars.Length]
            Write-Host "`r$Message $char" -NoNewline -ForegroundColor Cyan
            Start-Sleep -Milliseconds $DelayMs
            $counter++
        }
    } -ArgumentList $Message, $DelayMs, $spinnerChars
    
    return @{
        Stop = {
            Stop-Job $spinnerJob.Id
            Remove-Job $spinnerJob.Id
            Write-Host "`r" + (" " * ($Message.Length + 2)) + "`r" -NoNewline
        }
        Job = $spinnerJob
    }
}

# Export functions
Export-ModuleMember -Function @(
    'Set-LogLevel',
    'Write-Log',
    'Filter-Items',
    'Confirm-Action',
    'Format-FileSize',
    'Get-Timestamp',
    'Test-ValidFileName',
    'Sanitize-FileName',
    'Show-Spinner'
)
