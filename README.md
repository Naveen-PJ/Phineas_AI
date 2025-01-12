# Phineas_AI

## Overview
Phineas AI is a Python-based software designed to record entire lectures or classes, transcribe them into text, and generate concise summaries. The summaries include key points such as homework details, additional points discussed by the professor, and answers to student doubts. The software uses the `facebook/bart-large-cnn` model for summarization and has a user-friendly interface built with Kivy.

### Key Features

1. **Transcription**:
   - Converts the recorded audio into text using speech recognition.
2. **Summarization**:
   - Generates summaries of the lecture using the `facebook/bart-large-cnn` model, including key points, homework details, and professor's extra discussions.
3. **Doubt Clarification**:
   - A future feature to clarify students' doubts during the lecture.
4. **User Interface**:
   - A simple Kivy-based interface for an easy user experience.

---

## Technologies Used

- **Python**: The primary programming language used to build the software.
- **Transformers**: The `transformers` library by Hugging Face is used for text summarization with the `facebook/bart-large-cnn` model.
- **Kivy**: A Python framework for building the graphical user interface.
- **Speech Recognition**: Used to record audio.
- **Whisper**: Used for transcribing audio using the Whisper model.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Naveen-PJ/Phineas_AI.git
   cd Phineas_AI
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the following libraries installed:
   - `transformers` (for the `facebook/bart-large-cnn` model)
   - `Kivy`
   - `SpeechRecognition`
   - `whisper`
   - Other dependencies listed in `requirements.txt`.
   - **ffmpeg** (required for OpenAI-Whisper to handle audio file preprocessing)

4. Download the necessary Hugging Face model for summarization (this will be handled automatically by the `transformers` library when needed):
   ```bash
   pip install transformers
   ```

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- A working internet connection (for downloading required models)
- **ffmpeg** (required for OpenAI-Whisper to handle audio file preprocessing)

---

## Usage

### Recording Audio
1. To run the software, use the following command:
   ```bash
   python main.py
   ```

2. The program will begin recording the lecture. Once the lecture is complete, it will transcribe the audio and generate a summary containing the key points discussed during the lecture, using the `facebook/bart-large-cnn` model.

3. After the lecture, the summary will be presented. The software will also have a feature to clarify any doubts raised during the lecture (future feature).

---

## Folder Structure
```
Phineas_AI/
|-- Records/
|   |-- subject1/
|   |   |-- Transcript_Folder
|   |   |-- Summary_Folder
|   |-- subject2/
|   |   |-- Transcript_Folder
|   |   |-- Summary_Folder
|   ...
|-- Logs/  # .log files are created only if any error occurs during the execution of the program
|   |-- log1.log
|   |-- log2.log
|-- src/
|   |-- __pycache__/
|   |-- __init__.py
|   |-- Phineas_AI.py
|-- main.py
|-- .gitignore
|-- requirements.txt
|-- README.md
```

---

## Future Enhancements
1. **Live Transcription**:
   - Real-time transcription of lectures to be implemented.
2. **Enhanced UI**:
   - A more intuitive graphical interface with KivyMD components.
3. **Database Integration**:
   - Store transcripts, summaries, and doubts for future reference.
4. **Customization**:
   - Allow users to choose summarization styles or formats.
5. **Doubt Clarification**:
   - Providing responses to students' doubts during the lecture using NLP (future feature).

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---