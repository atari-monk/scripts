# Edit Command Module
# Opens posts in system editor

# Import core modules
Import-Module "$PSScriptRoot\..\core\paths.psm1" -Force
Import-Module "$PSScriptRoot\..\core\utils.psm1" -Force

function Get-SystemEditor {
    <#
    .SYNOPSIS
        Determines the system editor to use
    .DESCRIPTION
        Checks environment variables and common editors in order of preference
    .EXAMPLE
        $editor = Get-SystemEditor
    #>
    
    # Check environment variable first
    $editor = $env:EDITOR
    if (-not [string]::IsNullOrWhiteSpace($editor)) {
        Write-Log "Using editor from EDITOR environment variable: $editor" -Level DEBUG
        return $editor
    }
    
    # Check common editors
    $commonEditors = @(
        "code",                          # VS Code
        "notepad",                       # Windows Notepad
        "notepad++",                     # Notepad++
        "subl",                          # Sublime Text
        "atom",                          # Atom
        "vim",                           # Vim
        "nano"                           # Nano
    )
    
    foreach ($editorCmd in $commonEditors) {
        if (Get-Command $editorCmd -ErrorAction SilentlyContinue) {
            Write-Log "Found editor: $editorCmd" -Level DEBUG
            return $editorCmd
        }
    }
    
    # Fallback to notepad on Windows
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        Write-Log "Using fallback editor: notepad" -Level DEBUG
        return "notepad"
    }
    
    throw "No suitable editor found. Please set the EDITOR environment variable."
}

function Open-FileInEditor {
    <#
    .SYNOPSIS
        Opens a file in the system editor
    .DESCRIPTION
        Launches the appropriate editor for the file
    .EXAMPLE
        Open-FileInEditor -FilePath "C:\path\to\file.md"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        
        [string]$Editor
    )
    
    if (-not (Test-Path $FilePath)) {
        throw "File not found: $FilePath"
    }
    
    # Get file info for display
    $fileInfo = Get-Item $FilePath
    $fileSize = Format-FileSize -Bytes $fileInfo.Length
    $lastModified = $fileInfo.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    
    Write-Host "`n📝 Opening File in Editor" -ForegroundColor Cyan
    Write-Host "========================" -ForegroundColor Cyan
    Write-Host "   File: $FilePath" -ForegroundColor White
    Write-Host "   Size: $fileSize" -ForegroundColor Gray
    Write-Host "   Modified: $lastModified" -ForegroundColor Gray
    
    # Determine which editor to use
    if ([string]::IsNullOrWhiteSpace($Editor)) {
        $Editor = Get-SystemEditor
    }
    
    Write-Host "   Editor: $Editor" -ForegroundColor Gray
    
    try {
        # Launch editor
        Write-Log "Launching editor: $Editor $FilePath" -Level INFO
        
        if ($Editor -eq "code") {
            # VS Code with wait
            Start-Process -FilePath $Editor -ArgumentList $FilePath -Wait
        }
        elseif ($Editor -eq "notepad") {
            # Notepad with wait
            Start-Process -FilePath $Editor -ArgumentList $FilePath -Wait
        }
        else {
            # Generic editor
            Start-Process -FilePath $Editor -ArgumentList $FilePath -Wait
        }
        
        Write-Host "✅ Edit session completed" -ForegroundColor Green
        
        # Show file stats after edit
        $updatedInfo = Get-Item $FilePath
        $newSize = Format-FileSize -Bytes $updatedInfo.Length
        
        Write-Host "`n📊 File Updated:" -ForegroundColor Cyan
        Write-Host "   New size: $newSize" -ForegroundColor Gray
        Write-Host "   Modification time: $(Get-Timestamp)" -ForegroundColor Gray
        
        return @{
            FilePath = $FilePath
            Editor = $Editor
            OriginalSize = $fileSize
            NewSize = $newSize
        }
    }
    catch {
        Write-Log "Error opening editor: $($_.Exception.Message)" -Level ERROR
        Write-Host "❌ Failed to open editor: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Edit-File {
    <#
    .SYNOPSIS
        Edits a blog post in the system editor
    .DESCRIPTION
        Main function for opening posts in editor with proper validation
    .EXAMPLE
        Edit-File -BlogName "dev-blog" -CategoryPath "programming" -FileName "tips"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$BlogName,
        
        [Parameter(Mandatory = $true)]
        [string]$CategoryPath,
        
        [Parameter(Mandatory = $true)]
        [string]$FileName,
        
        [string]$Editor,
        
        [switch]$NoIndex
    )
    
    Write-Log "Editing file: $FileName in $CategoryPath" -Level INFO
    
    try {
        # Validate file exists
        if (-not (Test-FileExists -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName)) {
            Write-Host "❌ File '$FileName' not found in category '$CategoryPath'" -ForegroundColor Red
            Write-Host "💡 Use 'blog files $BlogName $CategoryPath' to see available files" -ForegroundColor Yellow
            return
        }
        
        # Resolve file path
        $filePath = Resolve-FilePath -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName
        
        # Open file in editor
        $result = Open-FileInEditor -FilePath $filePath -Editor $Editor
        
        # Show next steps
        Write-Host "`n💡 Next Steps:" -ForegroundColor Cyan
        if (-not $NoIndex) {
            Write-Host "   blog index $BlogName" -ForegroundColor White
        }
        Write-Host "   blog files $BlogName $CategoryPath" -ForegroundColor White
        
        return $result
        
    }
    catch {
        Write-Log "Error editing file: $($_.Exception.Message)" -Level ERROR
        Write-Host "❌ Failed to edit file: $($_.Exception.Message)" -ForegroundColor Red
        throw
    }
}

function Show-EditHelp {
    <#
    .SYNOPSIS
        Displays help information for the edit command
    #>
    
    Write-Host "`n📝 Edit Command Help" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor White
    Write-Host "  blog edit <blog-name> <category-path> <file-name> [--editor name] [--no-index]" -ForegroundColor Yellow
    Write-Host "`nParameters:" -ForegroundColor White
    Write-Host "  blog-name     Name of the blog (dev-blog, mind-dump)" -ForegroundColor Gray
    Write-Host "  category-path Path to the category (e.g., programming/python)" -ForegroundColor Gray
    Write-Host "  file-name     Name of the post to edit (without .md extension)" -ForegroundColor Gray
    Write-Host "  --editor      Specify editor to use (default: auto-detected)" -ForegroundColor Gray
    Write-Host "  --no-index    Skip automatic indexing after edit" -ForegroundColor Gray
    Write-Host "`nExamples:" -ForegroundColor White
    Write-Host "  blog edit dev-blog programming python-tips" -ForegroundColor Green
    Write-Host "  blog edit mind-dump ideas my-idea --editor code" -ForegroundColor Green
    Write-Host "  blog edit dev-blog javascript notes --no-index" -ForegroundColor Green
    Write-Host "`n💡 Supported Editors: VS Code, Notepad++, Sublime Text, Vim, Nano, Atom" -ForegroundColor Yellow
}

# Export functions
Export-ModuleMember -Function @(
    'Edit-File',
    'Show-EditHelp',
    'Get-SystemEditor'
)
