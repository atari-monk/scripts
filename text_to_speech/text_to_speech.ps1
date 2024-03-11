Add-Type -AssemblyName System.Speech

function CreateSpeechSynthesizer {
    try {
        $synthesizer = New-Object -TypeName System.Speech.Synthesis.SpeechSynthesizer
        return $synthesizer
    }
    catch {
        Write-Host "Error occurred while creating SpeechSynthesizer: $_"
        return $null
    }
}

function PrintAvailableVoices {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer
    )

    try {
        $voices = $synthesizer.GetInstalledVoices()

        Write-Host "Available Voices:"
        foreach ($voiceInfo in $voices) {
            Write-Host " - $($voiceInfo.VoiceInfo.Name)"
        }
    }
    catch {
        Write-Host "Error occurred while getting available voices: $_"
    }
}

function SelectVoiceByHints {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [System.Speech.Synthesis.VoiceGender]$gender,
        [System.Speech.Synthesis.VoiceAge]$age
    )

    try {
        $synthesizer.SelectVoiceByHints($gender, $age)
    }
    catch {
        Write-Host "Error occurred while selecting voice by hints: $_"
    }
}

function SpeakText {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [string]$text
    )

    try {
        $synthesizer.Speak($text)
    }
    catch {
        Write-Host "Error occurred while speaking the text: $_"
    }
}

function SetRate {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [int]$rate
    )

    try {
        # Set the speech rate (words per minute)
        $synthesizer.Rate = $rate
    }
    catch {
        Write-Host "Error occurred while setting speech rate: $_"
    }
}

function SetVolume {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [int]$volume
    )

    try {
        # Set the volume (0 to 100)
        $synthesizer.Volume = $volume
    }
    catch {
        Write-Host "Error occurred while setting volume: $_"
    }
}

function PauseSpeech {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer
    )

    try {
        $synthesizer.Pause()
    }
    catch {
        Write-Host "Error occurred while pausing speech: $_"
    }
}

function ResumeSpeech {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer
    )

    try {
        $synthesizer.Resume()
    }
    catch {
        Write-Host "Error occurred while resuming speech: $_"
    }
}

function SetPitch {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [int]$pitch
    )

    try {
        # Set the voice pitch (-10 to 10, 0 is normal)
        $synthesizer.Pitch = $pitch
    }
    catch {
        Write-Host "Error occurred while setting voice pitch: $_"
    }
}

function SelectVoiceByName {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [string]$voiceName
    )

    try {
        $synthesizer.SelectVoice($voiceName)
    }
    catch {
        Write-Host "Error occurred while selecting voice by name: $_"
    }
}

function AdjustVolumeDuringSpeech {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [int]$targetVolume,
        [int]$durationInSeconds
    )

    try {
        $initialVolume = $synthesizer.Volume
        $volumeChangeRate = ($targetVolume - $initialVolume) / $durationInSeconds
        $startTime = Get-Date

        while ((Get-Date) -lt ($startTime).AddSeconds($durationInSeconds)) {
            $synthesizer.Volume = $initialVolume + ($volumeChangeRate * (New-TimeSpan -Start $startTime).TotalSeconds)
            Start-Sleep -Milliseconds 100
        }

        $synthesizer.Volume = $targetVolume
    }
    catch {
        Write-Host "Error occurred while adjusting volume during speech: $_"
    }
}

function SaveToWav {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [string]$text,
        [string]$outputPath
    )

    try {
        $synthesizer.SetOutputToWaveFile($outputPath)
        $synthesizer.Speak($text)
        $synthesizer.SetOutputToDefaultAudioDevice()
    }
    catch {
        Write-Host "Error occurred while saving to WAV: $_"
    }
}

function PromptForSaveToWav {
    param (
        [System.Speech.Synthesis.SpeechSynthesizer]$synthesizer,
        [string]$textToRead
    )

    do {
        $saveToWav = Read-Host -Prompt "Do you want to save the speech to a WAV file? (Y/N)"
        if ($saveToWav -eq 'Y' -or $saveToWav -eq 'y') {
            $outputDirectory = "C:\atari-monk\code\micro-engine\script\text_to_speech"
        
            if (-not (Test-Path -Path $outputDirectory -PathType Container)) {
                Write-Host "Error: The specified output directory does not exist."
            }
            else {
                $outputPath = Join-Path $outputDirectory "test.wav"
                SaveToWav -synthesizer $synthesizer -text $textToRead -outputPath $outputPath
                break  # Exit the loop if the WAV file is successfully saved
            }
        }
        elseif ($saveToWav -eq 'N' -or $saveToWav -eq 'n') {
            break  # Exit the loop if the user chooses not to save the WAV file
        }
        else {
            Write-Host "Invalid input. Please enter 'Y' or 'N'."
        }
    } while ($true)  # Keep asking until a valid input is provided
}

$synthesizer = CreateSpeechSynthesizer

if ($null -ne $synthesizer) {
    #PrintAvailableVoices -synthesizer $synthesizer

    SelectVoiceByHints -synthesizer $synthesizer -gender ([System.Speech.Synthesis.VoiceGender]::Female) -age ([System.Speech.Synthesis.VoiceAge]::Adult)

    $rate = 0 # (-10 to 10, 0 is normal)
    SetRate -synthesizer $synthesizer -rate $rate

    $volume = 70 # (0 to 100)
    SetVolume -synthesizer $synthesizer -volume $volume

    $textToRead = Read-Host -Prompt "Enter the text you want Narrator to read"

    SpeakText -synthesizer $synthesizer -text $textToRead

    PromptForSaveToWav -synthesizer $synthesizer -textToRead $textToRead
}
