# type: ignore
import argparse
import whisper
import os
import sys

def transcribe_audio_file(file_path, model_name="base", language=None):
    """Transcribe an audio file using Whisper"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    # Validate file extension
    valid_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.mp4', '.webm', '.ogg'}
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in valid_extensions:
        print(f"❌ Unsupported file format: {file_ext}")
        print(f"✅ Supported formats: {', '.join(valid_extensions)}")
        sys.exit(1)
    
    print(f"📝 Transcribing {os.path.basename(file_path)}...")
    if language:
        print(f"🌐 Language: {language}")
    
    try:
        # Load model
        model = whisper.load_model(model_name)
        
        # Transcribe
        result = model.transcribe(
            file_path,
            language=language,  # Use specified language or auto-detect
            task="transcribe",
            fp16=False,
            no_speech_threshold=0.6
        )
        
        # Output results
        print("\n" + "="*50)
        print("📄 TRANSCRIPTION:")
        print("="*50)
        print(result["text"].strip())
        print("="*50)
        
        # Show detected language if auto-detected
        if not language:
            print(f"🔍 Detected language: {result['language']}")
        
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files to text using Whisper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ftt.py audio.mp3                    # Auto-detect language
  python ftt.py audio.mp3 --language en      # Force English
  python ftt.py audio.mp3 --language pl      # Force Polish
  python ftt.py audio.wav --model small --language en
        """
    )
    
    parser.add_argument(
        "file_path",
        help="Path to the audio file (MP3, WAV, M4A, FLAC, etc.)"
    )
    
    parser.add_argument(
        "--model", "-m",
        choices=["tiny", "base", "small", "medium", "large"],
        default="base",
        help="Whisper model size (default: base)"
    )
    
    parser.add_argument(
        "--language", "-l",
        choices=["en", "pl"],
        help="Force specific language: en (English) or pl (Polish). If not specified, auto-detect will be used."
    )
    
    args = parser.parse_args()
    
    transcribe_audio_file(args.file_path, args.model, args.language)

if __name__ == "__main__":
    main()