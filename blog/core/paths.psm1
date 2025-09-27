# Core Path Handling Module
# Handles blog roots, category resolution, nested folders

# Blog root configuration
$BlogRoots = @{
    "dev-blog" = "C:\Atari-Monk\dev-blog\content"
    "mind-dump" = "C:\Atari-Monk\mind-dump\content"
}

function Get-BlogRoot {
    param(
        [string]$BlogName
    )
    
    if (-not $BlogRoots.ContainsKey($BlogName)) {
        throw "Blog '$BlogName' not found. Available blogs: $($BlogRoots.Keys -join ', ')"
    }
    
    return $BlogRoots[$BlogName]
}

function Resolve-CategoryPath {
    param(
        [string]$BlogName,
        [string]$CategoryPath
    )
    
    $blogRoot = Get-BlogRoot -BlogName $BlogName
    $fullPath = Join-Path $blogRoot $CategoryPath
    
    # Normalize the path (remove trailing slashes, etc.)
    $fullPath = [System.IO.Path]::GetFullPath($fullPath)
    
    # Security check: ensure the resolved path is within the blog root
    if (-not $fullPath.StartsWith($blogRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Category path '$CategoryPath' resolves outside blog root"
    }
    
    return $fullPath
}

function Test-CategoryExists {
    param(
        [string]$BlogName,
        [string]$CategoryPath
    )
    
    try {
        $categoryPath = Resolve-CategoryPath -BlogName $BlogName -CategoryPath $CategoryPath
        return (Test-Path $categoryPath -PathType Container)
    }
    catch {
        return $false
    }
}

function Ensure-CategoryExists {
    param(
        [string]$BlogName,
        [string]$CategoryPath
    )
    
    $categoryPath = Resolve-CategoryPath -BlogName $BlogName -CategoryPath $CategoryPath
    
    if (-not (Test-Path $categoryPath)) {
        Write-Host "Creating category path: $categoryPath" -ForegroundColor Yellow
        New-Item -ItemType Directory -Path $categoryPath -Force | Out-Null
    }
    
    return $categoryPath
}

function Get-Subcategories {
    param(
        [string]$BlogName,
        [string]$CategoryPath = "",
        [switch]$Recursive
    )
    
    $searchPath = Resolve-CategoryPath -BlogName $BlogName -CategoryPath $CategoryPath
    
    if (-not (Test-Path $searchPath)) {
        return @()
    }
    
    if ($Recursive) {
        $directories = Get-ChildItem -Path $searchPath -Directory -Recurse
    } else {
        $directories = Get-ChildItem -Path $searchPath -Directory
    }
    
    $relativePaths = $directories | ForEach-Object {
        $relativePath = $_.FullName.Substring((Get-BlogRoot $BlogName).Length).TrimStart('\', '/')
        if ($relativePath -eq "") { $relativePath = "." }
        $relativePath
    }
    
    return $relativePaths
}

function Get-FilesInCategory {
    param(
        [string]$BlogName,
        [string]$CategoryPath,
        [string]$Filter = "*.md"
    )
    
    $categoryPath = Resolve-CategoryPath -BlogName $BlogName -CategoryPath $CategoryPath
    
    if (-not (Test-Path $categoryPath)) {
        return @()
    }
    
    $files = Get-ChildItem -Path $categoryPath -Filter $Filter -File
    
    return $files | ForEach-Object {
        @{
            Name = $_.Name
            FullName = $_.FullName
            BaseName = $_.BaseName
            LastWriteTime = $_.LastWriteTime
        }
    }
}

function Resolve-FilePath {
    param(
        [string]$BlogName,
        [string]$CategoryPath,
        [string]$FileName
    )
    
    # Ensure .md extension
    if (-not $FileName.EndsWith('.md')) {
        $FileName += '.md'
    }
    
    $categoryPath = Resolve-CategoryPath -BlogName $BlogName -CategoryPath $CategoryPath
    $filePath = Join-Path $categoryPath $FileName
    
    return $filePath
}

function Test-FileExists {
    param(
        [string]$BlogName,
        [string]$CategoryPath,
        [string]$FileName
    )
    
    try {
        $filePath = Resolve-FilePath -BlogName $BlogName -CategoryPath $CategoryPath -FileName $FileName
        return (Test-Path $filePath -PathType Leaf)
    }
    catch {
        return $false
    }
}

# Export functions
Export-ModuleMember -Function @(
    'Get-BlogRoot',
    'Resolve-CategoryPath',
    'Test-CategoryExists',
    'Ensure-CategoryExists',
    'Get-Subcategories',
    'Get-FilesInCategory',
    'Resolve-FilePath',
    'Test-FileExists'
)
