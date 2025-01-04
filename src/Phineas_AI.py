import sounddevice as sd
import wave
import whisper
from transformers import pipeline
from datetime import datetime
import threading

class Phineas_AI:
    def __init__(self):
        self.transcription_model = whisper.load_model("base")
        self.summarizer = pipeline("summarization")
        self.recording = False
        self.paused = False
        self.audio_frames = []
        self.fs = 44100  # Sample rate
        self.recording_thread = None
        self.audio_filename = ""

    def start_recording(self, folder="audio/"):
        """Start the recording process."""
        if self.recording:
            print("Recording is already in progress.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.audio_filename = f"{folder}lecture_{timestamp}.wav"
        self.recording = True
        self.paused = False
        self.audio_frames = []
        
        print("Starting recording...")
        self.recording_thread = threading.Thread(target=self._record_audio, args=(self.audio_filename,))
        self.recording_thread.start()

    def _record_audio(self, filename):
        """Internal method to handle audio recording."""
        def callback(indata, frames, time, status):
            if self.recording and not self.paused:
                self.audio_frames.append(indata.copy())

        print("Recording started. Press 'pause' or 'stop' to control recording.")

        with sd.InputStream(samplerate=self.fs, channels=2, callback=callback):
            while self.recording:
                sd.sleep(100)  # Allow time for pausing or stopping

        print("Recording complete. Saving file...")

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.fs)
            wf.writeframes(b''.join([frame.tobytes() for frame in self.audio_frames]))

        print(f"Saved to {filename}")

    def pause_recording(self):
        """Pause the recording."""
        if self.recording and not self.paused:
            self.paused = True
            print("Recording paused.")

    def resume_recording(self):
        """Resume the recording."""
        if self.recording and self.paused:
            self.paused = False
            print("Recording resumed.")

    def stop_recording(self):
        """Stop the recording."""
        if self.recording:
            self.recording = False
            self.paused = False
            print("Recording stopped.")
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join()

    def transcribe_audio(self, folder="transcripts/"):
        """Transcribe audio and save the transcript."""
        if not self.audio_filename:
            print("No audio file available for transcription.")
            return None

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{folder}transcript_{timestamp}.txt"

        print("Transcribing audio...")
        result = self.transcription_model.transcribe(self.audio_filename)
        with open(output_file, "w") as f:
            f.write(result['text'])

        print(f"Transcript saved to {output_file}")
        return output_file

    def summarize_text(self, input_file, folder="summaries/"):
        """Summarize text and save the summary."""
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

    # Start recording
    helper.start_recording()

    # Simulate user actions (pause, resume, stop)
    import time
    time.sleep(5)  # Simulate 5 seconds of recording
    helper.pause_recording()
    time.sleep(2)  # Simulate pause duration
    helper.resume_recording()
    time.sleep(5)  # Simulate additional recording time
    helper.stop_recording()

    # Transcribe and summarize the audio
    transcript_file = helper.transcribe_audio()
    if transcript_file:
        summary_file = helper.summarize_text(transcript_file)
