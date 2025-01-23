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

        # Path to the FAISS index file
        index_dir = os.path.join("Phineas_AI", "Data", "Database")
        self.index_file = os.path.join(index_dir, "faiss_index.bin")

        # Try to load an existing FAISS index
        self.faiss_index = self._load_faiss_index()

        logging.info("EmbeddingManager initialized.")

    def get_dir(self, index_dir):
        self.index_file = os.path.join(index_dir, "faiss_index.bin")
        

    def _save_faiss_index(self):
        """Save the FAISS index to a file."""
        if self.faiss_index is not None:
            self.faiss_index.save_local(self.index_file)
            logging.info(f"FAISS index saved to {self.index_file}.")

    def _load_faiss_index(self):
        """Load the FAISS index from a file."""
        if os.path.exists(self.index_file):
            try:
                logging.info(f"Loading FAISS index from {self.index_file}.")
                return FAISS.load_local(self.index_file, self.embeddings)
            except Exception as e:
                logging.error(f"Failed to load FAISS index: {e}")
                return None
        logging.info("No existing FAISS index found. Starting fresh.")
        return None

    def create_embeddings(self, input_texts):
        """Create embeddings and store them in the FAISS index."""
        try:
            logging.info("Creating embeddings for input texts.")

            # Split texts into manageable chunks
            splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = []

            for text in input_texts:
                chunks = splitter.split_text(text)
                for chunk in chunks:
                    docs.append(Document(page_content=chunk))

            # Create a new FAISS index or append to the existing one
            if self.faiss_index:
                logging.info("Appending new documents to the existing FAISS index.")
                self.faiss_index.add_documents(docs)
            else:
                logging.info("Creating a new FAISS index with the provided documents.")
                self.faiss_index = FAISS.from_documents(docs, self.embeddings)

            # Save the updated index to disk
            self._save_faiss_index()
            logging.info("Embeddings created and stored in FAISS index.")
        except Exception as e:
            logging.error(f"Error creating embeddings: {e}")
            raise e

    def query_embeddings(self, query_text, k=3):
        """Search for similar documents in the FAISS index."""
        try:
            if not self.faiss_index:
                raise ValueError("FAISS index is empty. Create embeddings first.")

            logging.info(f"Querying FAISS index for: {query_text}")

            # Search for similar documents
            results = self.faiss_index.similarity_search(query_text, k=k)
        
            # If no results are found, return None
            if not results:
                logging.info("No similar documents found.")
                return None
        
            return [result.page_content for result in results]
        except Exception as e:
            logging.error(f"Error querying embeddings: {e}")
            raise e



# Example usage
if __name__ == "__main__":
    embedding_manager = EmbeddingManager(index_file="faiss_index.bin")

    # Add initial data
    texts = [
        "Machine learning is a fascinating field of study.",
        "Natural language processing enables machines to understand text.",
    ]
    embedding_manager.create_embeddings(texts)

    # Append new data
    new_texts = ["FAISS is a library for efficient similarity search."]
    embedding_manager.create_embeddings(new_texts)

    # Query the FAISS index
    query = "What is FAISS used for?"
    similar_texts = embedding_manager.query_embeddings(query)

    print("Top similar texts:")
    for idx, text in enumerate(similar_texts, start=1):
        print(f"{idx}. {text}")
