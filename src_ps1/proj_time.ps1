# Read JSON data from file
$jsonData = Get-Content -Raw -Path "../data/proj_time_json/03_2024.json" | ConvertFrom-Json

# Initialize variables to store sums
$totalSum = [timespan]::Zero
$projectSums = @{}

# Output file path
$outputFilePath = "../data/proj_time_stats/03_2024.txt"  # Specify your desired output file path here

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
    $output = "ID: $($obj.id)`r`n"
    foreach ($projSum in $objProjectSums.GetEnumerator()) {
        $projDuration = $projSum.Value
        $output += "Project $($projSum.Name) Sum: $($projDuration.Hours) hours $($projDuration.Minutes) minutes`r`n"
        $objSum += $projDuration  # Update $objSum with project duration
    }
    $output += "Total Sum: $($objSum.Hours) hours $($objSum.Minutes) minutes`r`n`r`n"

    # Write output to file
    $output | Out-File -FilePath $outputFilePath -Append -Encoding utf8

    # Update ID sum
    $objSum = $objProjectSums.Values | Measure-Object -Property TotalSeconds -Sum | Select-Object -ExpandProperty Sum
}

# Output sum for all IDs
$output = "Total Sum of All IDs: $($totalSum.Hours) hours $($totalSum.Minutes) minutes`r`n"
$output += "Project Sums for All IDs:`r`n"
foreach ($projSum in $projectSums.GetEnumerator()) {
    $projDuration = $projSum.Value
    $output += "Project $($projSum.Name) Sum: $($projDuration.Hours) hours $($projDuration.Minutes) minutes`r`n"
}

# Write output to file
$output | Out-File -FilePath $outputFilePath -Append -Encoding utf8
