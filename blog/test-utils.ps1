# Test script for clipboard and utilities modules

# Import modules
Import-Module .\core\clipboard.psm1 -Force
Import-Module .\core\utils.psm1 -Force

Write-Host "=== Testing Core Utilities Modules ===" -ForegroundColor Green

try {
    # Test 1: Clipboard functionality
    Write-Host "`n1. Testing Clipboard Functions:" -ForegroundColor Cyan
    
    # Test clipboard text validation
    Write-Host "   Testing clipboard validation..." -ForegroundColor White
    $validation = Validate-ClipboardText
    Write-Host "   Clipboard valid: $($validation.IsValid)" -ForegroundColor Gray
    if (-not $validation.IsValid) {
        Write-Host "   Message: $($validation.Message)" -ForegroundColor Gray
    }
    
    # Test 2: Logging functionality
    Write-Host "`n2. Testing Logging Functions:" -ForegroundColor Cyan
    
    Write-Log "This is a DEBUG message" -Level DEBUG
    Write-Log "This is an INFO message" -Level INFO
    Write-Log "This is a WARN message" -Level WARN
    Write-Log "This is an ERROR message" -Level ERROR
    
    # Test log level setting
    Set-LogLevel -Level "WARN"
    Write-Log "This DEBUG message should not appear" -Level DEBUG
    Write-Log "This WARN message should appear" -Level WARN
    
    # Reset log level
    Set-LogLevel -Level "INFO"
    
    # Test 3: Filtering functionality
    Write-Host "`n3. Testing Filtering Functions:" -ForegroundColor Cyan
    
    $items = @("programming", "python", "javascript", "ideas", "python-tips")
    $filtered = $items | Filter-Items -FilterText "python"
    Write-Host "   Original items: $($items -join ', ')" -ForegroundColor Gray
    Write-Host "   Filtered (python): $($filtered -join ', ')" -ForegroundColor White
    
    # Test 4: Confirmation functionality
    Write-Host "`n4. Testing Confirmation Function (simulated):" -ForegroundColor Cyan
    # We'll simulate this since we can't automate interactive prompts easily
    Write-Host "   Confirmation function available - manual testing required" -ForegroundColor Gray
    
    # Test 5: File size formatting
    Write-Host "`n5. Testing File Size Formatting:" -ForegroundColor Cyan
    
    $sizes = @(123, 1024, 1048576, 1073741824)
    foreach ($size in $sizes) {
        $formatted = Format-FileSize -Bytes $size
        Write-Host "   $size bytes = $formatted" -ForegroundColor Gray
    }
    
    # Test 6: Timestamp functionality
    Write-Host "`n6. Testing Timestamp Functions:" -ForegroundColor Cyan
    
    $timestamp = Get-Timestamp
    $fileTimestamp = Get-Timestamp -Format "yyyyMMdd_HHmmss"
    Write-Host "   Standard timestamp: $timestamp" -ForegroundColor Gray
    Write-Host "   File timestamp: $fileTimestamp" -ForegroundColor Gray
    
    # Test 7: Filename validation and sanitization
    Write-Host "`n7. Testing Filename Functions:" -ForegroundColor Cyan
    
    $testNames = @("valid-file.md", "invalid:file.md", "file/with\path.md", "  spaced  .md")
    foreach ($name in $testNames) {
        $isValid = Test-ValidFileName -FileName $name
        $sanitized = Sanitize-FileName -FileName $name
        Write-Host "   '$name' -> Valid: $isValid, Sanitized: '$sanitized'" -ForegroundColor Gray
    }
    
    # Test 8: Spinner functionality (brief test)
    Write-Host "`n8. Testing Spinner Function (brief):" -ForegroundColor Cyan
    Write-Host "   Starting spinner for 2 seconds..." -ForegroundColor Gray
    $spinner = Show-Spinner -Message "Testing spinner"
    Start-Sleep -Seconds 2
    $spinner.Stop
    Write-Host "   Spinner stopped" -ForegroundColor Gray
    
    Write-Host "`n=== All core utilities tests completed successfully! ===" -ForegroundColor Green
}
catch {
    Write-Host "`n=== Test failed: $($_.Exception.Message) ===" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor DarkRed
}
