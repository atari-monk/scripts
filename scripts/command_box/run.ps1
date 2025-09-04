$ProjectPath = "C:/Atari-Monk-Art/command-box"
$MeilisearchUrl = "https://github.com/meilisearch/meilisearch/releases/latest/download/meilisearch-windows-amd64.exe"
$MeilisearchExe = "meilisearch.exe"

function Start-Project {
    if (-not (Test-Path $ProjectPath)) {
        Write-Error "Project path does not exist: $ProjectPath"
        return
    }

    Push-Location $ProjectPath

    try {
        if (-not (Test-Path $MeilisearchExe)) {
            Write-Host "Downloading Meilisearch..."
            Invoke-WebRequest -Uri $MeilisearchUrl -OutFile $MeilisearchExe
        }

        Write-Host "Starting Meilisearch service..."
        $MeilisearchProcess = Start-Process -FilePath $MeilisearchExe -PassThru

        Write-Host "Starting Next.js development server..."
        pnpm dev

    } finally {
        if ($MeilisearchProcess -and (-not $MeilisearchProcess.HasExited)) {
            Write-Host "Stopping Meilisearch service..."
            Stop-Process -Id $MeilisearchProcess.Id -Force
        }
        
        if (Test-Path $MeilisearchExe) {
            Remove-Item $MeilisearchExe -Force
        }
        
        Pop-Location
    }
}

Start-Project