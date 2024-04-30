# Specify the input and output file paths
$inFilePath = "../data/proj_time.txt"
$outFilePath = "../data/proj_time_convert.json"

Write-Host "Input file path: $inFilePath"
Write-Host "Output file path: $outFilePath"

# Read the content of the input file
$content = Get-Content $inFilePath

# Initialize an empty array to store the converted data
$result = @()

# Loop through each line in the input content
for ($i = 0; $i -lt $content.Count; $i++) {
    $line = $content[$i]

    # Check if the line contains an ID
    if ($line.StartsWith("id=")) {
        # Extract the ID
        $currentId = [int]($line -replace 'id=', '')
        $currentEntry = @{
            "id"    = $currentId
            "times" = @()
        }
        # Add the entry to the result
        $result += $currentEntry
    }
    else {
        # Check if it's a project line
        if ($line -match "^\w") {
            $currentProj = $line
            # Move to the next line to read the start time
            $start = $content[++$i]
            # Move to the next line to read the end time
            $end = $content[++$i]
            # Add time entry to the current entry
            $timeEntry = @{
                "proj"  = $currentProj
                "start" = $start
                "end"   = $end
            }
            $currentEntry.times += $timeEntry
        }
    }
}

# Convert the result to JSON format
$jsonResult = $result | ConvertTo-Json -Depth 100

Write-Host "Converted JSON:"
$jsonResult

# Write the JSON result to the output file
$jsonResult | Out-File -FilePath $outFilePath

Write-Host "Conversion completed. Output file written to: $outFilePath"
