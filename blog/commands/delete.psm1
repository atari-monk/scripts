# Delete Command Module
# Handles post deletion with confirmation and safety features

# Import core modules
Import-Module "$PSScriptRoot\..\core\paths.psm1" -Force
Import-Module "$PSScriptRoot\..\core\utils.psm1" -Force

function Get-FileInfoForDeletion {
    <#
    .SYNOPSIS
        Gets detailed file information for deletion confirmation
    .DESCRIPTION
        Retrieves file metadata to show user before deletion
    .EXAMPLE
        $fileInfo = Get-FileInfoForDeletion -FilePath $filePath
    #>
    
    param([Parameter(Mandatory = $true)][string]$FilePath)
    
    if (-not (Test-Path $FilePath)) {
        throw "File not found: $FilePath"
    }
    
    $file = Get-Item $FilePath
    $content = Get-Content $FilePath -Raw
    
    return @{
        FilePath = $file.FullName
        FileName = $file.Name
        Size = Format-FileSize -Bytes $file.Length
        Created = $file.CreationTime.ToString("yyyy-MM-dd HH:mm")
        Modified = $file.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
        LineCount = ($content -split "`n").Count
        WordCount = ($content -split "\s+" | Where-Object { $_.Length -gt 0 }).Count
        Preview = ($content -split "`n")[0..4] -join "`n"  # First 5 lines
    }
}

function Remove-EmptyCategory {
    <#
    .SYNOPSIS
        Removes empty category folders after file deletion
    .DESCRIPTION
        Recursively removes empty folders up the category tree
    .EXAMPLE
        Remove-EmptyCategory -BlogName $blogName -CategoryPath $categoryPath
    #>
    
    param([string]$BlogName, [string]$CategoryPath)
    
    try {
        $currentPath = Resolve-CategoryPath -BlogName $BlogName -CategoryPath $CategoryPath
        $blogRoot = Get-BlogRoot -BlogName $BlogName
        
        # Walk up the directory tree until we reach blog root
        while ($currentPath -ne $blogRoot -and $currentPath.StartsWith($blogRoot)) {
            # Check if directory is empty
            $items = Get-ChildItem $currentPath -Force
            if ($items.Count -eq 0) {
                Write-Log "Removing empty category: $currentPath" -Level INFO
                Remove-Item $currentPath -Force
                Write-Host "   🗑️  Removed empty category: $(Split-Path $currentPath -Leaf)" -ForegroundColor Yellow
                
                # Move up to parent directory
                $currentPath = Split-Path $currentPath -Parent
            } else {
                break  # Directory not empty, stop cleaning
            }
        }
    }
    catch {
        Write-Log "Error removing empty categories: $($_.Exception.Message)" -Level WARN
        # Non-fatal error, continue
    }
}

function Show-DeletionSummary {
    <#
    .SYNOPSIS
        Displays detailed information about file to be deleted
    .DESCRIPTION
        Shows file metadata and preview to help user make informed decision
    .EXAMPLE
        Show-DeletionSummary -FileInfo $fileInfo
    #>
    
    param([Parameter(Mandatory = $true)]$FileInfo)
    
    Write-Host "`n🗑️  File Deletion Summary" -ForegroundColor Red
    Write-Host "======================" -ForegroundColor Red
    Write-Host "   File: $($FileInfo.FileName)" -ForegroundColor White
    Write-Host "   Location: $(Split-Path $FileInfo.FilePath -Parent)" -ForegroundColor Gray
    Write-Host "   Size: $($FileInfo.Size)" -ForegroundColor Gray
    Write-Host "   Created: $($FileInfo.Created)" -ForegroundColor Gray
    Write-Host "   Modified: $($FileInfo.Modified)" -ForegroundColor Gray
    Write-Host "   Content: $($FileInfo.LineCount) lines, $($FileInfo.WordCount) words" -ForegroundColor Gray
    
    Write-Host "`n   Preview:" -ForegroundColor Yellow
    $previewLines = $FileInfo.Preview -split "`n"
    foreach ($line in $previewLines) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        Write-Host "   | $line" -ForegroundColor DarkGray
    }
    if ($previewLines.Count -eq 5) {
        Write-Host "   | ..." -ForegroundColor DarkGray
    }
}

