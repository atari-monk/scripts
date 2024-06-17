$scriptAssociations = @{}
$jsonData = Get-Content -Raw -Path "data.json" | ConvertFrom-Json
$jsonData | ForEach-Object {
    $scriptAssociations[$_.Command] = $_
}

function ShowHelp {
    Write-Host "Available Commands:"
    $sortedCommands = $scriptAssociations.Values | Sort-Object Order
    $table = @()
    foreach ($cmd in $sortedCommands) {
        $row = New-Object PSObject -Property @{
            'Order'   = $cmd.Order
            'Title'   = $cmd.Title
            'Command' = $cmd.Command
        }
        $table += $row
    }
    $table | Format-Table -AutoSize
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

            Write-Host "Script Path: $scriptPath"
            Write-Host "Received Parameters: $parameters"

            $paramsArray = $parameters -split ' '

            Write-Host "Parameter Array: $($paramsArray -join ', ')"

            $paramsHashtable = @{}

            for ($i = 0; $i -lt $paramsArray.Length; $i += 2) {
                $key = $paramsArray[$i]
                $value = $paramsArray[$i + 1]

                $key = $key.TrimStart('-')

                Write-Host "Parsed Parameter - Key: $key, Value: $value"

                $paramsHashtable[$key] = $value
            }

            Write-Host "Parsed Parameters: $($paramsHashtable | Format-Table | Out-String)"

            $argList = @(
                "-NoExit",
                "-Command",
                "[console]::Title='$title'; . '$scriptPath'"
            )

            foreach ($key in $paramsHashtable.Keys) {
                $argList += "-$key", $paramsHashtable[$key]
            }

            Start-Process powershell -ArgumentList $argList
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
