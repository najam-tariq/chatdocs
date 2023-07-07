import streamlit as st
import g4f
import PyPDF2
import random
import io
from stqdm import stqdm

# --- Hiding Header and Footer
st.set_page_config(page_title="Chat Docs")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
# --- Hiding Header and Footer

def extract_text_from_pdf(file_path):
    with io.BytesIO(file.read()) as file_obj:
        reader = PyPDF2.PdfReader(file_obj)
        num_pages = len(reader.pages)
        text = ''
        for page in stqdm(range(num_pages)):
            page_obj = reader.pages[page]
            text += page_obj.extract_text()
    return text

st.title("Chat Docs")
file = st.file_uploader('Upload') # can be pdf or word file
if file is not None:
    def gpt2text(text):
        parsed_text = extract_text_from_pdf(file)
        res = g4f.ChatCompletion.create(
                model= g4f.Model.gpt_35_turbo, 
                messages=[
                    {"role": "user", "content": f'Answer the question using the info below: {parsed_text}'},
                    {"role": "user", "content": f'{text}'},
                ],
                provider=random.choice([
                    g4f.Provider.GravityEngine
                ]))
        return res
        

    text = st.text_input(
        label="Enter Text:", 
        placeholder="Write a summary...",
        )

    run_button = st.button("Run")
    if run_button:
        with st.spinner(text="Please Wait..."):
            response = gpt2text(text=text)
            if len(response) < 5:
                st.warning('Error Occurred', icon="⚠️")
            else:
                st.text_area("Response: ", response, height=200)