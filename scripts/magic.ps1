param(
    [string]$command,
    [string]$name,
    [string[]]$extraArgs
)

# -----------------------------
# Path to JSON commands
# -----------------------------
$jsonPath = "C:/Atari-Monk/scripts/data/magic.json"

if (-not (Test-Path $jsonPath)) {
    Write-Host "magic.json not found at $jsonPath" -ForegroundColor Red
    return
}

# Load JSON
try {
    $commandsData = Get-Content $jsonPath -Raw | ConvertFrom-Json
} catch {
    Write-Host "Failed to parse magic.json" -ForegroundColor Red
    return
}

# -----------------------------
# Show Help
# -----------------------------
if (-not $command) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  magic <command> <name> [extraArgs]" -ForegroundColor Cyan
    Write-Host "`nAvailable commands:" -ForegroundColor Yellow

    foreach ($cmd in $commandsData.commands) {
        Write-Host ("- {0}: {1}" -f $cmd.name, $cmd.description)
    }
    return
}

# -----------------------------
# Find Command
# -----------------------------
$selected = $commandsData.commands | Where-Object { $_.name -eq $command }

if (-not $selected) {
    Write-Host "Unknown command '$command'" -ForegroundColor Red
    return
}

# -----------------------------
# Prepare Script Text
# -----------------------------
$scriptText = $selected.script -replace "{name}", $name

# Add extra arguments if provided
if ($extraArgs) {
    $scriptText += " " + ($extraArgs -join " ")
}

# -----------------------------
# Run Command
# -----------------------------
$color = $selected.color
if (-not $color) { $color = "Green" }

$emoji = $selected.emoji
if (-not $emoji) { $emoji = "✨" }

Write-Host "$emoji Running '$command' for '$name'..." -ForegroundColor $color
Invoke-Expression $scriptText
Write-Host "✅ '$name $command' done!" -ForegroundColor $color
