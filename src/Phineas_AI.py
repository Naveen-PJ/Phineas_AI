import speech_recognition as sr
from transformers import pipeline
from datetime import datetime
import threading
import os

foldertrans = os.path.join("Phineas_AI", "Transcriptfolder")
foldersum = os.path.join("Phineas_AI", "Summeryfolder")

# Ensure the folders exist
if not os.path.exists(foldertrans):
    os.makedirs(foldertrans)
if not os.path.exists(foldersum):
    os.makedirs(foldersum)

class Phineas_AI:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.transcribing = False
        self.paused = False
        self.transcription_thread = None
        self.transcription_result = ""
        self.transcription_filename = ""

    def start_transcription(self, folder=foldertrans):
        """Start the transcription process."""
        if self.transcribing:
            print("Transcription is already in progress.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.transcription_filename = f"{folder}\Transcript_{timestamp}.txt"
        self.transcribing = True
        self.paused = False
        self.transcription_result = ""

        print("Starting transcription...")
        self.transcription_thread = threading.Thread(target=self._transcribe_audio)
        self.transcription_thread.start()

    def _transcribe_audio(self):
        """Internal method to handle audio transcription."""
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while self.transcribing:
                if not self.paused:
                    try:
                        print("Listening...")
                        audio = self.recognizer.listen(source)
                        print("Transcribing...")
                        text = self.recognizer.recognize_google(audio)
                        self.transcription_result += text + " "
                        print(f"Recognized Text: {text}")
                    except sr.RequestError as e:
                        print(f"API unavailable or unresponsive: {e}")
                    except sr.UnknownValueError:
                        print("Unable to recognize speech. Skipping this part.")
                    except Exception as e:
                        print(f"An error occurred: {e}")

        # Print and Save the transcription result
        print(f"Final Transcription Result: {self.transcription_result}")
        if self.transcription_result:
            with open(self.transcription_filename, "w") as f:
                f.write(self.transcription_result)
            print(f"Transcript saved to {self.transcription_filename}")
        else:
            print("No transcription result to save.")

    def pause_transcription(self):
        """Pause the transcription."""
        if self.transcribing and not self.paused:
            self.paused = True
            print("Transcription paused.")

    def resume_transcription(self):
        """Resume the transcription."""
        if self.transcribing and self.paused:
            self.paused = False
            print("Transcription resumed.")

    def stop_transcription(self):
        """Stop the transcription."""
        if self.transcribing:
            self.transcribing = False
            print("Transcription stopped.")
            if self.transcription_thread and self.transcription_thread.is_alive():
                self.transcription_thread.join()

    def summarize_text(self, input_file, folder=foldersum):
        """Summarize text and save the summary."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"{folder}\Summary_{timestamp}.txt"

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

    # Start transcription
    helper.start_transcription()

    import time
    time.sleep(10)  # Simulate 10 seconds of transcription

    # Pause transcription
    helper.pause_transcription()
    time.sleep(2)  # Simulate pause duration

    # Resume transcription
    helper.resume_transcription()
    time.sleep(10)  # Simulate additional transcription time

    # Stop transcription
    helper.stop_transcription()

    # Summarize the transcript
    transcript_file = helper.transcription_filename
    if transcript_file:
        summary_file = helper.summarize_text(transcript_file)
