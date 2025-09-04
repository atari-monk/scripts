# Adding a PowerShell Script Alias to Your Profile

This guide will show you how to create an alias for a PowerShell script so you can run it by typing a simple command name.

## Method 1: Create a Function in Your Profile (Recommended)

### Step 1: Find Your PowerShell Profile
Open PowerShell and check if you have a profile:
```powershell
Test-Path $PROFILE
```

If it returns `False`, create one:
```powershell
New-Item -Path $PROFILE -Type File -Force
```

### Step 2: Edit Your Profile
Open your profile in your preferred editor:
```powershell
notepad $PROFILE
```
Or with VS Code:
```powershell
code $PROFILE
```

### Step 3: Add Your Alias Function
Add a function that calls your script. For example, if you want to create an alias `myscript` for `C:\Scripts\my-script.ps1`:

```powershell
function Invoke-MyScript {
    & "C:\Scripts\my-script.ps1" @args
}

Set-Alias -Name myscript -Value Invoke-MyScript
```

### Step 4: Save and Reload
Save the file and reload your profile:
```powershell
. $PROFILE
```

## Method 2: Direct Alias (For Simple Commands)

For simple commands without parameters, you can use:

```powershell
Set-Alias -Name shortname -Value "C:\Scripts\my-script.ps1"
```

Add this to your profile file.

## Method 3: Using a Profile Module

For better organization, create a module:

### Step 1: Create a Modules Directory
```powershell
$modulePath = "$HOME\Documents\PowerShell\Modules\MyScripts"
New-Item -ItemType Directory -Path $modulePath -Force
```

### Step 2: Create a Module File
Create `MyScripts.psm1` in that directory with:
```powershell
function Invoke-MyScript {
    & "C:\Scripts\my-script.ps1" @args
}

Export-ModuleMember -Function Invoke-MyScript
```

### Step 3: Import in Your Profile
Add to your `$PROFILE`:
```powershell
Import-Module MyScripts
Set-Alias -Name myscript -Value Invoke-MyScript
```

## Example: Complete Profile Setup

Here's a complete example profile setup:

```powershell
# PowerShell Profile

# Script Aliases
function Invoke-MyScript {
    & "C:\Scripts\my-script.ps1" @args
}

function Invoke-Backup {
    & "D:\Utilities\backup-tool.ps1" @args
}

# Set Aliases
Set-Alias -Name myscript -Value Invoke-MyScript
Set-Alias -Name backup -Value Invoke-Backup
Set-Alias -Name ll -Value Get-ChildItem  # Built-in command alias

# Reload function
function Reload-Profile {
    . $PROFILE
    Write-Host "Profile reloaded!" -ForegroundColor Green
}

Write-Host "Profile loaded. Available commands: myscript, backup, ll" -ForegroundColor Cyan
```

## Usage

After setting up, you can use your aliases directly:
```powershell
myscript
backup -param value
ll
```

## Troubleshooting

- If commands don't work, check execution policy:
  ```powershell
  Get-ExecutionPolicy
  ```
  If restricted, set to RemoteSigned:
  ```powershell
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- Check for errors when loading profile:
  ```powershell
  . $PROFILE 2>&1
  ```

- Verify alias exists:
  ```powershell
  Get-Alias myscript
  ```

Your script aliases are now ready to use!

## The Problem

PowerShell has a built-in `prompt` function that determines how your command prompt looks.  
When you set an alias named `prompt`, it overrides this built-in function and runs your script instead - which happens every time the prompt is displayed (after every command!).  
Solution: Use a Different Name.
