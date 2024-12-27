from transformers import pipeline
from datetime import datetime

def summarize_text(input_file, folder="summaries/"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = f"{folder}summary_{timestamp}.txt"
    
    with open(input_file, "r") as f:
        text = f.read()
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    with open(output_file, "w") as f:
        f.write(summary)
    print(f"Summary saved to {output_file}")

if __name__ == "__main__":
    summarize_text("transcripts/transcript_2024-12-26_14-45-30.txt")
