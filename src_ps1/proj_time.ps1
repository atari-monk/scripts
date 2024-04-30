# Read JSON data from file
$jsonData = Get-Content -Raw -Path "../data/proj_time_json/test.json" | ConvertFrom-Json

# Initialize variables to store sums
$totalHours = 0
$totalMinutes = 0

$projectSums = @{}

# Output file path
$outputFilePath = "../data/proj_time_stats/test.txt"  # Specify your desired output file path here

# Loop through each ID
foreach ($obj in $jsonData) {
    $objHours = 0
    $objMinutes = 0

    $objProjectSums = @{}

    # Loop through each time entry for the ID
    foreach ($timeEntry in $obj.times) {
        # Calculate the duration
        $startTime = [datetime]::ParseExact($timeEntry.start, 'HH:mm', $null)
        $endTime = [datetime]::ParseExact($timeEntry.end, 'HH:mm', $null)
        
        # Adjust end time if it's before start time (crosses midnight)
        if ($endTime -lt $startTime) {
            $endTime = $endTime.AddDays(1)
        }
        
        $duration = $endTime - $startTime

        # Calculate duration in hours and minutes
        $hours = $duration.Hours
        $minutes = $duration.Minutes

        # Update total sum for the current ID
        $objHours += $hours
        $objMinutes += $minutes

        # Update project sums for the current ID
        $proj = $timeEntry.proj
        if (-not $objProjectSums.ContainsKey($proj)) {
            $objProjectSums[$proj] = [pscustomobject]@{
                Hours = $hours
                Minutes = $minutes
            }
        } else {
            $objProjectSums[$proj].Hours += $hours
            $objProjectSums[$proj].Minutes += $minutes
        }

        # Update total sum for all IDs
        $totalHours += $hours
        $totalMinutes += $minutes

        # Update project sums for all IDs
        if (-not $projectSums.ContainsKey($proj)) {
            $projectSums[$proj] = [pscustomobject]@{
                Hours = $hours
                Minutes = $minutes
            }
        } else {
            $projectSums[$proj].Hours += $hours
            $projectSums[$proj].Minutes += $minutes
        }

        # Check if minutes overflow to hours for the total sum
        if ($totalMinutes -ge 60) {
            $totalHours += 1
            $totalMinutes -= 60
        }
    }

    # Output sum for the current ID
    $output = "ID: $($obj.id)`r`n"
    foreach ($projSum in $objProjectSums.GetEnumerator()) {
        $projDuration = $projSum.Value
        $output += "Project $($projSum.Name) Sum: $($projDuration.Hours) hours $($projDuration.Minutes) minutes`r`n"
    }
    $output += "Total Sum: $objHours hours $objMinutes minutes`r`n`r`n"

    # Write output to file
    $output | Out-File -FilePath $outputFilePath -Append -Encoding utf8
}

# Output sum for all IDs
$output = "Total Sum of All IDs: $totalHours hours $totalMinutes minutes`r`n"
$output += "Project Sums for All IDs:`r`n"
foreach ($projSum in $projectSums.GetEnumerator()) {
    $projDuration = $projSum.Value
    $output += "Project $($projSum.Name) Sum: $($projDuration.Hours) hours $($projDuration.Minutes) minutes`r`n"
}

# Write output to file
$output | Out-File -FilePath $outputFilePath -Append -Encoding utf8
