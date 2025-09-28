# Core Clipboard Module
# Handles clipboard operations for reading and writing

function Get-ClipboardText {
    <#
    .SYNOPSIS
        Retrieves text content from the clipboard
    .DESCRIPTION
        Attempts to get text from clipboard using multiple methods for cross-platform compatibility
    .EXAMPLE
        $content = Get-ClipboardText
    #>
    
    try {
        # Method 1: PowerShell 5.1+ Get-Clipboard (Windows)
        if (Get-Command Get-Clipboard -ErrorAction SilentlyContinue) {
            $content = Get-Clipboard -Raw -ErrorAction Stop
            if (-not [string]::IsNullOrWhiteSpace($content)) {
                return $content.Trim()
            }
        }
        
        # Method 2: Using .NET for Windows (alternative)
        try {
            Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
            if ([System.Windows.Forms.Clipboard]::ContainsText()) {
                $content = [System.Windows.Forms.Clipboard]::GetText()
                if (-not [string]::IsNullOrWhiteSpace($content)) {
                    return $content.Trim()
                }
            }
        }
        catch {
            # Continue to next method
        }
        
        # Method 3: Using clip.exe (Windows fallback)
        try {
            $tempFile = [System.IO.Path]::GetTempFileName()
            Start-Process -FilePath "cmd.exe" -ArgumentList "/c clip > `"$tempFile`" 2>&1" -Wait -NoNewWindow
            if (Test-Path $tempFile) {
                $content = Get-Content $tempFile -Raw -ErrorAction SilentlyContinue
                Remove-Item $tempFile -Force -ErrorAction SilentlyContinue
                if (-not [string]::IsNullOrWhiteSpace($content)) {
                    return $content.Trim()
                }
            }
        }
        catch {
            # Continue to next method
        }
        
        # Method 4: For cross-platform (if we extend to Linux/Mac)
        try {
            if (Get-Command "pbpaste" -ErrorAction SilentlyContinue) {
                $content = pbpaste
                if (-not [string]::IsNullOrWhiteSpace($content)) {
                    return $content.Trim()
                }
            }
        }
        catch {
            # pbpaste not available
        }
        
        throw "No text content found in clipboard or clipboard access not available"
    }
    catch {
        throw "Failed to read clipboard: $($_.Exception.Message)"
    }
}

function Set-ClipboardText {
    <#
    .SYNOPSIS
        Sets text content to the clipboard
    .DESCRIPTION
        Attempts to set text to clipboard using multiple methods for cross-platform compatibility
    .EXAMPLE
        Set-ClipboardText -Text "Hello World"
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text
    )
    
    try {
        # Method 1: PowerShell 5.1+ Set-Clipboard (Windows)
        if (Get-Command Set-Clipboard -ErrorAction SilentlyContinue) {
            Set-Clipboard -Value $Text -ErrorAction Stop
            return
        }
        
        # Method 2: Using .NET for Windows (alternative)
        try {
            Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
            [System.Windows.Forms.Clipboard]::SetText($Text)
            return
        }
        catch {
            # Continue to next method
        }
        
        # Method 3: Using clip.exe (Windows fallback)
        try {
            $Text | clip.exe
            return
        }
        catch {
            # Continue to next method
        }
        
        # Method 4: For cross-platform (if we extend to Linux/Mac)
        try {
            if (Get-Command "pbcopy" -ErrorAction SilentlyContinue) {
                $Text | pbcopy
                return
            }
        }
        catch {
            # pbcopy not available
        }
        
        Write-Warning "Clipboard setting not available. Text was: $Text"
    }
    catch {
        Write-Warning "Failed to set clipboard: $($_.Exception.Message)"
    }
}

function Test-ClipboardText {
    <#
    .SYNOPSIS
        Tests if clipboard contains valid text content
    .DESCRIPTION
        Checks if clipboard has text content that meets minimum requirements
    .EXAMPLE
        if (Test-ClipboardText) { Write-Host "Clipboard has valid text" }
    #>
    
    try {
        $text = Get-ClipboardText -ErrorAction Stop
        return (-not [string]::IsNullOrWhiteSpace($text))
    }
    catch {
        return $false
    }
}

function Validate-ClipboardText {
    <#
    .SYNOPSIS
        Validates clipboard text content for posting
    .DESCRIPTION
        Checks if clipboard text meets requirements for creating a blog post
    .EXAMPLE
        $validation = Validate-ClipboardText
        if ($validation.IsValid) { ... }
    #>
    
    try {
        $text = Get-ClipboardText -ErrorAction Stop
        
        if ([string]::IsNullOrWhiteSpace($text)) {
            return @{
                IsValid = $false
                Message = "Clipboard contains empty or whitespace-only text"
            }
        }
        
        # Check minimum length (optional - adjust as needed)
        if ($text.Trim().Length -lt 10) {
            return @{
                IsValid = $false
                Message = "Clipboard text is too short (minimum 10 characters required)"
            }
        }
        
        # Check if text looks like meaningful content (basic heuristic)
        $lineCount = ($text -split "`n").Count
        $wordCount = ($text -split "\s+" | Where-Object { $_.Length -gt 1 }).Count
        
        if ($wordCount -lt 5) {
            return @{
                IsValid = $false
                Message = "Clipboard text doesn't contain enough meaningful content"
            }
        }
        
        return @{
            IsValid = $true
            Message = "Clipboard content is valid"
            Text = $text
            LineCount = $lineCount
            WordCount = $wordCount
        }
    }
    catch {
        return @{
            IsValid = $false
            Message = $_.Exception.Message
        }
    }
}

# Export functions
Export-ModuleMember -Function @(
    'Get-ClipboardText',
    'Set-ClipboardText',
    'Test-ClipboardText',
    'Validate-ClipboardText'
)
