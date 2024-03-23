param (
    [string]$Mode = "UserInput"
)

Import-Module "C:\atari-monk\code\scripts\utils\CloneFile.psm1"

if ($Mode -eq "Arguments") {
    Write-Host 'CloneFileFromArguments'
    CloneFileFromArguments($args)
}
elseif ($Mode -eq "UserInput") {
    Write-Host 'CloneFileFromUserInput'
    CloneFileFromUserInput
}
else {
    Write-Host "Invalid mode specified. Please specify either 'Arguments' or 'UserInput'."
}