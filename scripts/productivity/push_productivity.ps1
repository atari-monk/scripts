[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [Alias("s")]
    [switch]$State,
    
    [Parameter(Mandatory=$false)]
    [Alias("c")]
    [switch]$Commit,
    
    [Parameter(Mandatory=$false)]
    [Alias("o")]
    [switch]$Override,
    
    [Parameter(Mandatory=$false)]
    [Alias("m")]
    [string]$Message
)

begin {
    $GitPath = "C:/Atari-Monk-Art/dev-blog"
    
    function Show-Help {
        Write-Host "Usage: $($MyInvocation.MyCommand.Name) [-State] [-Commit] [-Override] [-Message <string>]"
        Write-Host "Flags are mandatory: At least one must be specified"
        Write-Host "-State (-s): Print last commit info"
        Write-Host "-Commit (-c): Execute git add, commit with default message, and push"
        Write-Host "-Override (-o): Execute git add, commit with default message, and push"
        Write-Host "-Message (-m): Specify custom commit message"
    }
}

process {
    if (-not ($State -or $Commit -or $Override)) {
        Show-Help
        exit 1
    }

    $originalLocation = Get-Location
    try {
        Set-Location -Path $GitPath -ErrorAction Stop

        if ($State) {
            git log -1
            return
        }

        $commitMessage = if ($Message) { $Message } else { "Update content" }

        if ($Commit -or $Override) {
            git add .
            git commit -m $commitMessage
            git push origin master
        }
    }
    catch {
        Write-Error "Error occurred: $_"
    }
    finally {
        Set-Location -Path $originalLocation
    }
}