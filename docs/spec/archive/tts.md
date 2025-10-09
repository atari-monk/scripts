# tts (Text-to-Speech) Tool - Technical Specification

## Overview
**tts** is a command-line text-to-speech tool that converts text into spoken audio using the `pyttsx3` library. The tool supports both direct text input and clipboard text extraction, with configurable voice settings for language and gender.

## CLI API Definition

```sh
tts [--text TEXT] [--lang LANGUAGE] [--gender GENDER]
```

### Arguments
- **--text** (optional): Direct text input to speak
- **--lang** (optional): Language selection - "en" (English) or "pl" (Polish), defaults to "en"
- **--gender** (optional): Voice gender - "male" or "female", defaults to "female"

## Usage Examples

```sh
python tts.py --text "Hello world"                    # Speak direct text
python tts.py --text "Hello" --lang en --gender male # English male voice
python tts.py --lang pl --gender female              # Polish female voice from clipboard
python tts.py                                        # Use clipboard text with default settings
```

## Input Sources

### Text Input Methods
1. **Direct text** (`--text` argument): Provided as command-line argument
2. **Clipboard**: Automatically uses clipboard content when no `--text` provided
3. **Clipboard requirements**: Must contain non-empty text content

### Text Processing
- Handles plain text input
- No character limits (subject to system TTS engine capabilities)
- Preserves original text formatting for speech

## Voice Configuration

### Supported Languages
- **English (en)**: Primary supported language
- **Polish (pl)**: Secondary supported language

### Voice Gender Options
- **female**: Default female voice
- **male**: Male voice option

### Voice Selection Logic
```python
if language == 'en' and gender == 'female': voice[0]
elif language == 'en' and gender == 'male': voice[1]  
elif language == 'pl' and gender == 'female': voice[2]
else: default system voice
```

## Output Features

### Audio Output
- Real-time speech synthesis
- System audio output through default speakers
- No audio file generation (direct playback only)

### Console Feedback
```
📋 Using text from clipboard
🔊 Speaking with en-female voice
🎤 Speaking: [text content]
```

## Error Handling

### Input Validation
- Empty clipboard detection with helpful message
- Clipboard access errors with installation guidance
- Graceful fallback to default voice for unsupported combinations

### Error Messages
- "❌ Clipboard is empty! Please copy some text first or use --text argument."
- "❌ Error accessing clipboard: [error details]"
- "💡 Make sure you have pyperclip installed: pip install pyperclip"
- "❌ No voice found for [lang]-[gender], using default"

## Dependencies

### Required Libraries
- `pyttsx3` - Text-to-speech engine
- `pyperclip` - Clipboard operations  
- `argparse` - Command-line argument parsing

### Installation
```bash
pip install pyttsx3 pyperclip
```

### System Requirements
- **Platform**: Windows, macOS, Linux (with system TTS support)
- **Audio**: Functional audio output system
- **Python**: 3.6+

## Voice Availability Notes

### Platform Differences
- Voice availability varies by operating system
- Polish voice support depends on system-installed voices
- Default fallback to system default voice when requested voice unavailable

### Voice Quality
- Dependent on system TTS engines and installed voices
- No external voice download (uses system-provided voices)
- Real-time synthesis without internet connection

## Usage Scenarios

### Primary Use Cases
1. **Quick text playback** from clipboard
2. **Language learning** with different voice genders
3. **Accessibility** tool for visually impaired users
4. **Proofreading** by hearing written text

### Workflow Integration
- Can be chained with other text-processing tools
- Useful in scripts for audio feedback
- Complements the `ftt` speech-to-text tool

## Limitations

### Current Constraints
- No audio file output (playback only)
- Limited to system-installed voices
- No voice speed/volume control in current implementation
- No batch processing of multiple texts

### Known Issues
- Voice selection may not work consistently across all platforms
- Polish voice availability varies by system configuration

This specification provides complete documentation for the tts tool's functionality, requirements, and usage patterns for both end-users and developers.