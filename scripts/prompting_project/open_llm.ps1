function Show-Usage {
    Write-Host "Usage: .\open_llm.ps1 [-fox] [-h]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -fox       Open DeepSeek in Firefox instead of Chrome"
    Write-Host "  -h         Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\open_llm.ps1           # Open in Chrome (default)"
    Write-Host "  .\open_llm.ps1 -fox      # Open in Firefox"
}

function Open-DeepSeekChrome {
    $chromePaths = @(
        "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe",
        "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
    )
    
    $chromePath = $chromePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
    
    if (-not $chromePath) {
        throw "Google Chrome not found"
    }
    
    Start-Process -FilePath $chromePath -ArgumentList 'https://chat.deepseek.com'
}

function Open-DeepSeekFirefox {
    $firefoxPaths = @(
        "${env:ProgramFiles}\Mozilla Firefox\firefox.exe",
        "${env:ProgramFiles(x86)}\Mozilla Firefox\firefox.exe"
    )
    
    $firefoxPath = $firefoxPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
    
    if (-not $firefoxPath) {
        throw "Mozilla Firefox not found"
    }
    
    Start-Process -FilePath $firefoxPath -ArgumentList 'https://chat.deepseek.com'
}

if ($args -contains '-h' -or $args -contains '-help' -or $args -contains '--help') {
    Show-Usage
    exit 0
}

if ($args -contains '-fox') {
    Open-DeepSeekFirefox
} else {
    Open-DeepSeekChrome
}