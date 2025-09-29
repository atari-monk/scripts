# blog.ps1
#!/usr/bin/env pwsh
# Blog CLI Tool - Main Entry Point
# A high-level, semi-automated CLI tool to manage multiple blogs efficiently

param(
    [Parameter(Position=0)]
    [string]$Command,
    
    [Parameter(Position=1, ValueFromRemainingArguments=$true)]
    [string[]]$Args
)

# Import configuration and core modules
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Import-Module "$ScriptRoot\config.psm1" -Force
Import-Module "$ScriptRoot\core\utils.psm1" -Force

function Show-Help {
    <#
    .SYNOPSIS
        Displays main help information for the blog CLI tool
    #>
    
    Write-Host "`n📚 Blog CLI Tool" -ForegroundColor Cyan
    Write-Host "================" -ForegroundColor Cyan
    Write-Host "A high-level, semi-automated CLI tool to manage multiple blogs efficiently`n" -ForegroundColor White
    
    Write-Host "📖 Usage:" -ForegroundColor Yellow
    Write-Host "  blog <command> <blog-name> [options]`n" -ForegroundColor White
    
    Write-Host "🛠️  Commands:" -ForegroundColor Yellow
    Write-Host "  list    <blog-name> [--filter text] [--show-files]" -ForegroundColor Green
    Write-Host "          List categories recursively with optional filtering`n" -ForegroundColor Gray
    
    Write-Host "  post    <blog-name> <category-path> <file-name> [--force] [--no-index] [--auto-push]" -ForegroundColor Green
    Write-Host "          Create new post from clipboard content`n" -ForegroundColor Gray
    
    Write-Host "  files   <blog-name> <category-path> [--filter text]" -ForegroundColor Green
    Write-Host "          List files in a specific category`n" -ForegroundColor Gray
    
    Write-Host "  edit    <blog-name> <category-path> <file-name> [--editor name] [--no-index]" -ForegroundColor Green
    Write-Host "          Edit a post in system editor`n" -ForegroundColor Gray
    
    Write-Host "  delete  <blog-name> <category-path> <file-name> [--force] [--no-cleanup]" -ForegroundColor Green
    Write-Host "          Delete a post with confirmation`n" -ForegroundColor Gray
    
    Write-Host "  index   <blog-name>" -ForegroundColor Green
    Write-Host "          Invoke indexing script (placeholder)`n" -ForegroundColor Gray
    
    Write-Host "  push    <blog-name>" -ForegroundColor Green
    Write-Host "          Invoke GitHub push script (placeholder)`n" -ForegroundColor Gray
    
    Write-Host "  config  [--show] [--set key value]" -ForegroundColor Green
    Write-Host "          Manage configuration settings`n" -ForegroundColor Gray
    
    Write-Host "  help    [command]" -ForegroundColor Green
    Write-Host "          Show help for specific command`n" -ForegroundColor Gray
    
    Write-Host "📝 Examples:" -ForegroundColor Yellow
    Write-Host "  blog list dev-blog --show-files" -ForegroundColor White
    Write-Host "  blog post dev-blog programming python-tips" -ForegroundColor White
    Write-Host "  blog edit dev-blog programming python-tips" -ForegroundColor White
    Write-Host "  blog files dev-blog programming --filter tips" -ForegroundColor White
    Write-Host "  blog delete dev-blog programming old-post" -ForegroundColor White
    
    Write-Host "`n🏠 Available Blogs:" -ForegroundColor Yellow
    Get-BlogNames | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    
    Write-Host "`n💡 Tip: Use 'blog help <command>' for detailed command help" -ForegroundColor Cyan
}

function Show-CommandHelp {
    <#
    .SYNOPSIS
        Shows detailed help for a specific command
    #>
    
    param([string]$CommandName)
    
    $commandName = $CommandName.ToLower()
    
    switch ($commandName) {
        "list" { 
            Import-Module "$ScriptRoot\commands\list.psm1" -Force
            Show-ListHelp
        }
        "post" { 
            Import-Module "$ScriptRoot\commands\post.psm1" -Force
            Show-PostHelp
        }
        "files" { 
            Import-Module "$ScriptRoot\commands\files.psm1" -Force
            Show-FilesHelp
        }
        "edit" { 
            Import-Module "$ScriptRoot\commands\edit.psm1" -Force
            Show-EditHelp
        }
        "delete" { 
            Import-Module "$ScriptRoot\commands\delete.psm1" -Force
            Show-DeleteHelp
        }
        "index" { Show-IndexHelp }
        "push" { Show-PushHelp }
        "config" { Show-ConfigHelp }
        default {
            Write-Host "❌ Unknown command: $CommandName" -ForegroundColor Red
            Write-Host "💡 Use 'blog help' to see available commands" -ForegroundColor Yellow
        }
    }
}

