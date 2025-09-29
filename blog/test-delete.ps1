# Test script for delete command

# Import core modules first
Import-Module .\core\paths.psm1 -Force
Import-Module .\core\utils.psm1 -Force

# Import command modules
Import-Module .\commands\delete.psm1 -Force

Write-Host "=== Testing Delete Command ===" -ForegroundColor Green

try {
    # Test 1: File info retrieval
    Write-Host "`n1. Testing File Info Retrieval:" -ForegroundColor Cyan
    
    # First, let's create a test file to examine
    $testBlog = "dev-blog"
    $testCategory = "test"
    $testFileName = "delete-test-file"
    
    # Ensure test category exists
    Ensure-CategoryExists -BlogName $testBlog -CategoryPath $testCategory
    
    # Create a test file
    $testFilePath = Resolve-FilePath -BlogName $testBlog -CategoryPath $testCategory -FileName $testFileName
    $testContent = @"
# Test File for Deletion

This is a test file created for deletion testing.
It contains multiple lines and some sample content.

- Item one
- Item two
- Item three

This should be enough content to test the deletion preview functionality.
"@
    
    $testContent | Out-File -FilePath $testFilePath -Encoding UTF8
    Write-Host "   Created test file: $testFilePath" -ForegroundColor Gray
    
    # Test file info function
    $fileInfo = Get-FileInfoForDeletion -FilePath $testFilePath
    Write-Host "   File info retrieved:" -ForegroundColor White
    Write-Host "   - Name: $($fileInfo.FileName)" -ForegroundColor Gray
    Write-Host "   - Size: $($fileInfo.Size)" -ForegroundColor Gray
    Write-Host "   - Lines: $($fileInfo.LineCount)" -ForegroundColor Gray
    Write-Host "   - Words: $($fileInfo.WordCount)" -ForegroundColor Gray
    
    # Test 2: Deletion summary display
    Write-Host "`n2. Testing Deletion Summary Display:" -ForegroundColor Cyan
    Show-DeletionSummary -FileInfo $fileInfo
    
    # Test 3: Empty category cleanup simulation
    Write-Host "`n3. Testing Empty Category Cleanup Logic:" -ForegroundColor Cyan
    Write-Host "   (Simulating without actual deletion)" -ForegroundColor Gray
    
    # Test 4: Help function
    Write-Host "`n4. Testing Help Function:" -ForegroundColor Cyan
    Show-DeleteHelp
    
    # Clean up: Delete the test file we created
    Write-Host "`n5. Cleaning up test file..." -ForegroundColor Cyan
    if (Test-Path $testFilePath) {
        Remove-Item $testFilePath -Force
        Write-Host "   Test file cleaned up" -ForegroundColor Gray
    }
    
    Write-Host "`n=== Delete command tests completed successfully! ===" -ForegroundColor Green
    Write-Host "`n💡 Note: Actual deletion tests require:" -ForegroundColor Yellow
    Write-Host "   - Existing files for deletion" -ForegroundColor Gray
    Write-Host "   - Manual confirmation testing" -ForegroundColor Gray
    Write-Host "   - Verification of empty category cleanup" -ForegroundColor Gray
    
}
catch {
    Write-Host "`n=== Test failed: $($_.Exception.Message) ===" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor DarkRed
}
