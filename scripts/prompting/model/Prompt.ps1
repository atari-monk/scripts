class Prompt {
    # Required fields (must be provided during construction)
    [string]$Role
    [string]$Task
    [string]$OutputFormat
    
    # Optional fields (can be empty/null)
    [string]$Reasoning
    [string[]]$StopConditions
    [string[]]$Paths
    [string[]]$Requirements

    # Default constructor for deserialization
    Prompt() {}
    
    # Main constructor with required fields
    Prompt(
        [string]$role,
        [string]$task,
        [string]$outputFormat
    ) {
        $this.Role = $role
        $this.Task = $task
        $this.OutputFormat = $outputFormat
    }
    
    # Full constructor with all optional fields
    Prompt(
        [string]$role,
        [string]$task,
        [string]$outputFormat,
        [string]$reasoning,
        [string[]]$stopConditions,
        [string[]]$paths,
        [string[]]$requirements
    ) {
        $this.Role = $role
        $this.Task = $task
        $this.OutputFormat = $outputFormat
        $this.Reasoning = $reasoning
        $this.StopConditions = $stopConditions
        $this.Paths = $paths
        $this.Requirements = $requirements
    }
    
    [string]GetCombinedText() {
        $combinedText = @()
        
        # Follow the exact order from the example
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
        
        # Add path content to context (this should come after Paths as in the example)
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
                            # Use single quotes and escape backticks properly
                            $combinedText += '```' + $extension
                            $combinedText += $content
                            $combinedText += '```'
                        } catch {
                            $combinedText += "File: $path (error reading: $($_.Exception.Message))"
                        }
                    }
                    $combinedText += ""  # Add empty line between files
                }
            }
        }

        return $combinedText -join "`r`n"
    }
    
    [void]Execute() {
        # Validate paths
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
        
        # Get enhanced combined text with path contents
        $combinedText = $this.GetCombinedText()
        
        # Copy to clipboard
        try {
            Set-Clipboard -Value $combinedText
            Write-Host "Prompt executed and copied to clipboard!" -ForegroundColor Green
            Write-Host "Character count: $($combinedText.Length)" -ForegroundColor Cyan
        } catch {
            Write-Error "Failed to copy to clipboard: $($_.Exception.Message)"
            Write-Host "Prompt text:`n$combinedText" -ForegroundColor Yellow
        }
    }
    
    # Save to file
    [void]SaveToFile([string]$filePath) {
        $data = @{
            Role = $this.Role
            Task = $this.Task
            Requirements = $this.Requirements
            Paths = $this.Paths
            Reasoning = $this.Reasoning
            StopConditions = $this.StopConditions
            OutputFormat = $this.OutputFormat
        }
        
        $data | ConvertTo-Json -Depth 3 | Out-File -FilePath $filePath -Encoding UTF8
        Write-Host "Prompt saved to: $filePath" -ForegroundColor Green
    }
    
    # Helper method to get prompt summary
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
"@
    }
}