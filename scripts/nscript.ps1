<#
.SYNOPSIS
Creates a new PowerShell script from clipboard content and registers a persistent alias.

.DESCRIPTION
- Creates a new script file in the default scripts folder.
- Copies clipboard content into the new file.
- Adds a Set-Alias entry to $PROFILE for persistent aliasing.
- Prints help if required parameters are missing.

.PARAMETER FileName (-f)
Name of the new PowerShell script file. Required.

.PARAMETER AliasName (-a)
Alias name to run the script. Required.

.PARAMETER Interactive (-i)
Prompts user to copy content to clipboard and press Enter before writing.

.EXAMPLE
nscript -f magic.ps1 -a magic -i
#>

[CmdletBinding()]
param(
    [Alias("f")]
    [string]$FileName,

    [Alias("a")]
    [string]$AliasName,

    [Alias("i")]
    [switch]$Interactive,

    [string]$TargetPath = "C:\Atari-Monk\scripts\scripts"
)

function Show-Help {
    Write-Host "`nUSAGE:"
    Write-Host "  nscript -f <ScriptName.ps1> -a <AliasName> [-i]"
    Write-Host "`nPARAMETERS:"
    Write-Host "  -f, -FileName   Name of the new script file (required)"
    Write-Host "  -a, -AliasName  Alias name for the script (required)"
    Write-Host "  -i, -Interactive Prompt to copy content before writing"
    Write-Host "`nEXAMPLES:"
    Write-Host "  nscript -f magic.ps1 -a magic"
    Write-Host "  nscript -f magic.ps1 -a magic -i`n"
}

# Check required parameters
if (-not $FileName -or -not $AliasName) {
    Show-Help
    exit
}

# Ensure target folder exists
if (-not (Test-Path $TargetPath)) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

# Full path for the new script
$FullPath = Join-Path $TargetPath $FileName

# Create file if it doesn't exist
if (-not (Test-Path $FullPath)) {
    New-Item -Path $FullPath -ItemType File | Out-Null
}

# Interactive prompt if requested
if ($Interactive) {
    Write-Host "Please copy the content you want in '$FileName' to the clipboard and press Enter..."
    Read-Host
}

# Get clipboard content
$ClipboardContent = Get-Clipboard

# Warn if clipboard is empty
if ([string]::IsNullOrWhiteSpace($ClipboardContent)) {
    Write-Warning "Clipboard is empty! Script file will not be updated."
    exit
}

# Write clipboard content to the file
$ClipboardContent | Set-Content $FullPath

# Add alias to profile if not already present
$AliasCommand = "Set-Alias -Name $AliasName -Value `"$FullPath`""
if (-not (Get-Content $PROFILE | Select-String -Pattern $AliasCommand -SimpleMatch)) {
    Add-Content -Path $PROFILE -Value $AliasCommand
}

Write-Host "`nScript created at:"
Write-Host "  $FullPath"
Write-Host "Alias added to profile:"
Write-Host "  $AliasName"
Write-Host "`nRestart PowerShell to use the alias."
