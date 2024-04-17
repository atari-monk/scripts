function Build-Lib () {
    Write-Output "Building Library Package"
    npm i
    npm run build
    Set-Location build
    npm pack  
}

function Assert-Lib() {
    param (
        [string]$LibPath
    )

    if (-not (Test-Path $LibPath)) {
        Write-Error "Library file not found: $LibPath"
        return $false
    }

    Write-Output "Library file checked"
    return $true
}

function Install-Pack {
    param (
        [string]$PackPath,
        [string]$ProjDir,
        [string]$PackName
    )
    Write-Output "Copy package $PackPath to project $ProjDir"
    Copy-Item $PackPath $ProjDir
    Set-Location $ProjDir
    Write-Output "Installing..."
    npm i (Get-Item $PackName).Name
    $PackFile = Join-Path $ProjDir $PackName
    Write-Output "Removing: $PackFile"
    Remove-Item -Path $PackFile
}
