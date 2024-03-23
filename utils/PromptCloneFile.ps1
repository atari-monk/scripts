. ".\CloneFile.ps1"

$fileFolder = Read-Host "Enter the file folder path"
$fileName = Read-Host "Enter the file name"
$cloneFileName = Read-Host "Enter the clone file name (press Enter to use default)"

CloneFile -fileFolder $fileFolder -fileName $fileName -cloneFileName $cloneFileName
