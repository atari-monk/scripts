# Define a list of projects to build with their folders and build commands
$projects = @(
    @{ Name = "zippy-shared-lib"; Path = "C:\Atari-Monk-Art\zippy-shared-lib"; BuildCmd = { pnpm run build --mode development } },
    @{ Name = "fullscreen-canvas-vanilla"; Path = "C:\Atari-Monk-Art\fullscreen-canvas-vanilla"; BuildCmd = { pnpm run build } },
    @{ Name = "zippy"; Path = "C:\Atari-Monk-Art\zippy"; BuildCmd = { pnpm run build } },
    @{ Name = "zippy-test"; Path = "C:\Atari-Monk-Art\zippy-test"; BuildCmd = { pnpm run build --mode development } }
)

# Store build results
$results = @()

foreach ($proj in $projects) {
    Write-Host "Building $($proj.Name)..."
    try {
        # Change to project directory
        Set-Location $proj.Path

        # Clean dist folder
        Remove-Item -Recurse -Force .\dist -ErrorAction SilentlyContinue

        # Run the build command, capturing output and errors
        & $proj.BuildCmd

        # Check last exit code for failure
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Build succeeded: $($proj.Name)" -ForegroundColor Green
            $results += [PSCustomObject]@{ Project = $proj.Name; Status = "Succeeded" }
        }
        else {
            Write-Host "Build FAILED: $($proj.Name)" -ForegroundColor Red
            $results += [PSCustomObject]@{ Project = $proj.Name; Status = "Failed" }
        }
    }
    catch {
        Write-Host "Build ERROR: $($proj.Name)" -ForegroundColor Red
        Write-Host $_.Exception.Message
        $results += [PSCustomObject]@{ Project = $proj.Name; Status = "Error" }
    }
}

# Summary output
Write-Host "`nBuild Summary:"
foreach ($result in $results) {
    $color = if ($result.Status -eq "Succeeded") { "Green" } else { "Red" }
    Write-Host "$($result.Project): $($result.Status)" -ForegroundColor $color
}
