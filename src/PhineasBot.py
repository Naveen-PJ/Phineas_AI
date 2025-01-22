// import logging
import os
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
from src.vectorstoreai import EmbeddingManager


# Ensure the Logs directory exists
log_dir = os.path.join("Phineas_AI", "Data", "Logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging to save to a file in the Logs directory
logging.basicConfig(
    filename=os.path.join(log_dir, 'phineas_ai_with_vectors.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ChatBotWithVectors:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Initialize required components
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.model_name = "llama3-70b-8192"
        self.chat_history = []

        self.memory = ConversationBufferWindowMemory(k=10)  # Store the last 10 interactions

        # Initialize Groq LLM
        self.groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )

        # Initialize embedding manager
        self.embedding_manager = EmbeddingManager()
        self.faiss_index = faiss.IndexFlatL2(512)  # Assuming 512-dimensional embeddings

        logging.info("ChatBotWithVectors initialized.")

    def add_to_faiss_index(self, texts):
        embeddings = self.embedding_manager.create_embeddings(texts)
        self.faiss_index.add(embeddings)

    def search_faiss_index(self, query, k=5):
        query_embedding = self.embedding_manager.create_embeddings([query])
        distances, indices = self.faiss_index.search(query_embedding, k)
        return indices

    def ask(self, query):
        try:
            logging.info(f"Received query: {query}")

            # Save chat history to memory
            for message in self.chat_history:
                self.memory.save_context({'input': message['human']}, {'output': message['AI']})

            # Check for similar texts in the FAISS index
            similar_indices = self.search_faiss_index(query)
            similar_texts = [self.embedding_manager.get_text_by_index(idx) for idx in similar_indices[0]]
            if similar_texts:
              # If similar texts are found, include them as context
                context = "\n".join(similar_texts)
                full_query = f"User Query:\n{query}\n\nContext:\n{context}"
            else:
                # If no similar texts are found, proceed to query the LLM directly
                full_query = f"User Query:\n{query}"

            # Get response from Groq
                conversation = ConversationChain(llm=self.groq_chat, memory=self.memory)
                response = conversation(full_query)

            # Update chat history
            message = {'human': query, 'AI': response['response']}
            self.chat_history.append(message)

            logging.info(f"Response generated: {response['response']}".strip())
            return response['response']
        except Exception as e:
            logging.error(f"Error during query handling: {e}")
            return f"An error occurred: {e}"


    def add_to_vector_store(self, texts):
        try:
            logging.info("Adding texts to vector store.")
            self.embedding_manager.create_embeddings(texts)
            logging.info("Texts added to vector store successfully.")
        except Exception as e:
            logging.error(f"Error adding texts to vector store: {e}")
            return f"An error occurred while adding to vector store: {e}"

    def summarize(self, input_file, output_file):
        try:
            logging.info(f"Starting summarization for file: {input_file}")

            with open(input_file, "r") as f:
                text = f.read()

            # Create a summarization query
            summary_prompt = f"Summarize the following text:\n{text}"
            key_points_prompt = f"Extract key points of the following text:\n{text}"

            # Use Groq API to get the summary
            conversation = ConversationChain(llm=self.groq_chat)
            response = conversation.run(summary_prompt)
            response_key_points = conversation.run(key_points_prompt)

            summary_text = response if isinstance(response, str) else response.get('response', '')
            key_points_text = response_key_points if isinstance(response_key_points, str) else response_key_points.get('response', '')

            max_words_per_line = 20  # Maximum words per line
            words = summary_text.split()
            summary_lines = [' '.join(words[i:i + max_words_per_line]) 
                            for i in range(0, len(words), max_words_per_line)]

            with open(output_file, "w") as f:
                for line in summary_lines:
                    f.write(line + "\n")  # Write each line with a newline character
                f.write("\n\nKEY POINTS\n")
                for line in key_points_text.split('\n'):
                    f.write(line + "\n")

            # Add the summary to the vector store
            self.add_to_vector_store([summary_text])

            logging.info(f"Summarization completed. Output saved to: {output_file}")
            return output_file
        except Exception as e:
            logging.error(f"Error during summarization: {e}")
            return f"An error occurred during summarization: {e}"

# Example usage
if __name__ == "__main__":
    chatbot = ChatBotWithVectors()

    print("Chatbot is ready! Type 'exit' to quit.")

    while True:
        print("\nOptions:")
        print("1: Ask a question")
        print("2: Add texts to vector store")
        print("3: Summarize a text file")
        print("4: Exit")

        choice = input("Choose an option: ")
        if choice == '1':
            user_query = input("Your Query: ")
            response = chatbot.ask(user_query)
            print(f"Chatbot: {response}")
        elif choice == '2':
            print("Enter texts to add to the vector store (type 'END' on a new line to finish):")
            input_texts = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                input_texts.append(line)

            result = chatbot.add_to_vector_store(input_texts)
            if result:
                print(result)
            else:
                print("Texts added successfully.")
        elif choice == '3':
            file_path = input("Enter the path of the file to summarize: ")
            output_path = file_path.replace(".txt", "_summary.txt")
            result = chatbot.summarize(file_path, output_path)
            print(f"Summary saved to: {result}" if not result.startswith("An error occurred") else result)
        elif choice == '4':
            print("Goodbye!")
            logging.info("Chatbot session ended.")
            break
        else:
            print("Invalid choice. Please try again.")
