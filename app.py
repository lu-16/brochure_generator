"A Streamlit application to generate a markdown brochure for an apartment complex."
import streamlit as st
from brochure import generate_brochure

st.set_page_config(
    page_title="Apartment Brochure Generator",
    page_icon=":cityscape:",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title(":cityscape: Apartment Brochure Generator")
url = st.text_input("Enter apartment website URL")

# if url:
#     with st.spinner("Generating brochure..."):
#         markdown = generate_brochure(url)
#         st.markdown(markdown)

if url:
    spinner_placeholder = st.empty()
    spinner_placeholder.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px;">
            <div style="font-size: 60px; animation: spin 1s linear infinite;">🏵️</div>
            <h3 style="text-align:center;">Creating your apartment brochure... Please wait!</h3>
        </div>
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg);}
            100% { transform: rotate(360deg);}
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    markdown = generate_brochure(url)
    spinner_placeholder.empty()
    st.markdown(markdown)
