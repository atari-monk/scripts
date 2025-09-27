# Test script for the paths module

# Import the paths module
Import-Module .\core\paths.psm1 -Force

Write-Host "=== Testing Paths Module ===" -ForegroundColor Green

try {
    # Test 1: Get blog roots
    Write-Host "`n1. Testing Get-BlogRoot:" -ForegroundColor Cyan
    $devBlogRoot = Get-BlogRoot -BlogName "dev-blog"
    Write-Host "   dev-blog root: $devBlogRoot" -ForegroundColor White
    
    $mindDumpRoot = Get-BlogRoot -BlogName "mind-dump"
    Write-Host "   mind-dump root: $mindDumpRoot" -ForegroundColor White
    
    # Test 2: Resolve category paths
    Write-Host "`n2. Testing Resolve-CategoryPath:" -ForegroundColor Cyan
    $categoryPath = Resolve-CategoryPath -BlogName "dev-blog" -CategoryPath "programming/python"
    Write-Host "   Resolved path: $categoryPath" -ForegroundColor White
    
    # Test 3: Test category existence
    Write-Host "`n3. Testing Test-CategoryExists:" -ForegroundColor Cyan
    $exists = Test-CategoryExists -BlogName "dev-blog" -CategoryPath "programming/python"
    Write-Host "   Category exists: $exists" -ForegroundColor White
    
    # Test 4: Ensure category creation
    Write-Host "`n4. Testing Ensure-CategoryExists:" -ForegroundColor Cyan
    $createdPath = Ensure-CategoryExists -BlogName "dev-blog" -CategoryPath "test/category"
    Write-Host "   Created/verified path: $createdPath" -ForegroundColor White
    
    # Test 5: Get subcategories
    Write-Host "`n5. Testing Get-Subcategories:" -ForegroundColor Cyan
    $subcategories = Get-Subcategories -BlogName "dev-blog" -CategoryPath "" -Recursive
    Write-Host "   Found $($subcategories.Count) subcategories:" -ForegroundColor White
    $subcategories | ForEach-Object { Write-Host "   - $_" -ForegroundColor Gray }
    
    # Test 6: Get files in category
    Write-Host "`n6. Testing Get-FilesInCategory:" -ForegroundColor Cyan
    $files = Get-FilesInCategory -BlogName "dev-blog" -CategoryPath ""
    Write-Host "   Found $($files.Count) files in root category" -ForegroundColor White
    
    # Test 7: Resolve file path
    Write-Host "`n7. Testing Resolve-FilePath:" -ForegroundColor Cyan
    $filePath = Resolve-FilePath -BlogName "dev-blog" -CategoryPath "test" -FileName "sample-post"
    Write-Host "   Resolved file path: $filePath" -ForegroundColor White
    
    # Test 8: Test file existence
    Write-Host "`n8. Testing Test-FileExists:" -ForegroundColor Cyan
    $fileExists = Test-FileExists -BlogName "dev-blog" -CategoryPath "test" -FileName "sample-post"
    Write-Host "   File exists: $fileExists" -ForegroundColor White
    
    # Test 9: Error handling - invalid blog
    Write-Host "`n9. Testing error handling (invalid blog):" -ForegroundColor Cyan
    try {
        Get-BlogRoot -BlogName "invalid-blog"
    }
    catch {
        Write-Host "   Error caught: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host "`n=== All tests completed successfully! ===" -ForegroundColor Green
}
catch {
    Write-Host "`n=== Test failed: $($_.Exception.Message) ===" -ForegroundColor Red
    Write-Host "Stack trace: $($_.ScriptStackTrace)" -ForegroundColor DarkRed
}
