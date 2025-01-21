import speech_recognition as sr
from datetime import datetime
import threading
import os
import whisper
import logging
from src.PhineasBot import ChatBotWithVectors

class Phineas_AI:

    def __init__(self):
        self.whisper_model = whisper.load_model("base")
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
        self.vector_store = None

        self.lock = threading.Lock()
        self.initialize_folders()
        

        # Ensure the Logs directory exists
        log_dir = os.path.join("Phineas_AI","Data","Logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Set up logging to save to a file in the Logs directory
        logging.basicConfig(
            filename=os.path.join(log_dir, 'phineas_ai.log'),  # Specify the log file path
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def initialize_folders(self):
        base_path = os.path.join("Phineas_AI", "Records")
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    def create_subfolders(self):
        self.foldertrans = os.path.join("Phineas_AI", "Records", self.subname, "Transcript_Folder")
        self.foldersum = os.path.join("Phineas_AI", "Records", self.subname, "Summary_Folder")
        self.folderaudio = os.path.join("Phineas_AI", "Records", self.subname, "Audio_Folder")
        #self.vector_store = os.path.join("Phineas_AI", "Data", "Database")

        for folder in [self.foldertrans, self.foldersum, self.folderaudio]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    def start_transcription(self, subname):
        self.subname = subname
        self.create_subfolders()

        if self.transcribing:
            logging.info("Transcription is already in progress.")
            return

        timestamp = datetime.now().strftime("-%Y-%m-%d_%I-%M-%p")
        self.transcription_filename = f"{self.foldertrans}/{self.subname}{timestamp}.txt"
        self.transcribing = True
        self.paused = False
        self.transcription_result = ""

        logging.info("Starting transcription...")
        self.transcription_thread = threading.Thread(target=self._transcribe_audio)
        self.transcription_thread.start()

    def listen(self):
        audio_data = []
        while self.transcribing:
            self.timestamp = datetime.now().strftime("-%Y-%m-%d_%I-%M-%p")
            # Use a fixed filename for the entire recording
            self.audiofilename = f"{self.folderaudio}/{self.subname}_{self.timestamp}.wav"

            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source)
                logging.info("Listening...")

                if not self.paused:
                    try:
                        audio = self.recognizer.listen(source, timeout=60)  # Set listening timeout to 60 seconds
                        audio_data.append(audio)
                    except sr.WaitTimeoutError:
                        logging.warning("Listening timed out while waiting for phrase to start.")
                    except Exception as e:
                        logging.error(f"An error occurred while listening: {e}")

            if len(audio_data) >= 5:  # Buffer 5 chunks before saving
                self.save_audio_chunk(audio_data)
                audio_data = []  # Clear the buffer

        # Save and transcribe any remaining audio data
        if audio_data:
            self.save_audio_chunk(audio_data)
        self.transcribe()

    def save_audio_chunk(self, audio_data):
        with open(self.audiofilename, "ab") as file:
            for audio in audio_data:
                file.write(audio.get_wav_data())
        logging.info(f"Audio has been saved to '{self.audiofilename}'.")

    def transcribe(self):
        try:
            # Use Whisper to transcribe the audio file
            logging.info(f"Transcribing audio using Whisper: {self.audiofilename}")
            result = self.whisper_model.transcribe(self.audiofilename)
            self.transcription_result = result["text"]

        except Exception as e:
            logging.error(f"An error occurred with Whisper transcription: {e}")

        if self.transcription_result:
            # Split the text into lines based on a fixed number of words
            max_words_per_line = 10  # Maximum words per line
            words = self.transcription_result.split()
            lines = [' '.join(words[i:i + max_words_per_line]) 
                     for i in range(0, len(words), max_words_per_line)]

            with open(self.transcription_filename, "a") as f:  # Append to the file instead of overwriting
                for line in lines:
                    f.write(line + "\n")  # Write each line with a newline character

            logging.info(f"Transcript saved to {self.transcription_filename}")
            output_file = f"{self.foldersum}/{self.subname}_Summary_{self.timestamp}.txt"
            self.bot=ChatBotWithVectors()
            self.bot.summarize(self.transcription_filename,output_file)
        else:
            logging.warning("No transcription result to save.")


    def _transcribe_audio(self):
        while self.transcribing:
            if not self.paused:
                self.listen()

    def pause_transcription(self):
        with self.lock:
            if self.transcribing:
                self.paused = True
                logging.info("Transcription paused.")

    def resume_transcription(self):
        with self.lock:
            if self.transcribing and self.paused:
                self.paused = False
                logging.info("Transcription resumed.")

    def stop_transcription(self):
        with self.lock:
            if self.transcribing:
                self.transcribing = False
                logging.info("Transcription stopped.")
                if self.transcription_thread and self.transcription_thread.is_alive():
                    self.transcription_thread.join()
        
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

    # Stop transcription
    helper.stop_transcription()