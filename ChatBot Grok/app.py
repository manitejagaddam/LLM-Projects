from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
import os
from dotenv import load_dotenv


load_dotenv()

api_key =  os.getenv("GROQ")


try:
    chat_model = ChatGroq(
        model="llama3-70b-8192",  
        temperature=0.7,   
        api_key=api_key     
    )

    conversation = ConversationChain(llm=chat_model)

except Exception as e:
    print(f"Error initializing the model: {e}")
    exit()

def chatbot():
    print("Chatbot: Hello! I am Grok. Type 'quit' to end the chat.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("Chatbot: Goodbye! Have a nice day.")
            break
        
        try:
            response = conversation.predict(input=user_input)
            print("Chatbot:", response)
        except Exception as e:
            print(f"Error during conversation: {e}")
            break

# Run the chatbot
chatbot()
