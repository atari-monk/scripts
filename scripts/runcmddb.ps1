$ProjectPath = "C:/Atari-Monk/command-box"
$MeilisearchExe = "meilisearch.exe"

# Kill any running Meilisearch processes
Get-Process meilisearch -ErrorAction SilentlyContinue | ForEach-Object { 
    Write-Host "Stopping existing Meilisearch process (PID $($_.Id))..."
    Stop-Process -Id $_.Id -Force 
}

# Open Meilisearch in a new PowerShell window
Start-Process "powershell.exe" -ArgumentList "-NoExit -Command cd $ProjectPath; .\$MeilisearchExe --db-path ./data.ms" -WindowStyle Normal

# Open Next.js dev server in another PowerShell window
Start-Process "powershell.exe" -ArgumentList "-NoExit -Command cd $ProjectPath; pnpm dev" -WindowStyle Normal

Write-Host "Two consoles opened: Meilisearch and Next.js"
