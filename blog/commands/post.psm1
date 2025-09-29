# Post Command Module
# Creates new posts from clipboard content

# Import core modules
#Import-Module "$PSScriptRoot\..\core\paths.psm1" -Force
#Import-Module "$PSScriptRoot\..\core\clipboard.psm1" -Force
#Import-Module "$PSScriptRoot\..\core\utils.psm1" -Force

function New-PostContent {
    <#
    .SYNOPSIS
        Creates formatted post content with metadata
    .DESCRIPTION
        Adds YAML front matter and formatting to post content
    .EXAMPLE
        $formattedContent = New-PostContent -RawContent $content -Title "My Post"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$RawContent,
        
        [string]$Title,
        
        [string]$CategoryPath
    )
    
    # Generate title from filename or first line if not provided
    if ([string]::IsNullOrWhiteSpace($Title)) {
        # Try to extract title from first line of content
        $firstLine = ($RawContent -split "`n")[0].Trim()
        if ($firstLine.Length -gt 0 -and $firstLine.Length -lt 100) {
            $Title = $firstLine
        } else {
            $Title = "New Post"
        }
    }
    
    # Create YAML front matter
    $frontMatter = @"
---
title: "$Title"
date: $(Get-Date -Format "yyyy-MM-ddTHH:mm:sszzz")
category: "$CategoryPath"
slug: "$(Get-Timestamp -Format "yyyyMMdd-HHmmss")"
---
"@

    # Format the content
    $formattedContent = $frontMatter + "`n`n" + $RawContent.Trim()
    
    return $formattedContent
}

function Test-PostCreation {
    <#
    .SYNOPSIS
        Validates conditions for post creation
    .DESCRIPTION
        Checks clipboard content, file conflicts, and other pre-conditions
    .EXAMPLE
        $validation = Test-PostCreation -BlogName $blog -CategoryPath $cat -FileName $file
    #>
    
    param(
        [string]$BlogName,
        [string]$CategoryPath,
        [string]$FileName,
        [switch]$Force
    )
    
    $results = @{
        IsValid = $false
        Messages = @()
        Warnings = @()
    }
    
    try {
        # 1. Validate clipboard content
        Write-Log "Validating clipboard content..." -Level DEBUG
        $clipboardValidation = Validate-ClipboardText
        
        if (-not $clipboardValidation.IsValid) {
            $results.Messages += "Clipboard validation failed: $($clipboardValidation.Message)"
            return $results
        }
        
        $results.ClipboardStats = @{
            LineCount = $clipboardValidation.LineCount
            WordCount = $clipboardValidation.WordCount
        }
        
        # 2. Validate filename
        Write-Log "Validating filename..." -Level DEBUG
        if (-not (Test-ValidFileName -FileName $FileName)) {
            $sanitized = Sanitize-FileName -FileName $FileName
            $results.Messages += "Invalid filename '$FileName'. Suggested: '$sanitized'"
            return $results
        }
        
        # 3. Check for file conflicts
        Write-Log "Checking for file conflicts..." -Level DEBUG
        if (Test-FileExists -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName) {
            if (-not $Force) {
                $results.Messages += "File '$FileName' already exists in category '$CategoryPath'. Use --force to overwrite."
                return $results
            } else {
                $results.Warnings += "⚠️  Overwriting existing file: $FileName"
            }
        }
        
        # 4. All checks passed
        $results.IsValid = $true
        $results.Messages += "✅ All validation checks passed"
        
    }
    catch {
        $results.Messages += "Validation error: $($_.Exception.Message)"
    }
    
    return $results
}

