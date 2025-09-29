# Test script for CLI entry point

# Import the main CLI script as a module
Import-Module .\config.psm1 -Force
Import-Module .\core\utils.psm1 -Force

Write-Host "=== Testing CLI Entry Point and Configuration ===" -ForegroundColor Green

try {
    # Test 1: Configuration functions
    Write-Host "`n1. Testing Configuration Functions:" -ForegroundColor Cyan
    
    $config = Get-Configuration
    Write-Host "   Configuration loaded successfully" -ForegroundColor White
    
    $blogNames = Get-BlogNames
    Write-Host "   Available blogs: $($blogNames -join ', ')" -ForegroundColor White
    
    # Test 2: Show configuration
    Write-Host "`n2. Testing Configuration Display:" -ForegroundColor Cyan
    Show-Configuration
    
    # Test 3: Configuration setting
    Write-Host "`n3. Testing Configuration Setting:" -ForegroundColor Cyan
    Set-Configuration -Key "LogLevel" -Value "DEBUG"
    Write-Host "   Set LogLevel to DEBUG" -ForegroundColor White
    
    # Test 4: Blog root resolution
    Write-Host "`n4. Testing Blog Root Resolution:" -ForegroundColor Cyan
    try {
        $devBlogRoot = Get-BlogRoot -BlogName "dev-blog"
        Write-Host "   dev-blog root: $devBlogRoot" -ForegroundColor White
    }
    catch {
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test 5: Error handling for invalid blog
    Write-Host "`n5. Testing Error Handling (Invalid Blog):" -ForegroundColor Cyan
    try {
        $invalidRoot = Get-BlogRoot -BlogName "invalid-blog"
    }
    catch {
        Write-Host "   Correctly caught error: $($_.Exception.Message)" -ForegroundColor Green
    }
    
    Write-Host "`n=== CLI and configuration tests completed successfully! ===" -ForegroundColor Green
    Write-Host "`n💡 Note: Full CLI testing requires manual command execution" -ForegroundColor Yellow
    
}
catch {
    Write-Host "`n=== Test failed: $($_.Exception.Message) ===" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor DarkRed
}
