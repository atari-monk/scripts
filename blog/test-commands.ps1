# Test script for list and files commands

# Import core modules first
Import-Module .\core\paths.psm1 -Force
Import-Module .\core\utils.psm1 -Force

# Import command modules
Import-Module .\commands\list.psm1 -Force
Import-Module .\commands\files.psm1 -Force

Write-Host "=== Testing Command Modules ===" -ForegroundColor Green

try {
    # Test 1: List categories without filter
    Write-Host "`n1. Testing List Categories (basic):" -ForegroundColor Cyan
    Write-Host "   Listing all categories in dev-blog..." -ForegroundColor Gray
    List-Categories -BlogName "dev-blog"
    
    # Test 2: List categories with show-files
    Write-Host "`n2. Testing List Categories with files:" -ForegroundColor Cyan
    Write-Host "   Listing categories with files in dev-blog..." -ForegroundColor Gray
    List-Categories -BlogName "dev-blog" -ShowFiles
    
    # Test 3: List categories with filter
    Write-Host "`n3. Testing List Categories with filter:" -ForegroundColor Cyan
    Write-Host "   Searching for 'test' categories..." -ForegroundColor Gray
    List-Categories -BlogName "dev-blog" -FilterText "test" -ShowFiles
    
    # Test 4: List files in root category
    Write-Host "`n4. Testing List Files (root category):" -ForegroundColor Cyan
    Write-Host "   Listing files in root category..." -ForegroundColor Gray
    List-Files -BlogName "dev-blog" -CategoryPath ""
    
    # Test 5: List files in specific category
    Write-Host "`n5. Testing List Files (specific category):" -ForegroundColor Cyan
    Write-Host "   Listing files in test category..." -ForegroundColor Gray
    List-Files -BlogName "dev-blog" -CategoryPath "test"
    
    # Test 6: List files with filter
    Write-Host "`n6. Testing List Files with filter:" -ForegroundColor Cyan
    Write-Host "   Searching for files in test category..." -ForegroundColor Gray
    List-Files -BlogName "dev-blog" -CategoryPath "test" -FilterText "sample"
    
    # Test 7: Error handling - invalid category
    Write-Host "`n7. Testing error handling (invalid category):" -ForegroundColor Cyan
    Write-Host "   Attempting to list files in non-existent category..." -ForegroundColor Gray
    List-Files -BlogName "dev-blog" -CategoryPath "non-existent-category"
    
    # Test 8: Help functions
    Write-Host "`n8. Testing Help Functions:" -ForegroundColor Cyan
    Show-ListHelp
    Start-Sleep -Seconds 1
    Show-FilesHelp
    
    Write-Host "`n=== All command tests completed successfully! ===" -ForegroundColor Green
}
catch {
    Write-Host "`n=== Test failed: $($_.Exception.Message) ===" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor DarkRed
}

Write-Host "`n💡 Note: Some tests may show empty results if no matching content exists." -ForegroundColor Yellow
Write-Host "   This is expected behavior for clean test environments." -ForegroundColor Yellow