function Delete-File {
    <#
    .SYNOPSIS
        Deletes a blog post with confirmation and safety checks
    .DESCRIPTION
        Main function for deleting posts with comprehensive validation
    .EXAMPLE
        Delete-File -BlogName "dev-blog" -CategoryPath "programming" -FileName "old-post"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$BlogName,
        
        [Parameter(Mandatory = $true)]
        [string]$CategoryPath,
        
        [Parameter(Mandatory = $true)]
        [string]$FileName,
        
        [switch]$Force,
        
        [switch]$NoCleanup
    )
    
    Write-Log "Initiating file deletion..." -Level INFO
    Write-Log "Blog: $BlogName, Category: $CategoryPath, File: $FileName" -Level DEBUG
    
    try {
        # Validate file exists
        if (-not (Test-FileExists -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName)) {
            Write-Host "❌ File '$FileName' not found in category '$CategoryPath'" -ForegroundColor Red
            Write-Host "💡 Use 'blog files $BlogName $CategoryPath' to see available files" -ForegroundColor Yellow
            return
        }
        
        # Resolve file path
        $filePath = Resolve-FilePath -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName
        
        # Get file information for confirmation
        $fileInfo = Get-FileInfoForDeletion -FilePath $filePath
        
        # Show deletion summary
        Show-DeletionSummary -FileInfo $fileInfo
        
        # Confirm deletion (unless forced)
        if (-not $Force) {
            Write-Host "`n❓ Are you sure you want to delete this file?" -ForegroundColor Red
            $confirmed = Confirm-Action -Message "This action cannot be undone!" -Default "n"
            
            if (-not $confirmed) {
                Write-Host "✅ Deletion cancelled" -ForegroundColor Green
                return
            }
        }
        
        # Perform deletion
        Write-Log "Deleting file: $filePath" -Level INFO
        Remove-Item $filePath -Force
        
        # Show success message
        Write-Host "`n✅ File deleted successfully!" -ForegroundColor Green
        Write-Host "   📄 $($fileInfo.FileName)" -ForegroundColor Gray
        Write-Host "   💾 $($fileInfo.Size)" -ForegroundColor Gray
        Write-Host "   📝 $($fileInfo.LineCount) lines, $($fileInfo.WordCount) words" -ForegroundColor Gray
        
        # Clean up empty categories (unless disabled)
        if (-not $NoCleanup) {
            Write-Host "`n🧹 Cleaning up empty categories..." -ForegroundColor Cyan
            Remove-EmptyCategory -BlogName $BlogName -CategoryPath $CategoryPath
        }
        
        # Show next steps
        Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
        Write-Host "   blog files $BlogName $CategoryPath" -ForegroundColor White
        Write-Host "   blog list $BlogName" -ForegroundColor White
        
        return @{
            DeletedFile = $fileInfo.FileName
            BlogName = $BlogName
            CategoryPath = $CategoryPath
            FileSize = $fileInfo.Size
            LineCount = $fileInfo.LineCount
            WordCount = $fileInfo.WordCount
        }
        
    }
    catch {
        Write-Log "Error deleting file: $($_.Exception.Message)" -Level ERROR
        Write-Host "`n❌ Failed to delete file: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Show-DeleteHelp {
    <#
    .SYNOPSIS
        Displays help information for the delete command
    #>
    
    Write-Host "`n🗑️  Delete Command Help" -ForegroundColor Cyan
    Write-Host "====================" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor White
    Write-Host "  blog delete <blog-name> <category-path> <file-name> [--force] [--no-cleanup]" -ForegroundColor Yellow
    Write-Host "`nParameters:" -ForegroundColor White
    Write-Host "  blog-name     Name of the blog (dev-blog, mind-dump)" -ForegroundColor Gray
    Write-Host "  category-path Path to the category (e.g., programming/python)" -ForegroundColor Gray
    Write-Host "  file-name     Name of the post to delete (without .md extension)" -ForegroundColor Gray
    Write-Host "  --force       Skip confirmation prompt" -ForegroundColor Gray
    Write-Host "  --no-cleanup  Don't remove empty categories after deletion" -ForegroundColor Gray
    Write-Host "`nExamples:" -ForegroundColor White
    Write-Host "  blog delete dev-blog programming old-post" -ForegroundColor Green
    Write-Host "  blog delete mind-dump ideas temp-idea --force" -ForegroundColor Green
    Write-Host "  blog delete dev-blog test sample --no-cleanup" -ForegroundColor Green
    Write-Host "`n⚠️  Warning: Deleted files cannot be recovered!" -ForegroundColor Red
}

# Export functions
Export-ModuleMember -Function @(
    'Delete-File',
    'Show-DeleteHelp',
    'Get-FileInfoForDeletion',
    'Show-DeletionSummary'
)
