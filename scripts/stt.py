# type: ignore
import pyaudio
import wave
import keyboard
import whisper
import numpy as np

def record_audio():
    CHUNK = 1024  # Smaller chunk for lower latency
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000  # Whisper works best with 16kHz
    
    p = pyaudio.PyAudio()
    
    # Check available devices and use default
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        input_device_index=None  # Use default device
    )
    
    print("🎤 Recording... Press ENTER to stop")
    frames = []
    
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            if keyboard.is_pressed('enter'):
                break
    except KeyboardInterrupt:
        pass
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # Save as WAV
    filename = "C:/Atari-Monk/scripts/data/recording.wav"
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    return filename

def main():
    # Model selection - base offers best balance of speed/accuracy
    model_name = "base"  # tiny/base/small/medium/large
    
    # Record audio
    audio_file = record_audio()
    
    # Load model and transcribe
    print("📝 Transcribing...")
    model = whisper.load_model(model_name)
    
    # Optimized transcription parameters
    result = model.transcribe(
        audio_file,
        language="en",
        task="transcribe",  # Explicitly set to transcription
        fp16=False,  # Use FP32 for better accuracy on CPU
        no_speech_threshold=0.6  # Better handling of silence
    )
    
    print("\n" + "="*50)
    print("📄 TRANSCRIPTION:")
    print("="*50)
    print(result["text"].strip())
    print("="*50)

if __name__ == "__main__":
    main()