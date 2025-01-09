import speech_recognition as sr
from transformers import pipeline
from datetime import datetime
import threading
import os

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

        self.subname = None
        self.foldertrans = None
        self.foldersum = None
        self.folderaudio = None
        self.audiofilename = None

        self.lock = threading.Lock()
        self.initialize_folders()

    def initialize_folders(self):
        base_path = os.path.join("Phineas_AI", "Records")
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    def create_subfolders(self):
        self.foldertrans = os.path.join("Phineas_AI", "Records", self.subname, "Transcript_Folder")
        self.foldersum = os.path.join("Phineas_AI", "Records", self.subname, "Summary_Folder")
        self.folderaudio = os.path.join("Phineas_AI", "Records", self.subname, "Audio_Folder")

        for folder in [self.foldertrans, self.foldersum, self.folderaudio]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def start_transcription(self, subname):
        self.subname = subname
        self.create_subfolders()

        if self.transcribing:
            print("Transcription is already in progress.")
            return

        timestamp = datetime.now().strftime("-%Y-%m-%d_%I-%M-%p")
        self.transcription_filename = f"{self.foldertrans}/{self.subname}{timestamp}.txt"
        self.transcribing = True
        self.paused = False
        self.transcription_result = ""

        print("Starting transcription...")
        self.transcription_thread = threading.Thread(target=self._transcribe_audio)
        self.transcription_thread.start()

    def listen(self):
        timestamp = datetime.now().strftime("-%Y-%m-%d_%I-%M-%p")
        self.audiofilename = f"{self.folderaudio}/{self.subname}{timestamp}.wav"
        audio_data = []

        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            while self.transcribing:
                if not self.paused:
                    try:
                        audio = self.recognizer.listen(source, timeout=5)
                        audio_data.append(audio)
                    except sr.WaitTimeoutError:
                        print("Listening timed out while waiting for phrase to start.")
                    except Exception as e:
                        print(f"An error occurred while listening: {e}")

        self.save_audio_chunk(audio_data)

    def save_audio_chunk(self, audio_data):
        with open(self.audiofilename, "wb") as file:
            for audio in audio_data:
                file.write(audio.get_wav_data())
        print(f"Audio has been saved to '{self.audiofilename}'.")

    def transcribe(self):
        try:
            with sr.AudioFile(self.audiofilename) as source:
                audio = self.recognizer.record(source)
            self.transcription_result = self.recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from the Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        if self.transcription_result:
            with open(self.transcription_filename, "w") as f:
                f.write(self.transcription_result)
            print(f"Transcript saved to {self.transcription_filename}")
            self.summarize_text(self.transcription_filename)
        else:
            print("No transcription result to save.")

    def _transcribe_audio(self):
        while self.transcribing:
            if not self.paused:
                self.listen()
                self.transcribe()

    def pause_transcription(self):
        with self.lock:
            if self.transcribing:
                self.paused = True
                print("Transcription paused.")

    def resume_transcription(self):
        with self.lock:
            if self.transcribing and self.paused:
                self.paused = False
                print("Transcription resumed.")

    def stop_transcription(self):
        with self.lock:
            if self.transcribing:
                self.transcribing = False
                print("Transcription stopped.")
                if self.transcription_thread and self.transcription_thread.is_alive():
                    self.transcription_thread.join()

    def summarize_text(self, input_file):
        timestamp = datetime.now().strftime("-%Y-%m-%d_%I-%M-%p")
        output_file = f"{self.foldersum}/{self.subname}_Summary_{timestamp}.txt"

        with open(input_file, "r") as f:
            text = f.read()

        print("Summarizing text...")
        summary = self.summarizer(text, max_length=1500, min_length=10, do_sample=False)[0]['summary_text']
        with open(output_file, "w") as f:
            f.write(summary)

        print(f"Summary saved to {output_file}")
        return output_file

    def openrepo(self):
        path = os.path.join("Phineas_AI", "Records")
        os.startfile(path)

# Example usage
if __name__ == "__main__":
    helper = Phineas_AI()

    # Start transcription
    helper.start_transcription("Subject_Name")

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
