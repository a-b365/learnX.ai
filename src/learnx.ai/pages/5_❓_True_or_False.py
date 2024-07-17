#Standard library imports
import random

#Third party imports
import requests
import streamlit as st
import nltk

st.write("# :question: True or False Generator\n\n")
st.divider()
input_text = st.text_area(label="# ***Input Context***", placeholder="Paste here...", height=300)
button_four = st.button("***Generate***", use_container_width=True)

if button_four:

    url = "http://127.0.0.1:8000/tf"
    response = requests.post(url, params={"q":str(input_text)})
    if response.status_code == 200:
        st.write("Hello")
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")