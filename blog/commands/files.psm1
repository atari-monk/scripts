# Files Command Module
# Lists files in a specific category with optional filtering

# Import core modules
Import-Module "$PSScriptRoot\..\core\paths.psm1" -Force
Import-Module "$PSScriptRoot\..\core\utils.psm1" -Force

function Format-FileList {
    <#
    .SYNOPSIS
        Formats file list for display with metadata
    .DESCRIPTION
        Creates a detailed file listing with size and modification date
    .EXAMPLE
        $fileList = Format-FileList -Files $files
    #>
    
    param(
        [array]$Files,
        [string]$CategoryPath
    )
    
    if ($Files.Count -eq 0) {
        Write-Log "No files found in category" -Level INFO
        return @()
    }
    
    $formattedLines = @()
    
    # Calculate column widths for nice formatting
    $maxNameLength = ($Files | ForEach-Object { $_.Name.Length } | Measure-Object -Maximum).Maximum
    $maxNameLength = [Math]::Min($maxNameLength, 50)  # Cap at reasonable width
    
    foreach ($file in $Files | Sort-Object Name) {
        $fileItem = Get-Item $file.FullName
        $size = Format-FileSize -Bytes $fileItem.Length
        $date = $fileItem.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        
        # Truncate long filenames
        $displayName = if ($file.Name.Length -gt 50) {
            $file.Name.Substring(0, 47) + "..."
        } else {
            $file.Name
        }
        
        $formattedLines += @{
            Name = $displayName
            Size = $size
            Modified = $date
            FullName = $file.FullName
        }
    }
    
    return $formattedLines
}

function Display-FileTable {
    <#
    .SYNOPSIS
        Displays files in a formatted table
    .DESCRIPTION
        Shows files with metadata in a clean table format
    .EXAMPLE
        Display-FileTable -Files $formattedFiles
    #>
    
    param(
        [array]$Files,
        [string]$CategoryPath,
        [string]$FilterText = ""
    )
    
    if ($Files.Count -eq 0) {
        Write-Host "   No files found" -ForegroundColor Gray
        return
    }
    
    # Create table display
    Write-Host "   Name".PadRight(55) "Size".PadRight(12) "Modified" -ForegroundColor Cyan
    Write-Host "   " + ("─" * 75) -ForegroundColor DarkGray
    
    foreach ($file in $Files) {
        $nameColor = if ($file.Name -like "*.md") { "White" } else { "Yellow" }
        Write-Host "   $($file.Name.PadRight(52)) " -NoNewline -ForegroundColor $nameColor
        Write-Host "$($file.Size.PadRight(10)) " -NoNewline -ForegroundColor Gray
        Write-Host $file.Modified -ForegroundColor Gray
    }
}

function List-Files {
    <#
    .SYNOPSIS
        Lists files in a specific category with optional filtering
    .DESCRIPTION
        Shows markdown files in a category with metadata and search capabilities
    .EXAMPLE
        List-Files -BlogName "dev-blog" -CategoryPath "programming/python" -FilterText "tips"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$BlogName,
        
        [Parameter(Mandatory = $false)]
        [string]$CategoryPath = ".",
        
        [string]$FilterText = ""
    )
    
    # Treat empty string or whitespace as root
    if ([string]::IsNullOrWhiteSpace($CategoryPath)) {
        $CategoryPath = "."   # module convention for root
    }

    Write-Log "Listing files in category: $CategoryPath" -Level INFO
    
    try {
        # Validate category exists
        if (-not (Test-CategoryExists -BlogName $BlogName -CategoryPath $CategoryPath)) {
            Write-Log "Category '$CategoryPath' does not exist in blog '$BlogName'" -Level ERROR
            Write-Host "❌ Category '$CategoryPath' not found in blog '$BlogName'" -ForegroundColor Red
            Write-Host "💡 Use 'blog list $BlogName' to see available categories" -ForegroundColor Yellow
            return
        }
        
        # Get files in category
        $allFiles = Get-FilesInCategory -BlogName $BlogName -CategoryPath $CategoryPath
        
        # Apply filter if specified
        if (-not [string]::IsNullOrWhiteSpace($FilterText)) {
            $filteredFiles = $allFiles | Filter-Items -FilterText $FilterText
            Write-Log "Filtered to $($filteredFiles.Count) files matching '$FilterText'" -Level INFO
        } else {
            $filteredFiles = $allFiles
        }
        
        # Display results
        Write-Host "`n📄 Files in '$CategoryPath' category:" -ForegroundColor Green
        if (-not [string]::IsNullOrWhiteSpace($FilterText)) {
            Write-Host "   Filter: '$FilterText'" -ForegroundColor Cyan
        }
        Write-Host ("─" * 80) -ForegroundColor DarkGray
        
        if ($filteredFiles.Count -eq 0) {
            Write-Host "   No files found" -ForegroundColor Gray
            if (-not [string]::IsNullOrWhiteSpace($FilterText)) {
                Write-Host "   Try a different filter or check the category name" -ForegroundColor Yellow
            }
        } else {
            $formattedFiles = Format-FileList -Files $filteredFiles -CategoryPath $CategoryPath
            Display-FileTable -Files $formattedFiles -CategoryPath $CategoryPath -FilterText $FilterText
        }
        
        # Show summary
        Write-Host ("─" * 80) -ForegroundColor DarkGray
        Write-Host "📊 Found $($filteredFiles.Count) files" -ForegroundColor Green
        
        # Show quick actions
        if ($filteredFiles.Count -gt 0) {
            Write-Host "`n💡 Quick actions:" -ForegroundColor Cyan
            Write-Host "   Use 'blog edit $BlogName $CategoryPath <filename>' to edit a file" -ForegroundColor Gray
            Write-Host "   Use 'blog delete $BlogName $CategoryPath <filename>' to delete a file" -ForegroundColor Gray
        }
        
    }
    catch {
        Write-Log "Error listing files: $($_.Exception.Message)" -Level ERROR
        throw
    }
}

function Show-FilesHelp {
    <#
    .SYNOPSIS
        Displays help information for the files command
    #>
    
    Write-Host "`n📄 Files Command Help" -ForegroundColor Cyan
    Write-Host "====================" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor White
    Write-Host "  blog files <blog-name> <category-path> [--filter text]" -ForegroundColor Yellow
    Write-Host "`nParameters:" -ForegroundColor White
    Write-Host "  blog-name     Name of the blog (dev-blog, mind-dump)" -ForegroundColor Gray
    Write-Host "  category-path Path to the category (e.g., programming/python)" -ForegroundColor Gray
    Write-Host "  --filter      Optional text filter for file names" -ForegroundColor Gray
    Write-Host "`nExamples:" -ForegroundColor White
    Write-Host "  blog files dev-blog programming" -ForegroundColor Green
    Write-Host "  blog files dev-blog programming/python --filter tips" -ForegroundColor Green
    Write-Host "  blog files mind-dump ideas" -ForegroundColor Green
}

# Export functions
Export-ModuleMember -Function @(
    'List-Files',
    'Show-FilesHelp'
)
