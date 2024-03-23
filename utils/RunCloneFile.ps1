. ".\CloneFile.ps1"
. ".\GetHashtableFromArguments.ps1"

if ($args) {
    $parsedArgs = GetHashtableFromArguments -argsArray $args

    CloneFile -fileFolder $parsedArgs['fileFolder'] -fileName $parsedArgs['fileName'] -cloneFileName $parsedArgs['cloneFileName']
}
else {
    Write-Host "No arguments provided."
}
