# Configuration Module
# Manages blog CLI configuration settings

# Default configuration
$Script:Configuration = @{
    # Blog roots
    Blogs = @{
        "dev-blog" = "C:\Atari-Monk\dev-blog\content"
        "mind-dump" = "C:\Atari-Monk\mind-dump\content"
    }
    
    # Editor settings
    Editor = ""  # Auto-detect if empty
    
    # Integration settings
    AutoIndex = $true
    AutoPush = $false
    
    # Behavior settings
    LogLevel = "INFO"
    ConfirmDeletions = $true
    CleanupEmptyCategories = $true
}

function Get-BlogNames {
    <#
    .SYNOPSIS
        Returns list of available blog names
    #>
    
    return $Script:Configuration.Blogs.Keys | Sort-Object
}

function Get-BlogRoot {
    <#
    .SYNOPSIS
        Gets the root path for a blog
    #>
    
    param([string]$BlogName)
    
    if (-not $Script:Configuration.Blogs.ContainsKey($BlogName)) {
        throw "Blog '$BlogName' not found. Available blogs: $(($Script:Configuration.Blogs.Keys | Sort-Object) -join ', ')"
    }
    
    return $Script:Configuration.Blogs[$BlogName]
}

function Get-Configuration {
    <#
    .SYNOPSIS
        Gets the current configuration
    #>
    
    return $Script:Configuration
}

function Show-Configuration {
    <#
    .SYNOPSIS
        Displays current configuration
    #>
    
    Write-Host "`n⚙️  Blog CLI Configuration" -ForegroundColor Cyan
    Write-Host "========================" -ForegroundColor Cyan
    
    Write-Host "`n📚 Blogs:" -ForegroundColor Yellow
    foreach ($blog in ($Script:Configuration.Blogs.Keys | Sort-Object)) {
        Write-Host "  $blog : $($Script:Configuration.Blogs[$blog])" -ForegroundColor White
    }
    
    Write-Host "`n📝 Editor Settings:" -ForegroundColor Yellow
    Write-Host "  Editor : $(if ($Script:Configuration.Editor) { $Script:Configuration.Editor } else { 'Auto-detect' })" -ForegroundColor White
    
    Write-Host "`n🔗 Integration Settings:" -ForegroundColor Yellow
    Write-Host "  AutoIndex : $($Script:Configuration.AutoIndex)" -ForegroundColor White
    Write-Host "  AutoPush  : $($Script:Configuration.AutoPush)" -ForegroundColor White
    
    Write-Host "`n⚡ Behavior Settings:" -ForegroundColor Yellow
    Write-Host "  LogLevel             : $($Script:Configuration.LogLevel)" -ForegroundColor White
    Write-Host "  ConfirmDeletions     : $($Script:Configuration.ConfirmDeletions)" -ForegroundColor White
    Write-Host "  CleanupEmptyCategories : $($Script:Configuration.CleanupEmptyCategories)" -ForegroundColor White
    
    Write-Host "`n💡 Use 'blog config --set <key> <value>' to modify settings" -ForegroundColor Gray
}

function Set-Configuration {
    <#
    .SYNOPSIS
        Sets a configuration value
    #>
    
    param(
        [Parameter(Mandatory = $true)]
        [string]$Key,
        
        [Parameter(Mandatory = $true)]
        [string]$Value
    )
    
    $validKeys = @("Editor", "AutoIndex", "AutoPush", "LogLevel", "ConfirmDeletions", "CleanupEmptyCategories")
    
    if ($validKeys -contains $Key) {
        # Convert string values to appropriate types
        $convertedValue = $Value
        if ($Key -in @("AutoIndex", "AutoPush", "ConfirmDeletions", "CleanupEmptyCategories")) {
            $convertedValue = $Value -eq "true" -or $Value -eq "1" -or $Value -eq "yes"
        }
        
        $Script:Configuration[$Key] = $convertedValue
        Write-Host "✅ Configuration updated: $Key = $Value" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Invalid configuration key: $Key" -ForegroundColor Red
        Write-Host "💡 Valid keys: $($validKeys -join ', ')" -ForegroundColor Yellow
    }
}

function Load-Configuration {
    <#
    .SYNOPSIS
        Loads configuration from file (future enhancement)
    #>
    
    # TODO: Implement configuration file loading
    Write-Log "Configuration loading not yet implemented" -Level DEBUG
}

function Save-Configuration {
    <#
    .SYNOPSIS
        Saves configuration to file (future enhancement)
    #>
    
    # TODO: Implement configuration file saving
    Write-Log "Configuration saving not yet implemented" -Level DEBUG
}

# Export functions
Export-ModuleMember -Function @(
    'Get-BlogNames',
    'Get-BlogRoot',
    'Get-Configuration',
    'Show-Configuration',
    'Set-Configuration',
    'Load-Configuration',
    'Save-Configuration'
)
