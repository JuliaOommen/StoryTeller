import streamlit as st
from gtts import gTTS
import os
import tempfile
from langchain_groq import ChatGroq
from utils import load_css   

# Apply CSS
load_css("style.css")

# Page setup
st.title("🌍 Language Fun")
st.write("Translate English sentences into different languages and listen to them!")

# Back button
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

# Language options
languages = {
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml"
}

choice = st.selectbox("Choose a language", list(languages.keys()))
target_lang = languages[choice]

# User input
text = st.text_area("Enter English text to translate:")

if st.button("Translate & Speak"):
    if text.strip() != "":
        # Call Groq model to translate
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=300
        )

        prompt = f"Translate the following English text into {choice}: {text}"
        resp = llm.invoke(prompt)
        translation = resp.content

        st.success(f"**{choice} Translation:**\n\n{translation}")

        # Generate speech
        try:
            tts = gTTS(translation, lang=target_lang)
            with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
                tts.save(tmp_file.name + ".mp3")
                st.audio(tmp_file.name + ".mp3", format="audio/mp3")
        except Exception as e:
            st.error(f"Could not generate audio for {choice}. Error: {e}")
    else:
        st.warning("Please enter some English text first.")
