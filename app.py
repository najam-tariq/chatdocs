import streamlit as st
import g4f
import PyPDF2
import io
from stqdm import stqdm
import requests

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
file = st.file_uploader('Upload', type=['pdf']) # can be pdf or word file
if file is not None:
    def gpt2text(query):
        with st.spinner(text="Processing Text..."):
            parsed_text = extract_text_from_pdf(file)
            words = parsed_text.split()
            contexts = [words[i:i+1000] for i in range(0, len(words), 1000)]
            st.info(f'Processed {len(words)} Words', icon="ℹ️")
            
        with st.spinner(text="Analyzing Query..."):
            url = "https://gptleg.zeabur.app/api/openai/v1/chat/completions"
            headers =  {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
            messages = [
                {"role": "user", "content": f'Process the info below: {context}'}
                for context in contexts
            ]
            
            messages.append({"role": "user", "content": f'Now, answer the following question if the answer is contained in the above info else reply I do not know: {query}'})
            messages.append({"role": "user", "content": f'Also, if the answer is contained; add references (quote text) from text (under a heading) after answering the query.'})
            data = {
                "messages": messages,
                "stream": False,
                "model": "gpt-4-0613",
                "temperature": 0.5,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "top_p": 1
            }

        with st.spinner(text="Processing Query..."):
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                response = response.json()
                return response['choices'][0]['message']['content']
            else:
                return None

    query = st.text_input(
        label="Enter Query:", 
        placeholder="Write a summary...",
        )

    run_button = st.button("Run")
    if run_button:
        response = gpt2text(query=query)
        if len(response) < 5:
            st.warning('Error Occurred', icon="⚠️")
        else:
            st.text_area("Response: ", response, height=200)