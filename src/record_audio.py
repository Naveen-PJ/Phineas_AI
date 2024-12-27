import sounddevice as sd
import wave
from datetime import datetime

def record_audio(duration, folder="audioclipsfolder/"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{folder}lecture_{timestamp}.wav"
    
    fs = 44100  # Sample rate
    print("Recording...")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait for recording to finish
    print("Recording complete. Saving file...")
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())
    print(f"Saved to {filename}")

if __name__ == "__main__":
    record_audio(10)  # Record for 10 seconds
