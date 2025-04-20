import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key
api_key = os.getenv("GROQ") 

# Initialize the model
try:
    chat_model = ChatGroq(
        model="llama3-70b-8192",
        temperature=0.7,
        api_key=api_key
    )
    conversation = ConversationChain(llm=chat_model)
except Exception as e:
    st.error(f"Error initializing the model: {e}")
    st.stop()

# Page config
st.set_page_config(page_title="Grok Chatbot", layout="wide")

# Custom dark styling
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: white;
    }
    .block-container {
        background-color: #121212;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 75%;
        line-height: 1.5;
        word-wrap: break-word;
        font-size: 1rem;
    }
    .user {
        background-color: #0B93F6;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .bot {
        background-color: #2E2E2E;
        color: white;
        align-self: flex-start;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:white;'>🤖 Chatbot 🤖 </h1>", unsafe_allow_html=True)

# --- Chat state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat input (always at bottom) ---
user_input = st.chat_input("Type your message...")

# --- Only generate a reply immediately after user submits ---
if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "text": user_input})

    try:
        bot_response = conversation.predict(input=user_input)
    except Exception as e:
        bot_response = f"Error: {e}"

    # Append bot message
    st.session_state.messages.append({"role": "bot", "text": bot_response})

# --- Render all messages from history ---
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "bot"
    sender = "You" if msg["role"] == "user" else "Chatbot"
    st.markdown(f"""
        <div class='chat-message {role_class}'>
            <strong>{sender}:</strong><br>{msg['text']}
        </div>
    """, unsafe_allow_html=True)
