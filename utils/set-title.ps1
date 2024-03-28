function Set-ConsoleTitle {
    param (
        [string]$Title
    )

    if (-not $Title) {
        $Title = Read-Host "Enter the desired title for the console window"
    }

    $host.ui.RawUI.WindowTitle = $Title
}

Set-ConsoleTitle

#or just use
#$host.ui.RawUI.WindowTitle = ""