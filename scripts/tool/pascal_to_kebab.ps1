# PascalToKebab-Final.ps1
param(
    [string]$Path = "."
)

function Convert-PascalToKebab {
    param([string]$name)

    $result = ""
    for ($i = 0; $i -lt $name.Length; $i++) {
        $char = $name[$i].ToString()  # convert char to string

        if ($char -cmatch '[A-Z]') {
            if ($i -gt 0) { $result += "-" }
            $result += $char.ToLower()
        } else {
            $result += $char
        }
    }

    return $result
}

# Process files
Get-ChildItem -Path $Path -File -Recurse -Include *.ts, *.tsx | ForEach-Object {
    $oldName = $_.Name

    # Skip already kebab-case files
    if ($oldName -cmatch '^[a-z0-9\-]+\.(ts|tsx)$') { return }

    $base = [System.IO.Path]::GetFileNameWithoutExtension($oldName)
    $ext = $_.Extension
    $newBase = Convert-PascalToKebab $base
    $newName = "$newBase$ext"

    if ($oldName -ne $newName) {
        Write-Host "Renaming $oldName -> $newName"
        Rename-Item -Path $_.FullName -NewName $newName
    }
}
