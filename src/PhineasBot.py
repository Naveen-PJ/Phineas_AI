from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from dotenv import load_dotenv
import os

class SimpleChatBot:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from the environment variable
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.model_name = "llama3-70b-8192"
        self.chat_history = []
        self.subname = None

        self.memory = ConversationBufferWindowMemory(k=10)  # Store the last 10 interactions

        # Initialize Groq LLM
        self.groq_chat = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name
        )

    def ask(self, query):
        try:
            # Save chat history to memory
            for message in self.chat_history:
                self.memory.save_context({'input': message['human']}, {'output': message['AI']})

            # Combine the query with chat history
            full_query = f"User Query:\n{query}"

            # Get response from Groq
            conversation = ConversationChain(llm=self.groq_chat, memory=self.memory)
            response = conversation(full_query)

            # Update chat history
            message = {'human': query, 'AI': response['response']}
            self.chat_history.append(message)
            return response['response']
        except Exception as e:
            return f"An error occurred: {e}"

    def summarize(self, input_file, output_file):
        try:
            with open(input_file, "r") as f:
                text = f.read()

            # Create a summarization query
            summary_prompt = f"Summarize the following text \n{text}"
            key_points_prompt=f"Extract key points of the following text \n {text}"
            
            # Use Groq API to get the summary
            conversation = ConversationChain(llm=self.groq_chat)
            response = conversation.run(summary_prompt)  # Ensure this returns the expected format
            response_key_points = conversation.run(key_points_prompt)  # Ensure this returns the expected format

            # If the response is a dictionary or has keys like 'response', update accordingly
            if isinstance(response, dict):
                summary_text = response.get('response', '')  # Use .get() to safely retrieve the summary
            else:
                summary_text = response

            if isinstance(response_key_points,dict):
                key_points_text = response_key_points.get('response', '')  # Use .get() to
            else:
                key_points_text = response_key_points

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
            return output_file
        except Exception as e:
            return f"An error occurred during summarization: {e}"


# Example usage
if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    chatbot = SimpleChatBot()
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
            file_path = "sample.txt"
            try:
                summary_file = chatbot.summarize(file_path, file_path.replace(".txt", "_summary.txt"))
                print(f"Summary saved at: {summary_file}")
            except FileNotFoundError:
                print("File not found. Please try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
