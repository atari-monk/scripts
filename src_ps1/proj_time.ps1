# Read JSON data from file
$jsonData = Get-Content -Raw -Path "../data/proj_time.json" | ConvertFrom-Json

# Initialize variables to store sums
$totalSum = [timespan]::Zero
$projectSums = @{}

# Loop through each ID
foreach ($obj in $jsonData) {
    $objSum = [timespan]::Zero
    $objProjectSums = @{}

    # Loop through each time entry for the ID
    foreach ($timeEntry in $obj.times) {
        # Calculate the duration
        $startTime = [datetime]::ParseExact($timeEntry.start, 'HH:mm', $null)
        $endTime = [datetime]::ParseExact($timeEntry.end, 'HH:mm', $null)
        $duration = $endTime - $startTime

        # Update total sum
        $totalSum += $duration

        # Update project sums
        $objProjectSums[$timeEntry.proj] += $duration
        $projectSums[$timeEntry.proj] += $duration
    }

    # Output sum for the current ID
    Write-Output "ID: $($obj.id)"
    foreach ($projSum in $objProjectSums.GetEnumerator()) {
        $projDuration = $projSum.Value
        Write-Output "Project $($projSum.Name) Sum: $($projDuration.Hours) hours $($projDuration.Minutes) minutes"
        $objSum += $projDuration  # Update $objSum with project duration
    }
    Write-Output "Total Sum: $($objSum.Hours) hours $($objSum.Minutes) minutes"
    Write-Output ""

    # Update ID sum
    $objSum = $objProjectSums.Values | Measure-Object -Property TotalSeconds -Sum | Select-Object -ExpandProperty Sum
}

# Output sum for all IDs
Write-Output "Total Sum of All IDs: $($totalSum.Hours) hours $($totalSum.Minutes) minutes"
Write-Output "Project Sums for All IDs:"
foreach ($projSum in $projectSums.GetEnumerator()) {
    $projDuration = $projSum.Value
    Write-Output "Project $($projSum.Name) Sum: $($projDuration.Hours) hours $($projDuration.Minutes) minutes"
}
