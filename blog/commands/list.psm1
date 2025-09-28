# List Command Module
# Handles recursive category listing with filtering and file display

# Import core modules
Import-Module "$PSScriptRoot\..\core\paths.psm1" -Force
Import-Module "$PSScriptRoot\..\core\utils.psm1" -Force

function Format-CategoryTree {
    <#
    .SYNOPSIS
        Formats categories as a tree structure for display
    .DESCRIPTION
        Creates a hierarchical tree view of categories with proper indentation
    .EXAMPLE
        $tree = Format-CategoryTree -Categories $categories
    #>
    
    param(
        [array]$Categories,
        [switch]$ShowFiles,
        [string]$BlogName
    )
    
    if ($Categories.Count -eq 0) {
        Write-Log "No categories found" -Level WARN
        return
    }
    
    # Sort categories for consistent output
    $sortedCategories = $Categories | Sort-Object
    
    # Build tree structure
    $treeLines = @()
    
    foreach ($category in $sortedCategories) {
        if ($category -eq ".") {
            $displayName = "(root)"
        } else {
            $displayName = $category
        }
        
        # Add category line
        $treeLines += "📁 $displayName/"
        
        # If showing files, list files in this category
        if ($ShowFiles) {
            $files = Get-FilesInCategory -BlogName $BlogName -CategoryPath $category
            $sortedFiles = $files | Sort-Object Name
            
            foreach ($file in $sortedFiles) {
                $relativePath = if ($category -eq ".") { 
                    $file.Name 
                } else { 
                    "$category/$($file.Name)" 
                }
                $treeLines += "   📄 $($file.Name) ($(Format-FileSize -Bytes (Get-Item $file.FullName).Length))"
            }
            
            if ($sortedFiles.Count -gt 0) {
                $treeLines += ""  # Add spacing between categories
            }
        }
    }
    
    return $treeLines
}

function List-Categories {
    <#
    .SYNOPSIS
        Lists categories recursively with optional filtering and file display
    .DESCRIPTION
        Provides hierarchical view of blog categories with search and file listing options
    .EXAMPLE
        List-Categories -BlogName "dev-blog" -FilterText "python" -ShowFiles
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$BlogName,
        
        [string]$FilterText = "",
        
        [switch]$ShowFiles
    )
    
    Write-Log "Listing categories for blog: $BlogName" -Level INFO
    
    try {
        # Get all categories recursively
        $allCategories = Get-Subcategories -BlogName $BlogName -CategoryPath "" -Recursive
        
        # Always include root category
        $rootCategory = "."
        $allCategories = @($rootCategory) + $allCategories
        
        # Apply filter if specified
        if (-not [string]::IsNullOrWhiteSpace($FilterText)) {
            $filteredCategories = $allCategories | Filter-Items -FilterText $FilterText
            Write-Log "Filtered to $($filteredCategories.Count) categories matching '$FilterText'" -Level INFO
        } else {
            $filteredCategories = $allCategories
        }
        
        if ($filteredCategories.Count -eq 0) {
            Write-Log "No categories found matching filter: '$FilterText'" -Level WARN
            return
        }
        
        # Display results
        Write-Host "`n📚 Categories in '$BlogName' blog:" -ForegroundColor Green
        if (-not [string]::IsNullOrWhiteSpace($FilterText)) {
            Write-Host "   Filter: '$FilterText'" -ForegroundColor Cyan
        }
        Write-Host ("─" * 60) -ForegroundColor DarkGray
        
        $treeOutput = Format-CategoryTree -Categories $filteredCategories -ShowFiles:$ShowFiles -BlogName $BlogName
        
        if ($treeOutput) {
            $treeOutput | ForEach-Object { Write-Host $_ }
        }
        
        # Show summary
        Write-Host ("─" * 60) -ForegroundColor DarkGray
        Write-Host "📊 Found $($filteredCategories.Count) categories" -ForegroundColor Green
        if ($ShowFiles) {
            $totalFiles = 0
            foreach ($category in $filteredCategories) {
                $files = Get-FilesInCategory -BlogName $BlogName -CategoryPath $category
                $totalFiles += $files.Count
            }
            Write-Host "📄 Found $totalFiles files" -ForegroundColor Green
        }
        
    }
    catch {
        Write-Log "Error listing categories: $($_.Exception.Message)" -Level ERROR
        throw
    }
}

function Show-ListHelp {
    <#
    .SYNOPSIS
        Displays help information for the list command
    #>
    
    Write-Host "`n📚 List Command Help" -ForegroundColor Cyan
    Write-Host "====================" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor White
    Write-Host "  blog list <blog-name> [--filter text] [--show-files]" -ForegroundColor Yellow
    Write-Host "`nParameters:" -ForegroundColor White
    Write-Host "  blog-name    Name of the blog (dev-blog, mind-dump)" -ForegroundColor Gray
    Write-Host "  --filter     Optional text filter for category names" -ForegroundColor Gray
    Write-Host "  --show-files Show files in each category" -ForegroundColor Gray
    Write-Host "`nExamples:" -ForegroundColor White
    Write-Host "  blog list dev-blog" -ForegroundColor Green
    Write-Host "  blog list dev-blog --filter python" -ForegroundColor Green
    Write-Host "  blog list mind-dump --show-files" -ForegroundColor Green
    Write-Host "  blog list dev-blog --filter tips --show-files" -ForegroundColor Green
}

# Export functions
Export-ModuleMember -Function @(
    'List-Categories',
    'Show-ListHelp'
)
