param (
    [Parameter(Mandatory = $true)]
    [string]$ConfigPath
)

class ProjectConfig {
    [string]$BasePath
    [string[]]$Folders
    [string[]]$Files
}

function Get-ProjectConfig {
    param (
        [string]$ConfigPath
    )

    if (-not (Test-Path $ConfigPath)) {
        throw "Config file not found: $ConfigPath"
    }

    $json = Get-Content $ConfigPath -Raw | ConvertFrom-Json

    $config = [ProjectConfig]::new()
    $config.BasePath = $json.basePath
    $config.Folders = $json.folders
    $config.Files = $json.files

    return $config
}

function Join-ProjectPath {
    param (
        [string]$BasePath,
        [string]$RelativePath
    )

    return Join-Path $BasePath $RelativePath
}

function New-Folder {
    param (
        [string]$Path
    )

    if (-not (Test-Path $Path -PathType Container)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created folder: $Path"
    }
    else {
        Write-Host "Folder already exists: $Path"
    }
}

function New-File {
    param (
        [string]$Path
    )

    if (-not (Test-Path $Path -PathType Leaf)) {
        New-Item -ItemType File -Path $Path | Out-Null
        Write-Host "Created file: $Path"
    }
    else {
        Write-Host "File already exists: $Path"
    }
}

function Initialize-Folders {
    param (
        [ProjectConfig]$Config
    )

    foreach ($folder in $Config.Folders) {
        $fullPath = Join-ProjectPath `
            -BasePath $Config.BasePath `
            -RelativePath $folder

        New-Folder -Path $fullPath
    }
}

function Initialize-Files {
    param (
        [ProjectConfig]$Config
    )

    foreach ($file in $Config.Files) {
        $fullPath = Join-ProjectPath `
            -BasePath $Config.BasePath `
            -RelativePath $file

        New-File -Path $fullPath
    }
}

function Main {
    param (
        [string]$ConfigPath
    )

    $config = Get-ProjectConfig -ConfigPath $ConfigPath

    Initialize-Folders -Config $config
    Initialize-Files   -Config $config

    Write-Host "Init project complete"
}

Main -ConfigPath $ConfigPath