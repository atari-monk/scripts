function Convert-PathSeparator {
    [CmdletBinding()]
    param()

    $clipboardContent = Get-Clipboard
    if ([string]::IsNullOrEmpty($clipboardContent)) {
        return
    }

    $convertedPath = $clipboardContent -replace '\\', '/'
    Set-Clipboard -Value $convertedPath
}

Convert-PathSeparator