# Load data from JSON file and convert to hashtable
$scriptAssociations = @{}
$jsonData = Get-Content -Raw -Path "scriptAssociations.json" | ConvertFrom-Json
$jsonData | ForEach-Object {
    $scriptAssociations[$_.Command] = $_
}

function ShowHelp {
    Write-Host "Available Commands:"
    foreach ($cmd in $scriptAssociations.Keys) {
        $scriptInfo = $scriptAssociations[$cmd]
        Write-Host "`t$cmd - $($scriptInfo.Title)"
    }
}

function RunCommand {
    param (
        [string]$command,
        [string]$parameters = ""
    )

    if ($scriptAssociations.ContainsKey($command)) {
        $scriptInfo = $scriptAssociations[$command]
        $scriptFolder = $scriptInfo.ScriptFolder
        $scriptPath = Join-Path $scriptFolder $scriptInfo.ScriptFile
        $title = $scriptInfo.Title

        $originalDirectory = Get-Location

        try {
            Set-Location $scriptFolder
            Start-Process powershell -ArgumentList "-NoExit -Command `"[console]::Title='$title'; & '$scriptPath' $parameters`""
        }
        finally {
            Set-Location $originalDirectory
        }
    }
    else {
        Write-Host "Invalid command '$command'. Please enter a valid command."
    }
}

function RunCommands {
    param (
        [string[]]$commands
    )

    foreach ($command in $commands) {
        RunCommand -command $command
    }
}
