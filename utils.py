import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from gtts import gTTS

# Load API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Shared model instance
def get_model(temperature=0.7, max_tokens=200, top_p=1.0, top_k=50, frequency_penalty=0.0, presence_penalty=0.0):
    return ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        top_k=top_k,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

def generate_text(prompt, temperature=0.7, max_tokens=200, top_p=1.0, top_k=50, frequency_penalty=0.0, presence_penalty=0.0):
    llm = get_model(temperature, max_tokens, top_p, top_k, frequency_penalty, presence_penalty)
    response = llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)

# Text-to-Speech function
def text_to_audio(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# CSS loader
def load_css(file_name: str):
    """Load CSS file into Streamlit app"""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
