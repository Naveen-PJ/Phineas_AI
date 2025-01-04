# Phineas_AI

## Overview
This project is a Python-based software designed to assist students and professors by automating the process of lecture recording, transcription, and summarization. The software also includes a feature to clarify doubts using a free large language model (LLM).

### Key Features
1. **Audio Recording**:
   - Record lectures in audio format (e.g., `.wav`) using open-source libraries.
2. **Transcription**:
   - Convert audio to text using OpenAI Whisper, an open-source speech-to-text model.
3. **Summarization**:
   - Generate concise summaries of the lecture, including key points, homework details, and additional insights, using free NLP models.
4. **Doubt Clarification**:
   - Address student questions in real-time or post-lecture by leveraging open-source LLMs for context-based answers.
5. **User Interface**:
   - A graphical user interface (GUI) built with Kivy for ease of use.
6. **Planned Feature: Live Transcription**:
   - Live transcription functionality will be added later, allowing real-time text display during lectures.

---

## Technologies Used

### Python Libraries
- **Audio Processing**:
  - `sounddevice`: For recording audio.
  - `wave`: For handling audio files.
- **Speech-to-Text**:
  - OpenAI Whisper: For transcription.
- **Natural Language Processing**:
  - Hugging Face Transformers: For summarization and question answering.
  - `spaCy`: For extracting key points and preprocessing text.
- **User Interface**:
  - `Kivy`: For creating a cross-platform GUI.

---

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (optional but recommended)
- CUDA-compatible GPU (optional for faster transcription)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Recording Audio
1. Run the recording script:
   ```bash
   python record_audio.py
   ```
2. The audio file will be saved in the `audio/` directory.

### Transcription
1. Transcribe the recorded audio:
   ```bash
   python transcribe_audio.py <audio_file>
   ```
2. The transcript will be saved as a `.txt` file in the `transcripts/` directory.

### Summarization
1. Summarize the lecture transcript:
   ```bash
   python summarize_text.py <transcript_file>
   ```
2. The summary will be displayed and saved to the `summaries/` directory.

### Doubt Clarification
1. Ask a question about the lecture:
   ```bash
   python clarify_doubt.py <transcript_file> "Your question here"
   ```
2. The system will provide a context-based answer.

---

## Folder Structure
```
project-directory/
|-- audio/
|   |-- recorded_lecture.wav
|-- transcripts/
|   |-- transcript.txt
|-- summaries/
|   |-- summary.txt
|-- src/
|   |-- record_audio.py
|   |-- transcribe_audio.py
|   |-- summarize_text.py
|   |-- clarify_doubt.py
|-- requirements.txt
|-- README.md
```

---

## Future Enhancements
1. **Live Transcription**:
   - Add real-time transcription functionality to display text during lectures.
2. **Enhanced UI**:
   - A more intuitive graphical interface with KivyMD components.
3. **Database Integration**:
   - Store transcripts, summaries, and doubts for future reference.
4. **Customization**:
   - Allow users to choose summarization styles or formats.

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