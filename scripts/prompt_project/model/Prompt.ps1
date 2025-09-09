class Prompt {
    [string]$Role
    [string]$Task
    [string]$OutputFormat
    [string]$Reasoning
    [string[]]$StopConditions
    [string[]]$Paths
    [string[]]$Requirements
    [bool]$IncludeClipboard

    Prompt() {}
    
    Prompt(
        [string]$role,
        [string]$task,
        [string]$outputFormat
    ) {
        $this.Role = $role
        $this.Task = $task
        $this.OutputFormat = $outputFormat
    }
    
    Prompt(
        [string]$role,
        [string]$task,
        [string]$outputFormat,
        [string]$reasoning,
        [string[]]$stopConditions,
        [string[]]$paths,
        [string[]]$requirements,
        [bool]$includeClipboard
    ) {
        $this.Role = $role
        $this.Task = $task
        $this.OutputFormat = $outputFormat
        $this.Reasoning = $reasoning
        $this.StopConditions = $stopConditions
        $this.Paths = $paths
        $this.Requirements = $requirements
        $this.IncludeClipboard = $includeClipboard
    }
    
    [string]GetCombinedText() {
        $combinedText = @()
        
        $combinedText += "Role: $($this.Role)"
        $combinedText += "Task: $($this.Task)"
        
        if ($this.Requirements -and $this.Requirements.Count -gt 0) {
            $combinedText += "Requirements:"
            foreach ($req in $this.Requirements) {
                $combinedText += "- $req"
            }
        }
        
        if (-not [string]::IsNullOrEmpty($this.Reasoning)) {
            $combinedText += "Reasoning: $($this.Reasoning)"
        }
        
        if ($this.StopConditions -and $this.StopConditions.Count -gt 0) {
            $combinedText += "Stop Conditions: $($this.StopConditions -join ', ')"
        }
        
        $combinedText += "Output Format: $($this.OutputFormat)"
        
        if ($this.Paths -and $this.Paths.Count -gt 0) {
            $combinedText += "Paths: $($this.Paths -join ', ')"
        }
        
        if ($this.Paths -and $this.Paths.Count -gt 0) {
            $combinedText += "Path Contents:"
            foreach ($path in $this.Paths) {
                if (Test-Path $path) {
                    if (Get-Item $path -ErrorAction SilentlyContinue | Where-Object { $_.PSIsContainer }) {
                        $combinedText += "Directory: $path (contents not read)"
                    } else {
                        try {
                            $content = Get-Content $path -Raw -ErrorAction Stop
                            $extension = [System.IO.Path]::GetExtension($path).TrimStart('.')
                            if ([string]::IsNullOrEmpty($extension)) {
                                $extension = "txt"
                            }
                            $combinedText += "File: $path"
                            $combinedText += "Content:"
                            $combinedText += '```' + $extension
                            $combinedText += $content
                            $combinedText += '```'
                        } catch {
                            $combinedText += "File: $path (error reading: $($_.Exception.Message))"
                        }
                    }
                    $combinedText += ""
                }
            }
        }

        if ($this.IncludeClipboard) {
            $clipboardContent = $this.GetClipboardContentLoop()
            if (-not [string]::IsNullOrEmpty($clipboardContent)) {
                $combinedText += "Clipboard Content:"
                $combinedText += '```txt'
                $combinedText += $clipboardContent
                $combinedText += '```'
            }
        }

        return $combinedText -join "`r`n"
    }
    
    [string]GetClipboardContentLoop() {
        $allClipboardContent = @()
        $clipboardCount = 0
        
        Write-Host "Clipboard content collection mode (press Enter to add current clipboard, 'done' to finish):" -ForegroundColor Yellow
        
        do {
            $userInput = Read-Host "Press Enter to add clipboard content or type 'done'"
            
            if ($userInput -eq 'done') {
                break
            }
            
            try {
                $clipboardText = Get-Clipboard -ErrorAction Stop
                if (-not [string]::IsNullOrEmpty($clipboardText)) {
                    $clipboardCount++
                    Write-Host "Added clipboard content #$clipboardCount ($($clipboardText.Length) chars)" -ForegroundColor Green
                    $allClipboardContent += "=== Clipboard Content #$clipboardCount ==="
                    $allClipboardContent += $clipboardText
                    $allClipboardContent += ""
                } else {
                    Write-Host "Clipboard is empty, skipping..." -ForegroundColor Yellow
                }
            } catch {
                Write-Warning "Unable to access clipboard: $($_.Exception.Message)"
            }
            
        } while ($true)
        
        if ($allClipboardContent.Count -gt 0) {
            Write-Host "Added $clipboardCount clipboard snippets to context" -ForegroundColor Green
            return $allClipboardContent -join "`r`n"
        }
        
        return $null
    }
    
    [void]Execute() {
        $validPaths = @()
        if ($this.Paths -and $this.Paths.Count -gt 0) {
            foreach ($path in $this.Paths) {
                if (Test-Path $path) {
                    $validPaths += $path
                } else {
                    Write-Warning "Path not found: $path"
                }
            }
            $this.Paths = $validPaths
        }
        
        $combinedText = $this.GetCombinedText()
        
        try {
            Set-Clipboard -Value $combinedText
            Write-Host "Prompt executed and copied to clipboard!" -ForegroundColor Green
            Write-Host "Character count: $($combinedText.Length)" -ForegroundColor Cyan
        } catch {
            Write-Error "Failed to copy to clipboard: $($_.Exception.Message)"
            Write-Host "Prompt text:`n$combinedText" -ForegroundColor Yellow
        }
    }
    
    [void]SaveToFile([string]$filePath) {
        $data = @{
            Role = $this.Role
            Task = $this.Task
            Requirements = $this.Requirements
            Paths = $this.Paths
            Reasoning = $this.Reasoning
            StopConditions = $this.StopConditions
            OutputFormat = $this.OutputFormat
            IncludeClipboard = $this.IncludeClipboard
        }
        
        $data | ConvertTo-Json -Depth 3 | Out-File -FilePath $filePath -Encoding UTF8
        Write-Host "Prompt saved to: $filePath" -ForegroundColor Green
    }
    
    [string]GetSummary() {
        $taskPreview = if ($this.Task.Length -gt 50) { 
            $this.Task.Substring(0, 47) + "..." 
        } else { 
            $this.Task 
        }
        
        return @"
Prompt Summary:
- Role: $($this.Role)
- Task: $taskPreview
- Requirements: $(if ($this.Requirements) { $this.Requirements.Count } else { 0 })
- Paths: $(if ($this.Paths) { $this.Paths.Count } else { 0 })
- Include Clipboard: $($this.IncludeClipboard)
"@
    }
}