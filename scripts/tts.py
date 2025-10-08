# type: ignore
import pyttsx3 
import argparse
import pyperclip

def text_to_speech(text: str, language: str = 'en', gender: str = 'female'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if language == 'en' and gender == 'female':
        engine.setProperty('voice', voices[0].id)
    elif language == 'en' and gender == 'male':
        engine.setProperty('voice', voices[1].id)
    elif language == 'pl' and gender == 'female':
        engine.setProperty('voice', voices[2].id)
    else:
        print(f"❌ No voice found for {language}-{gender}, using default")
    
    print(f"🔊 Speaking with {language}-{gender} voice")
    engine.say(text)
    engine.runAndWait()

def main():
    parser = argparse.ArgumentParser(description='Text-to-Speech with strict voice selection')
    parser.add_argument('--text', type=str, help='Text to speak (if not provided, uses clipboard)')
    parser.add_argument('--lang', type=str, default='en', choices=['en', 'pl'], help='Language (en/pl)')
    parser.add_argument('--gender', type=str, default='female', choices=['male', 'female'], help='Voice gender')
    
    args = parser.parse_args()
    
    if args.text:
        text = args.text
    else:
        try:
            text = pyperclip.paste()
            if not text.strip():
                print("❌ Clipboard is empty! Please copy some text first or use --text argument.")
                return
            print(f"📋 Using text from clipboard")
        except Exception as e:
            print(f"❌ Error accessing clipboard: {e}")
            print("💡 Make sure you have pyperclip installed: pip install pyperclip")
            return
    
    print(f"🎤 Speaking: {text}")
    text_to_speech(text, args.lang, args.gender)

if __name__ == "__main__":
    main()