function Show-IndexHelp {
    Write-Host "`n📋 Index Command Help" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host "`nUsage: blog index <blog-name>`n" -ForegroundColor White
    Write-Host "💡 Note: Indexing integration not yet implemented" -ForegroundColor Yellow
}

function Show-PushHelp {
    Write-Host "`n🚀 Push Command Help" -ForegroundColor Cyan
    Write-Host "===================" -ForegroundColor Cyan
    Write-Host "`nUsage: blog push <blog-name>`n" -ForegroundColor White
    Write-Host "💡 Note: GitHub push integration not yet implemented" -ForegroundColor Yellow
}

function Show-ConfigHelp {
    Write-Host "`n⚙️  Config Command Help" -ForegroundColor Cyan
    Write-Host "=====================" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor White
    Write-Host "  blog config --show" -ForegroundColor Green
    Write-Host "  blog config --set <key> <value>`n" -ForegroundColor Green
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  blog config --show" -ForegroundColor Gray
    Write-Host "  blog config --set editor code" -ForegroundColor Gray
}

function Handle-ListCommand {
    param([string]$BlogName, [string[]]$RemainingArgs)
    
    $filter = ""
    $showFiles = $false
    
    # Parse arguments
    for ($i = 0; $i -lt $RemainingArgs.Count; $i++) {
        if ($RemainingArgs[$i] -eq "--filter" -and $i -lt $RemainingArgs.Count - 1) {
            $filter = $RemainingArgs[$i + 1]
            $i++
        }
        elseif ($RemainingArgs[$i] -eq "--show-files") {
            $showFiles = $true
        }
    }
    
    Import-Module "$ScriptRoot\commands\list.psm1" -Force
    List-Categories -BlogName $BlogName -FilterText $filter -ShowFiles:$showFiles
}

function Handle-PostCommand {
    param([string]$BlogName, [string[]]$RemainingArgs)
    
    if ($RemainingArgs.Count -lt 2) {
        Write-Host "❌ Missing arguments for post command" -ForegroundColor Red
        Write-Host "💡 Usage: blog post <blog-name> <category-path> <file-name>" -ForegroundColor Yellow
        return
    }
    
    $categoryPath = $RemainingArgs[0]
    $fileName = $RemainingArgs[1]
    $force = $RemainingArgs -contains "--force"
    $noIndex = $RemainingArgs -contains "--no-index"
    $autoPush = $RemainingArgs -contains "--auto-push"
    
    Import-Module "$ScriptRoot\commands\post.psm1" -Force
    Post-FromClipboard -BlogName $BlogName -CategoryPath $categoryPath -FileName $fileName -Force:$force -NoIndex:$noIndex -AutoPush:$autoPush
}

function Handle-FilesCommand {
    param([string]$BlogName, [string[]]$RemainingArgs)
    
    if ($RemainingArgs.Count -lt 1) {
        Write-Host "❌ Missing arguments for files command" -ForegroundColor Red
        Write-Host "💡 Usage: blog files <blog-name> <category-path>" -ForegroundColor Yellow
        return
    }
    
    $categoryPath = $RemainingArgs[0]
    $filter = ""
    
    for ($i = 1; $i -lt $RemainingArgs.Count; $i++) {
        if ($RemainingArgs[$i] -eq "--filter" -and $i -lt $RemainingArgs.Count - 1) {
            $filter = $RemainingArgs[$i + 1]
            $i++
        }
    }
    
    Import-Module "$ScriptRoot\commands\files.psm1" -Force
    List-Files -BlogName $BlogName -CategoryPath $categoryPath -FilterText $filter
}

function Handle-EditCommand {
    param([string]$BlogName, [string[]]$RemainingArgs)
    
    if ($RemainingArgs.Count -lt 2) {
        Write-Host "❌ Missing arguments for edit command" -ForegroundColor Red
        Write-Host "💡 Usage: blog edit <blog-name> <category-path> <file-name>" -ForegroundColor Yellow
        return
    }
    
    $categoryPath = $RemainingArgs[0]
    $fileName = $RemainingArgs[1]
    $editor = ""
    $noIndex = $RemainingArgs -contains "--no-index"
    
    # Parse editor if specified
    for ($i = 2; $i -lt $RemainingArgs.Count; $i++) {
        if ($RemainingArgs[$i] -eq "--editor" -and $i -lt $RemainingArgs.Count - 1) {
            $editor = $RemainingArgs[$i + 1]
            $i++
        }
    }
    
    Import-Module "$ScriptRoot\commands\edit.psm1" -Force
    Edit-File -BlogName $BlogName -CategoryPath $categoryPath -FileName $fileName -Editor $editor -NoIndex:$noIndex
}

