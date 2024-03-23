function CloneFile {
    param(
        [string]$fileFolder,
        [string]$fileName,
        [string]$cloneFileName = ""
    )

    Write-Host "Received parameters:"
    Write-Host "fileFolder: $fileFolder"
    Write-Host "fileName: $fileName"
    Write-Host "cloneFileName: $cloneFileName"
    
    if (-not $cloneFileName) {
        $cloneFileName = "New_$fileName"
    }

    $filePath = Join-Path $fileFolder $fileName

    if (Test-Path $filePath) {
        $fileExtension = [System.IO.Path]::GetExtension($filePath)
        $newFilePath = Join-Path $fileFolder ($cloneFileName + $fileExtension)

        Copy-Item -Path $filePath -Destination $newFilePath

        Write-Host "File cloned successfully. New file path: $newFilePath"
    }
    else {
        Write-Host "File not found: $filePath"
    }
}
