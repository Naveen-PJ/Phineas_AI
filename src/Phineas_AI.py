import sounddevice as sd
import wave
import whisper
from transformers import pipeline
from datetime import datetime

class Phineas_AI:
    def __init__(self):
        # Initialize resources if needed
        self.transcription_model = whisper.load_model("base")
        self.summarizer = pipeline("summarization")

    def record_audio(self, duration, folder="audio/"):
        """Record audio and save it to a file."""
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
        return filename

    def transcribe_audio(self, audio_file, folder="transcripts/"):
        """Transcribe audio and save the transcript to a file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{folder}transcript_{timestamp}.txt"

        print("Transcribing audio...")
        result = self.transcription_model.transcribe(audio_file)
        with open(output_file, "w") as f:
            f.write(result['text'])

        print(f"Transcript saved to {output_file}")
        return output_file

    def summarize_text(self, input_file, folder="summaries/"):
        """Summarize text and save the summary to a file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{folder}summary_{timestamp}.txt"

        with open(input_file, "r") as f:
            text = f.read()

        print("Summarizing text...")
        summary = self.summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        with open(output_file, "w") as f:
            f.write(summary)

        print(f"Summary saved to {output_file}")
        return output_file

# Example usage
if __name__ == "__main__":
    helper = Phineas_AI()

    # Record audio for 10 seconds
    audio_file = helper.record_audio(10)

    # Transcribe the recorded audio
    transcript_file = helper.transcribe_audio(audio_file)

    # Summarize the transcript
    summary_file = helper.summarize_text(transcript_file)