function Handle-DeleteCommand {
    param([string]$BlogName, [string[]]$RemainingArgs)
    
    if ($RemainingArgs.Count -lt 2) {
        Write-Host "❌ Missing arguments for delete command" -ForegroundColor Red
        Write-Host "💡 Usage: blog delete <blog-name> <category-path> <file-name>" -ForegroundColor Yellow
        return
    }
    
    $categoryPath = $RemainingArgs[0]
    $fileName = $RemainingArgs[1]
    $force = $RemainingArgs -contains "--force"
    $noCleanup = $RemainingArgs -contains "--no-cleanup"
    
    Import-Module "$ScriptRoot\commands\delete.psm1" -Force
    Delete-File -BlogName $BlogName -CategoryPath $categoryPath -FileName $fileName -Force:$force -NoCleanup:$noCleanup
}

function Handle-ConfigCommand {
    param([string[]]$RemainingArgs)
    
    if ($RemainingArgs -contains "--show") {
        Show-Configuration
    }
    elseif ($RemainingArgs -contains "--set" -and $RemainingArgs.Count -ge 3) {
        $keyIndex = [Array]::IndexOf($RemainingArgs, "--set") + 1
        if ($keyIndex -lt $RemainingArgs.Count) {
            $key = $RemainingArgs[$keyIndex]
            $value = $RemainingArgs[$keyIndex + 1]
            Set-Configuration -Key $key -Value $value
        }
    }
    else {
        Show-ConfigHelp
    }
}

# Main command routing
try {
    Write-Log "Blog CLI invoked with command: $Command, args: $($Args -join ', ')" -Level DEBUG
    
    switch ($Command.ToLower()) {
        "list" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for list command" -ForegroundColor Red
                Write-Host "💡 Usage: blog list <blog-name> [options]" -ForegroundColor Yellow
                break
            }
            Handle-ListCommand -BlogName $Args[0] -RemainingArgs $Args[1..($Args.Count-1)]
        }
        "post" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for post command" -ForegroundColor Red
                Write-Host "💡 Usage: blog post <blog-name> <category-path> <file-name>" -ForegroundColor Yellow
                break
            }
            Handle-PostCommand -BlogName $Args[0] -RemainingArgs $Args[1..($Args.Count-1)]
        }
        "files" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for files command" -ForegroundColor Red
                Write-Host "💡 Usage: blog files <blog-name> <category-path>" -ForegroundColor Yellow
                break
            }
            Handle-FilesCommand -BlogName $Args[0] -RemainingArgs $Args[1..($Args.Count-1)]
        }
        "edit" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for edit command" -ForegroundColor Red
                Write-Host "💡 Usage: blog edit <blog-name> <category-path> <file-name>" -ForegroundColor Yellow
                break
            }
            Handle-EditCommand -BlogName $Args[0] -RemainingArgs $Args[1..($Args.Count-1)]
        }
        "delete" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for delete command" -ForegroundColor Red
                Write-Host "💡 Usage: blog delete <blog-name> <category-path> <file-name>" -ForegroundColor Yellow
                break
            }
            Handle-DeleteCommand -BlogName $Args[0] -RemainingArgs $Args[1..($Args.Count-1)]
        }
        "index" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for index command" -ForegroundColor Red
                Write-Host "💡 Usage: blog index <blog-name>" -ForegroundColor Yellow
                break
            }
            Write-Host "📋 Indexing for blog: $($Args[0])" -ForegroundColor Cyan
            Write-Host "💡 Note: Indexing integration not yet implemented" -ForegroundColor Yellow
        }
        "push" {
            if ($Args.Count -eq 0) {
                Write-Host "❌ Missing blog name for push command" -ForegroundColor Red
                Write-Host "💡 Usage: blog push <blog-name>" -ForegroundColor Yellow
                break
            }
            Write-Host "🚀 Pushing blog: $($Args[0])" -ForegroundColor Cyan
            Write-Host "💡 Note: GitHub push integration not yet implemented" -ForegroundColor Yellow
        }
        "config" {
            Handle-ConfigCommand -RemainingArgs $Args
        }
        "help" {
            if ($Args.Count -gt 0) {
                Show-CommandHelp -CommandName $Args[0]
            } else {
                Show-Help
            }
        }
        { @("", "-h", "--help", "/?") -contains $_ } {
            Show-Help
        }
        default {
            Write-Host "❌ Unknown command: $Command" -ForegroundColor Red
            Write-Host "💡 Use 'blog help' to see available commands" -ForegroundColor Yellow
        }
    }
}
catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Log "CLI error: $($_.Exception.Message)" -Level ERROR
    exit 1
}
