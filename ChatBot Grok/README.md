![image](https://github.com/user-attachments/assets/124013a1-2f68-4a01-ab86-55e5f0860ce5)

# Streamlit-based Chatbot Application

This is a simple chatbot application built using Streamlit and the Grok API. The application allows users to interact with the chatbot and get responses in real-time.

## Features
- User-friendly chat interface built with Streamlit.
- Real-time responses powered by the Grok API.
- Easy setup and integration with Grok API.

## Requirements

- Python 3.x
- Streamlit
- dotenv
- Requests

## Setup Instructions

### Step 1: Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/manitejagaddam/LLM-Projects/tree/Machine-Learning/ChatBot%20Grok.git
```

### Step 2: Install Required Packages

Navigate to the project directory and install the required dependencies:

```bash
cd chatbot-streamlit
uv add -r requirements.txt
```

### Step 3: Create .env File
To run the application, you'll need to create a .env file in the project root directory and add your Grok API key there. Follow these steps:

- In the project directory, create a .env file.

- Add the following line to the .env file:


```bash
GROK_API_KEY=your_grok_api_key_here
```
- Replace your_grok_api_key_here with your actual API key.


### Step 4: Run the Application
Once you've set up the .env file, you can run the Streamlit application:


```bash
streamlit run chatbot.py
```

- This will start the chatbot application, and you can access it in your browser at http://localhost:8501.