function Select-Template {
    param(
        [Parameter(Mandatory=$false)]
        [string]$TemplatePath = ".\templates",
        
        [Parameter(Mandatory=$false)]
        [string]$FileFilter = "*.*"
    )
    
    # Check if template directory exists
    if (-not (Test-Path $TemplatePath)) {
        Write-Error "Template directory '$TemplatePath' does not exist"
        return $null
    }
    
    # Get all template files
    $templateFiles = Get-ChildItem -Path $TemplatePath -File -Filter $FileFilter | 
                     Sort-Object Name
    
    if ($templateFiles.Count -eq 0) {
        Write-Host "No template files found in '$TemplatePath'" -ForegroundColor Yellow
        return $null
    }
    
    # Display menu
    Write-Host "`n=== Template Selection ===" -ForegroundColor Cyan
    Write-Host "Select a template file:" -ForegroundColor White
    Write-Host "------------------------" -ForegroundColor Gray
    
    for ($i = 0; $i -lt $templateFiles.Count; $i++) {
        Write-Host "$($i + 1). $($templateFiles[$i].Name)" -ForegroundColor Yellow
    }
    
    Write-Host "0. Cancel" -ForegroundColor Red
    Write-Host "------------------------" -ForegroundColor Gray
    
    # Get user selection
    do {
        try {
            $selection = Read-Host "Enter selection (1-$($templateFiles.Count))"
            
            if ($selection -eq "0") {
                Write-Host "Selection cancelled." -ForegroundColor Red
                return $null
            }
            
            $index = [int]$selection - 1
            
            if ($index -ge 0 -and $index -lt $templateFiles.Count) {
                $selectedFile = $templateFiles[$index]
                
                # Return path with forward slashes
                $pathWithForwardSlashes = $selectedFile.FullName -replace '\\', '/'
                return $pathWithForwardSlashes
            }
            else {
                Write-Host "Invalid selection. Please choose a number between 1 and $($templateFiles.Count)." -ForegroundColor Red
            }
        }
        catch {
            Write-Host "Please enter a valid number." -ForegroundColor Red
        }
    } while ($true)
}