# ftt (File Transcription Tool) - Technical Specification

## Overview
**ftt** is a command-line audio transcription tool that converts audio files to text using OpenAI's Whisper speech recognition model. The tool supports multiple audio formats and provides both automatic language detection and manual language specification.

## CLI API Definition

```sh
ftt <file_path> [--model MODEL] [--language LANGUAGE]
```

### Arguments
- **file_path** (required): Path to the audio file for transcription
- **--model, -m** (optional): Whisper model size (tiny, base, small, medium, large) - defaults to "base"
- **--language, -l** (optional): Force specific language: "en" (English) or "pl" (Polish)

## Usage Examples

```sh
python ftt.py audio.mp3                    # Auto-detect language
python ftt.py audio.mp3 --language en      # Force English transcription
python ftt.py audio.mp3 --language pl      # Force Polish transcription  
python ftt.py audio.wav --model small --language en  # Use smaller model for English
```

## Input Requirements

### Supported Audio Formats
- **Audio files**: `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`
- **Video files with audio**: `.mp4`, `.webm`

### File Validation
- File must exist at specified path
- File extension must be in supported formats list
- Automatic format validation with descriptive error messages

## Output Format

### Console Output
```
📝 Transcribing audio.mp3...
🌐 Language: en

==================================================
📄 TRANSCRIPTION:
==================================================
This is the transcribed text from the audio file.
It will appear here as a continuous block of text.
==================================================
```

### Additional Information
- Displays detected language when auto-detection is used
- Shows progress indicators and error messages with emoji icons
- Formatted output with clear section boundaries

## Core Features

### 1. Audio Transcription
- Uses OpenAI Whisper models for speech-to-text conversion
- Supports multiple model sizes for quality/speed trade-offs
- Configurable transcription parameters:
  - Language specification or auto-detection
  - No-speech threshold: 0.6
  - FP16 disabled for compatibility

### 2. Language Support
- **Auto-detection**: Automatically identifies spoken language
- **Manual specification**: Force English ("en") or Polish ("pl")
- Displays detected language in results when auto-detected

### 3. Model Selection
- **tiny**: Fastest, lowest accuracy
- **base**: Balanced speed/accuracy (default)
- **small**: Better accuracy
- **medium**: High accuracy
- **large**: Best accuracy, slowest

## Error Handling

### Validation Errors
- File not found with descriptive error message
- Unsupported file format with list of valid extensions
- Clear error messages with emoji indicators

### Processing Errors
- Model loading failures
- Transcription process errors
- Graceful exit with error code 1 on failures

## Dependencies

### Required Libraries
- `whisper` - OpenAI Whisper speech recognition
- `argparse` - Command-line argument parsing
- `os` - File system operations
- `sys` - System operations and exit codes

### Model Requirements
- Automatically downloads Whisper models on first use
- Models cached locally for subsequent runs
- No internet connection required after initial model download

## Performance Characteristics

### Model Size vs Performance
- **tiny**: ~75MB, fastest processing
- **base**: ~150MB, good balance
- **small**: ~500MB, better accuracy
- **medium**: ~1.5GB, high accuracy
- **large**: ~3GB, best accuracy

### Processing Notes
- First run may be slower due to model downloading
- Larger models require more RAM and processing time
- Audio length directly impacts processing time

## Exit Codes
- **0**: Success
- **1**: Error (file not found, unsupported format, processing error)

## Compatibility
- **Python**: Compatible with Python 3.7+
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Audio**: Supports common audio and video formats with audio tracks

This specification provides a comprehensive overview of ftt's functionality, usage, and technical requirements for both end-users and developers.