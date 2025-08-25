import streamlit as st
from gtts import gTTS
import tempfile
import os
from langchain_groq import ChatGroq

# Page config
st.set_page_config(page_title="Adventure Game", page_icon="🗺️", layout="wide")

# Page title
st.title("🗺️ Adventure Time")

# Back to home button
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

# Initialize session state
if "adventure_story" not in st.session_state:
    st.session_state.adventure_story = []
if "adventure_choices" not in st.session_state:
    st.session_state.adventure_choices = []
if "adventure_step" not in st.session_state:
    st.session_state.adventure_step = 0
if "last_options" not in st.session_state:
    st.session_state.last_options = []

# Step 0 → Start game
if st.session_state.adventure_step == 0:
    theme = st.text_input("Pick a theme to begin (e.g., 'hidden island', 'space zoo'):")
    if st.button("🚀 Start Adventure") and theme.strip():
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192",
            temperature=0.8,
            max_tokens=400,
        )
        prompt = (
            f"You are telling a fun adventure story for children.\n"
            f"Start the first part of an adventure about: {theme}.\n"
            f"End with 3 short simple choices (label them clearly as 1, 2, 3)."
        )
        resp = llm.invoke(prompt)

        # Save story and extract choices
        st.session_state.adventure_story.append(resp.content)
        st.session_state.adventure_step = 1

        # Extract options (simple heuristic)
        options = []
        for line in resp.content.split("\n"):
            if line.strip().startswith(("1", "2", "3")):
                options.append(line.strip())
        st.session_state.last_options = options or ["Option 1", "Option 2", "Option 3"]

        st.rerun()

# Steps > 0 → Continue game
if st.session_state.adventure_step > 0:
    st.subheader("📖 Your Adventure")

    # Show past story
    for i, part in enumerate(st.session_state.adventure_story, start=1):
        st.markdown(f"**Part {i}:**\n\n{part}")

    # Read latest part aloud
    latest_part = st.session_state.adventure_story[-1]
    tts = gTTS(latest_part, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        st.audio(tmp_file.name, format="audio/mp3")

    # Show available options
    choice = st.radio(
        "What do you choose?",
        st.session_state.last_options,
        index=None,
        key=f"choice_{st.session_state.adventure_step}"
    )

    if choice and st.button("➡️ Continue Adventure"):
        st.session_state.adventure_choices.append(choice)

        # Build context
        history = "\n".join(
            f"Part {i+1}: {p}" for i, p in enumerate(st.session_state.adventure_story)
        )
        decisions = ", ".join(st.session_state.adventure_choices)

        # Ask LLM for continuation
        llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-8b-8192",
            temperature=0.8,
            max_tokens=400,
        )
        prompt = (
            f"You are telling a fun branching adventure for kids.\n\n"
            f"Story so far:\n{history}\n\n"
            f"The hero’s past choices: {decisions}\n\n"
            f"Now continue the story with the next exciting part. "
            f"End again with 3 short simple options (label them 1, 2, 3)."
        )
        resp = llm.invoke(prompt)

        # Save new part
        st.session_state.adventure_story.append(resp.content)
        st.session_state.adventure_step += 1

        # Extract new options
        options = []
        for line in resp.content.split("\n"):
            if line.strip().startswith(("1", "2", "3")):
                options.append(line.strip())
        st.session_state.last_options = options or ["Option 1", "Option 2", "Option 3"]

        st.rerun()
