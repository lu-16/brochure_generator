# File: /brochure_generator/brochure_generator/app.py
"A Streamlit application to generate a markdown brochure for an apartment complex."
from dotenv import load_dotenv
import streamlit as st
from llm_brochure_generator import generate_brochure_with_llm, stream_brochure

load_dotenv()

st.set_page_config(
    page_title="Apartment Brochure Generator",
    page_icon="🏢",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Apartment Brochure Generator")
url = st.text_input("Enter apartment website URL")

placeholder = st.empty()
text = ""

if url:
    markdown = generate_brochure_with_llm(url)
    st.markdown(markdown)
