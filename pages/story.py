import os, io
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from gtts import gTTS
from utils import load_css  

# Apply CSS
load_css("style.css")

load_dotenv()
st.title("📖 Story Time")
st.page_link("app.py", label="🏠 Back to Home", icon="↩️")

# --- Sidebar: full tuning ---
st.sidebar.header("Model & Parameters")
MODEL_OPTIONS = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
model_name = st.sidebar.selectbox("Model", MODEL_OPTIONS, index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
top_p = st.sidebar.slider("Top-p (nucleus)", 0.05, 1.0, 0.9, 0.05)
max_tokens = st.sidebar.slider("Max tokens", 50, 800, 300, 10)
presence_penalty = st.sidebar.slider("Presence penalty", -1.0, 1.0, 0.0, 0.1)
frequency_penalty = st.sidebar.slider("Frequency penalty", -1.0, 1.0, 0.0, 0.1)

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY missing. Put it in your .env and restart.")
    st.stop()

def build_llm():
    return ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        model_kwargs={
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
        },
    )

topic = st.text_input("What should the story be about?")
tone = st.selectbox("Tone", ["Playful", "Gentle", "Adventurous", "Magical", "Funny"], index=0)
length = st.slider("Approx. length (words)", 80, 600, 250, 10)

if "story_text" not in st.session_state:
    st.session_state.story_text = ""

colA, colB = st.columns(2)
with colA:
    if st.button("✨ Generate Story"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            llm = build_llm()
            prompt = (
                "You are a kid-safe writer. Simple words, short sentences, kind tone.\n"
                f"Write a {tone.lower()} story for children about: {topic}\n"
                f"Target length: ~{length} words. Avoid scary/violent content."
            )
            resp = llm.invoke(prompt)
            st.session_state.story_text = getattr(resp, "content", str(resp))

with colB:
    if st.button("🔄 Clear"):
        st.session_state.story_text = ""

if st.session_state.story_text:
    st.subheader("Your Story")
    st.write(st.session_state.story_text)

    # Play audio on demand (in-memory)
    if st.button("🔊 Play Story"):
        tts = gTTS(st.session_state.story_text, lang="en")
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        st.audio(buf.getvalue(), format="audio/mp3")

st.page_link("app.py", label="🏠 Back to Home", icon="↩️")
