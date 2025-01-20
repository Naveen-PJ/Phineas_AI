from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferWindowMemory
from groq import ChatGroq
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os
from datetime import datetime



class SimpleChatBot:
    def __init__(self, groq_api_key, pdf_text):
        self.groq_api_key = groq_api_key
        self.model_name ="llama3-70b-8192"
        self.pdf_text = pdf_text
        self.chat_history = []
        self.subname = None

        self.memory = ConversationBufferWindowMemory(k=5)  # Store the last 5 interactions
        
        # Initialize vector store
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = self.text_splitter.split_text(pdf_text)
        embeddings = OpenAIEmbeddings()
        self.vector_store = FAISS.from_texts(chunks, embeddings)

        # Initialize Groq LLM
        self.groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )

    def ask(self, query):
        try:
            # Retrieve relevant chunks
            relevant_chunks = self.vector_store.similarity_search(query, k=5)
            relevant_text = "\n".join([chunk.page_content for chunk in relevant_chunks])
            
            # Save chat history to memory
            for message in self.chat_history:
                self.memory.save_context({'input': message['human']}, {'output': message['AI']})

            # Combine relevant content with query
            full_query = f"Relevant PDF Content:\n{relevant_text}\n\nUser Query:\n{query}"
            
            # Get response from Groq
            conversation = ConversationChain(llm=self.groq_chat, memory=self.memory)
            response = conversation(full_query)
            

            # Update chat history
            message = {'human': query, 'AI': response['response']}
            self.chat_history.append(message)
            return response['response']
        except Exception as e:
            return f"An error occurred: {e}"

    def summarize(self,input_file):
        try:
            self.foldersum = os.path.join("Phineas_AI", "Records", self.subname, "Summary_Folder")
            timestamp = datetime.now().strftime("-%Y-%m-%d_%I-%M-%p")
            output_file = f"{self.foldersum}/{self.subname}_Summary_{timestamp}.txt"

            with open(input_file, "r") as f:
                text = f.read()
            # Create a summarization query
            summary_prompt = f"Summarize the following text:\n{text}"
            
            # Use Groq API to get the summary
            conversation = ConversationChain(llm=self.groq_chat)
            response = conversation(summary_prompt)
            summary_text = response['response']

            with open(output_file, "w") as f:
                for line in summary_text:
                    f.write(line + "\n")  # Write each line with a newline character

            return output_file

        except Exception as e:
            return f"An error occurred during summarization: {e}"

# Example usage
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    # Get the API key from the environment variable
    groq_api_key = os.getenv("GROQ_API_KEY")
    pdf_text = "Your PDF text content here"  # Replace with your PDF text

    chatbot = SimpleChatBot(groq_api_key, pdf_text)
    print("Chatbot is ready! Type 'exit' to quit.")

    while True:
        print("\nOptions:")
        print("1: Ask a question")
        print("2: Summarize a text file")
        print("3: Exit")
        
        choice = input("Choose an option: ")
        if choice == '1':
            user_query = input("Your Query: ")
            response = chatbot.ask(user_query)
            print(f"Chatbot: {response}")
        elif choice == '2':
            file_path = input("Enter the path of the text file to summarize: ")
            try:
                with open(file_path, 'r') as file:
                    text_content = file.read()
                summary = chatbot.summarize(text_content)
                print(f"Summary:\n{summary}")
            except FileNotFoundError:
                print("File not found. Please try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
