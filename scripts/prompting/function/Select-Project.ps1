# Function to select a project folder containing queue.json
function Select-Project {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ProjectsPath,
        [string]$FileFilter = "queue.json"
    )
    
    if (-not (Test-Path $ProjectsPath)) {
        throw "Projects directory not found: $ProjectsPath"
    }
    
    # Find all project folders that contain a queue.json file
    $projectFolders = Get-ChildItem -Path $ProjectsPath -Directory | Where-Object {
        Test-Path (Join-Path $_.FullName $FileFilter)
    }
    
    if ($projectFolders.Count -eq 0) {
        Write-Warning "No projects found with $FileFilter in $ProjectsPath"
        return $null
    }
    
    # Create menu
    Write-Host "`nSelect a Project:" -ForegroundColor Cyan
    Write-Host "=================" -ForegroundColor Cyan
    
    for ($i = 0; $i -lt $projectFolders.Count; $i++) {
        $queueFile = Join-Path $projectFolders[$i].FullName "queue.json"
        $queueData = Get-Content -Path $queueFile -Raw -Encoding UTF8 | ConvertFrom-Json -ErrorAction SilentlyContinue
        $itemCount = if ($queueData) { $queueData.Count } else { 0 }
        
        Write-Host "$($i + 1). $($projectFolders[$i].Name) ($itemCount items in queue)" -ForegroundColor Yellow
    }
    
    Write-Host "0. Cancel" -ForegroundColor Gray
    
    # Get user selection
    $selection = Read-Host "`nEnter selection (1-$($projectFolders.Count))"
    
    if ($selection -eq "0") {
        Write-Host "Selection cancelled." -ForegroundColor Gray
        return $null
    }
    
    if (-not ($selection -match "^\d+$") -or [int]$selection -lt 1 -or [int]$selection -gt $projectFolders.Count) {
        Write-Host "Invalid selection." -ForegroundColor Red
        return $null
    }
    
    $selectedProject = $projectFolders[[int]$selection - 1]
    Write-Host "Selected project: $($selectedProject.Name)" -ForegroundColor Green
    
    return $selectedProject.FullName
}