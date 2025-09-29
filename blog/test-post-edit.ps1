# Test script for post and edit commands

# Import core modules first
Import-Module .\core\paths.psm1 -Force
Import-Module .\core\clipboard.psm1 -Force
Import-Module .\core\utils.psm1 -Force

# Import command modules
Import-Module .\commands\post.psm1 -Force
Import-Module .\commands\edit.psm1 -Force

Write-Host "=== Testing Post and Edit Commands ===" -ForegroundColor Green

try {
    # Test 1: System editor detection
    Write-Host "`n1. Testing System Editor Detection:" -ForegroundColor Cyan
    $editor = Get-SystemEditor
    Write-Host "   Detected editor: $editor" -ForegroundColor White
    
    # Test 2: Post validation (without actual creation)
    Write-Host "`n2. Testing Post Validation:" -ForegroundColor Cyan
    Write-Host "   Note: This tests validation logic without creating files" -ForegroundColor Gray
    
    # Create test clipboard content first
    $testContent = @"
# Test Post Content

This is a test post content with multiple lines
to simulate real clipboard content for validation testing.

- Item one
- Item two
- Item three
"@
    
    # Set test content to clipboard if possible
    try {
        Set-ClipboardText -Text $testContent
        Write-Host "   Set test content to clipboard" -ForegroundColor Gray
    }
    catch {
        Write-Host "   Could not set clipboard (test will use existing content)" -ForegroundColor Yellow
    }
    
    # Test validation function
    $validation = Test-PostCreation -BlogName "dev-blog" -CategoryPath "test" -FileName "validation-test"
    Write-Host "   Validation result: $($validation.IsValid)" -ForegroundColor White
    if ($validation.Messages) {
        Write-Host "   Messages: $($validation.Messages -join '; ')" -ForegroundColor Gray
    }
    
    # Test 3: Post content formatting
    Write-Host "`n3. Testing Post Content Formatting:" -ForegroundColor Cyan
    $formatted = New-PostContent -RawContent $testContent -Title "Test Post" -CategoryPath "test/category"
    Write-Host "   Formatted content preview:" -ForegroundColor Gray
    $formatted -split "`n" | Select-Object -First 10 | ForEach-Object { Write-Host "   | $_" -ForegroundColor DarkGray }
    Write-Host "   ..." -ForegroundColor DarkGray
    
    # Test 4: File existence checks
    Write-Host "`n4. Testing File Existence Checks:" -ForegroundColor Cyan
    $exists = Test-FileExists -BlogName "dev-blog" -CategoryPath "test" -FileName "sample-post"
    Write-Host "   File exists: $exists" -ForegroundColor White
    
    # Test 5: Help functions
    Write-Host "`n5. Testing Help Functions:" -ForegroundColor Cyan
    Show-PostHelp
    Start-Sleep -Seconds 1
    Show-EditHelp
    
    Write-Host "`n=== Post and Edit command tests completed successfully! ===" -ForegroundColor Green
    Write-Host "`n💡 Note: Actual post creation and editing tests require:" -ForegroundColor Yellow
    Write-Host "   - Clipboard content for post creation" -ForegroundColor Gray
    Write-Host "   - Existing files for editing tests" -ForegroundColor Gray
    Write-Host "   - Manual verification of editor launching" -ForegroundColor Gray
    
}
catch {
    Write-Host "`n=== Test failed: $($_.Exception.Message) ===" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor DarkRed
}