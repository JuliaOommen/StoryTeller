import streamlit as st
from utils import load_css

# Must be first
st.set_page_config(page_title="Story Teller", page_icon="✨", layout="wide")

# Apply CSS
load_css("style.css")

# Title
st.markdown("<h1 style='text-align: center;'>✨ Welcome to Story Teller! ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Choose a fun activity below 👇</h3>", unsafe_allow_html=True)

# Layout
col1, col2 = st.columns(2)

with col1:
    if st.button("📖 Story Time", use_container_width=True):
        st.switch_page("pages/story.py")

    if st.button("🗺️ Adventure Game", use_container_width=True):
        st.switch_page("pages/adventure.py")

with col2:
    if st.button("📝 Poem Maker", use_container_width=True):
        st.switch_page("pages/poem.py")

    if st.button("🔤 Language Fun", use_container_width=True):
        st.switch_page("pages/languagefun.py")