function Post-FromClipboard {
    <#
    .SYNOPSIS
        Creates a new post from clipboard content
    .DESCRIPTION
        Main function for creating posts from clipboard with validation and formatting
    .EXAMPLE
        Post-FromClipboard -BlogName "dev-blog" -CategoryPath "programming" -FileName "new-tips"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$BlogName,
        
        [Parameter(Mandatory = $true)]
        [string]$CategoryPath,
        
        [Parameter(Mandatory = $true)]
        [string]$FileName,
        
        [switch]$Force,
        
        [switch]$NoIndex,
        
        [switch]$AutoPush
    )
    
    Write-Log "Creating new post from clipboard..." -Level INFO
    Write-Log "Blog: $BlogName, Category: $CategoryPath, File: $FileName" -Level DEBUG
    
    try {
        # Show pre-validation summary
        Write-Host "`n📝 Creating New Post" -ForegroundColor Cyan
        Write-Host "===================" -ForegroundColor Cyan
        Write-Host "   Blog: $BlogName" -ForegroundColor White
        Write-Host "   Category: $CategoryPath" -ForegroundColor White
        Write-Host "   File: $FileName.md" -ForegroundColor White
        
        if ($Force) {
            Write-Host "   Mode: Force (will overwrite existing files)" -ForegroundColor Yellow
        }
        
        # Run pre-creation validation
        $validation = Test-PostCreation -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName -Force:$Force
        
        if (-not $validation.IsValid) {
            Write-Host "`n❌ Validation Failed:" -ForegroundColor Red
            foreach ($msg in $validation.Messages) {
                Write-Host "   $msg" -ForegroundColor Red
            }
            return
        }
        
        # Show warnings
        foreach ($warning in $validation.Warnings) {
            Write-Host "   $warning" -ForegroundColor Yellow
        }
        
        # Get clipboard content
        Write-Log "Reading clipboard content..." -Level DEBUG
        $clipboardContent = Get-ClipboardText
        
        # Ensure category exists
        Write-Log "Ensuring category path exists..." -Level DEBUG
        $resolvedCategoryPath = Ensure-CategoryExists -BlogName $BlogName -CategoryPath $CategoryPath
        
        # Create formatted post content
        Write-Log "Formatting post content..." -Level DEBUG
        $postContent = New-PostContent -RawContent $clipboardContent -Title $FileName -CategoryPath $CategoryPath
        
        # Resolve file path
        $filePath = Resolve-FilePath -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName
        
        # Write the file
        Write-Log "Writing post to file: $filePath" -Level DEBUG
        $postContent | Out-File -FilePath $filePath -Encoding UTF8
        
        # Show success summary
        Write-Host "`n✅ Post Created Successfully!" -ForegroundColor Green
        Write-Host "   📍 Location: $filePath" -ForegroundColor Gray
        Write-Host "   📊 Stats: $($validation.ClipboardStats.LineCount) lines, $($validation.ClipboardStats.WordCount) words" -ForegroundColor Gray
        Write-Host "   📝 Preview: $($clipboardContent.Substring(0, [Math]::Min(100, $clipboardContent.Length)))..." -ForegroundColor Gray
        
        # Show next steps
        Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
        Write-Host "   blog edit $BlogName $CategoryPath $FileName" -ForegroundColor White
        Write-Host "   blog files $BlogName $CategoryPath" -ForegroundColor White
        
        if (-not $NoIndex) {
            Write-Host "   blog index $BlogName" -ForegroundColor White
        }
        
        if ($AutoPush) {
            Write-Host "   blog push $BlogName" -ForegroundColor White
        }
        
        # Return created file info
        return @{
            FilePath = $filePath
            BlogName = $BlogName
            CategoryPath = $CategoryPath
            FileName = $FileName
            LineCount = $validation.ClipboardStats.LineCount
            WordCount = $validation.ClipboardStats.WordCount
        }
        
    }
    catch {
        Write-Log "Error creating post: $($_.Exception.Message)" -Level ERROR
        Write-Host "`n❌ Failed to create post: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Show-PostHelp {
    <#
    .SYNOPSIS
        Displays help information for the post command
    #>
    
    Write-Host "`n📝 Post Command Help" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor White
    Write-Host "  blog post <blog-name> <category-path> <file-name> [--force] [--no-index] [--auto-push]" -ForegroundColor Yellow
    Write-Host "`nParameters:" -ForegroundColor White
    Write-Host "  blog-name     Name of the blog (dev-blog, mind-dump)" -ForegroundColor Gray
    Write-Host "  category-path Path to the category (e.g., programming/python)" -ForegroundColor Gray
    Write-Host "  file-name     Name for the new post (without .md extension)" -ForegroundColor Gray
    Write-Host "  --force       Overwrite existing file" -ForegroundColor Gray
    Write-Host "  --no-index    Skip automatic indexing" -ForegroundColor Gray
    Write-Host "  --auto-push   Automatically push to GitHub after creation" -ForegroundColor Gray
    Write-Host "`nExamples:" -ForegroundColor White
    Write-Host "  blog post dev-blog programming python-tips" -ForegroundColor Green
    Write-Host "  blog post mind-dump ideas new-idea --force" -ForegroundColor Green
    Write-Host "  blog post dev-blog javascript tips --auto-push" -ForegroundColor Green
    Write-Host "`n💡 Tip: Copy your content to clipboard first, then run this command" -ForegroundColor Yellow
}

# Export functions
Export-ModuleMember -Function @(
    'Post-FromClipboard',
    'Show-PostHelp',
    'Test-PostCreation',
    'New-PostContent'
)
