import os 
import google
import google.generativeai as genai
import gradio as gr 
from  dotenv import load_dotenv

# Load environment variables 
load_dotenv()
google_api_key = os.getenv("GEMINI_API_KEY")

# Debugging API Key presence
if google_api_key:
    print(f"Gemini API Key exists and begins {google_api_key[:8]}")
else:
    print("Gemini API Key not set")

# Configure Google Generative AI 
google.generativeai.configure(api_key=google_api_key)

# Inatialize Gemini Model
MODEL = "gemini-1.5-flash"
gemini = genai.GenerativeModel(MODEL)

# Sytem mesage
sytem_message = "you are a profesional assistant"

# Chat function 
def chat(message,history):
    # convert history into gemini expected format 
    formatted_history = []

    for msg in history:

        #sort and format each message
        if msg["role"] == "user":
            formatted_history.append({"role": "user", "parts": [msg["content"]]})
        else:
            formatted_history.append({"role": "model", "parts": [msg["content"]]})

    # Append the current user message
    formatted_history.append({"role": "user", "parts": [message]})

    # print out the formatted
    print("History is:" , history)
    print("Formatted Messaged are:", formatted_history)

    # Generate response with streaming
    stream = gemini.generate_content(formatted_history, stream=True)

    response = ""
    for chunk in stream:
        content = chunk.text if chunk.text else ""
        response += content
        yield response  

# Launch graido
gr.ChatInterface(fn=chat, type="messages").launch()