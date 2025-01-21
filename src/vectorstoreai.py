import logging
import os
from langchain.vectorstores import FAISS
from langchain.embeddings import SpacyEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import spacy
from langchain.docstore.document import Document

# Ensure the Logs directory exists
log_dir = os.path.join("Phineas_AI", "Data", "Logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging to save to a file in the Logs directory
logging.basicConfig(
    filename=os.path.join(log_dir, 'embedding_faiss.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EmbeddingManager:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")  # Load the spaCy model
        self.embeddings = SpacyEmbeddings()  # Initialize SpacyEmbeddings with spaCy model
        
        # Initialize FAISS index
        self.faiss_index = None

        logging.info("EmbeddingManager initialized.")

    def create_embeddings(self, input_texts):
        try:
            logging.info("Creating embeddings for input texts.")

            # Split texts into manageable chunks
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = []

            for text in input_texts:
                chunks = splitter.split_text(text)
                for chunk in chunks:
                    docs.append(Document(page_content=chunk))

            # Generate embeddings and store in FAISS
            self.faiss_index = FAISS.from_documents(docs, self.embeddings)

            logging.info("Embeddings created and stored in FAISS index.")
        except Exception as e:
            logging.error(f"Error creating embeddings: {e}")
            raise e

    def query_embeddings(self, query_text, k=3):
        try:
            if not self.faiss_index:
                raise ValueError("FAISS index is empty. Create embeddings first.")

            logging.info(f"Querying FAISS index for: {query_text}")

            # Search for similar documents
            results = self.faiss_index.similarity_search(query_text, k=k)
            return [result.page_content for result in results]
        except Exception as e:
            logging.error(f"Error querying embeddings: {e}")
            raise e

# Example usage
if __name__ == "__main__":
    embedding_manager = EmbeddingManager()

    # Sample texts
    texts = [
        "Machine learning is a fascinating field of study.",
        "Natural language processing enables machines to understand text.",
        "FAISS is a library for efficient similarity search.",
    ]

    # Create embeddings and store them in FAISS
    embedding_manager.create_embeddings(texts)

    # Query the FAISS index
    query = "What is FAISS used for?"
    similar_texts = embedding_manager.query_embeddings(query)

    print("Top similar texts:")
    for idx, text in enumerate(similar_texts, start=1):
        print(f"{idx}. {text}")