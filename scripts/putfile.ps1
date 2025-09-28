$config = Get-Content "C:/Atari-Monk/scripts/data/putfile.json" | ConvertFrom-Json
$fullPath = Join-Path $config.basePath $config.path
$filePath = Join-Path $fullPath $config.fileName

New-Item -ItemType Directory -Path $fullPath -Force | Out-Null

Get-Clipboard | Add-Content $filePath

Write-Host "Content written to: $filePath"