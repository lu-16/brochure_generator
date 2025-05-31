"A Streamlit application to generate a markdown brochure for an apartment complex."
from dotenv import load_dotenv
import streamlit as st
from brochure import generate_brochure

load_dotenv()

st.set_page_config(
    page_title="Apartment Brochure Generator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("Apartment Brochure Generator")
url = st.text_input("Enter apartment website URL")

if url:
    markdown = generate_brochure(url)
    st.markdown(markdown)
