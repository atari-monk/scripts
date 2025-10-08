# speech

A Python script that records audio from the microphone and transcribes it to text using OpenAI's Whisper model.

## CLI API

```sh
speech
```

## Core Functionality

### Audio Recording (`record_audio()`)
- **Input**: Real-time microphone audio
- **Activation**: Starts recording immediately upon execution
- **Termination**: Press ENTER key to stop recording
- **Output**: Saves as WAV file at `C:/Atari-Monk/scripts/data/recording.wav`

### Audio Specifications
- **Format**: 16-bit PCM (paInt16)
- **Channels**: Mono (1 channel)
- **Sample Rate**: 16kHz (optimized for Whisper)
- **Chunk Size**: 1024 frames (low latency)
- **Device**: Default system input device

### Transcription (`main()`)
- **Model**: Whisper base (balanced speed/accuracy)
- **Language**: English
- **Task**: Speech-to-text transcription
- **Optimizations**:
  - FP32 for CPU accuracy
  - No-speech threshold: 0.6 (improved silence handling)

## User Interface Flow
1. **Start**: "🚀 Starting speech-to-text..."
2. **Recording**: "🎤 Recording... Press ENTER to stop"
3. **Processing**: "🤖 Loading Whisper model..." → "📝 Transcribing..."
4. **Output**: Formatted transcription with separator lines

## Output Format
```
📄 TRANSCRIPTION:
==================================================
[Transcribed text content]
==================================================
```

## File Management
- **Output Location**: `C:/Atari-Monk/scripts/data/recording.wav`
- **Format**: Standard WAV file
- **Overwrite**: Replaces existing file on each execution

## Dependencies
- `pyaudio` - Audio recording
- `wave` - WAV file handling
- `keyboard` - Key press detection
- `whisper` - Speech recognition
- `numpy` - Audio processing

## Error Handling
- **Keyboard Interrupt**: Graceful recording termination
- **Audio Overflow**: Suppressed with `exception_on_overflow=False`
- **Model Loading**: Handles Whisper model initialization

## Performance Notes
- Optimized for CPU usage (FP32 instead of FP16)
- 16kHz sample rate balances quality and Whisper compatibility
- Base model provides best speed/accuracy tradeoff
- Real-time recording with low-latency chunk processing

## Usage Example
```sh
$ python speech.py
🚀 Starting speech-to-text...
🎤 Recording... Press ENTER to stop
⏹️ Stopping recording...
💾 Saved as C:/Atari-Monk/scripts/data/recording.wav
🤖 Loading Whisper model...
📝 Transcribing...

📄 TRANSCRIPTION:
==================================================
This is the transcribed text from the audio recording.
==================================================
