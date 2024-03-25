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
        $newFilePath = Join-Path $fileFolder $cloneFileName

        Copy-Item -Path $filePath -Destination $newFilePath

        Write-Host "File cloned successfully. New file path: $newFilePath"
    }
    else {
        Write-Host "File not found: $filePath"
    }
}

function CloneFileFromUserInput {
    param ()

    $fileFolder = Read-Host "Enter the file folder path"
    $fileName = Read-Host "Enter the file name with extension"
    $cloneFileName = Read-Host "Enter the clone file name (press Enter to use default)"

    CloneFile -fileFolder $fileFolder -fileName $fileName -cloneFileName $cloneFileName
}

function GetHashtableFromArguments {
    param (
        [string[]]$argsArray
    )

    $paramsHashtable = @{}

    for ($i = 0; $i -lt $argsArray.Length; $i += 2) {
        $key = $argsArray[$i]
        $value = $argsArray[$i + 1]

        $key = $key.TrimStart('-')

        $paramsHashtable[$key] = $value
    }

    return $paramsHashtable
}

function CloneFileFromArguments {
    param (
        [string[]]$argsArray
    )

    if ($argsArray) {
        $parsedArgs = GetHashtableFromArguments -argsArray $argsArray

        CloneFile -fileFolder $parsedArgs['fileFolder'] -fileName $parsedArgs['fileName'] -cloneFileName $parsedArgs['cloneFileName']
    }
    else {
        Write-Host "No arguments provided."
    }
}

Export-ModuleMember -Function CloneFile, CloneFileFromUserInput, GetHashtableFromArguments, CloneFileFromArguments
