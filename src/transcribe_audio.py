import whisper
from datetime import datetime

def transcribe_audio(audio_file, folder="transcriptfolder/"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"{folder}transcript_{timestamp}.txt"
    
    model = whisper.load_model("base")
    print("Transcribing audio...")
    result = model.transcribe(audio_file)
    with open(output_file, "w") as f:
        f.write(result['text'])
    print(f"Transcript saved to {output_file}")

if __name__ == "__main__":
    transcribe_audio("audio/lecture_2024-12-26_14-45-30.wav")
