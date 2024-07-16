import streamlit as st
import pandas as pd
import numpy as np
import requests

st.write("Fill in the blanks questions \n\n")
input_text = st.text_area(label="Give input context...")
button = st.button("Generate")

if button:

    url = "http://127.0.0.1:8000/predict"
    response = requests.post(url, params={"q":str(input_text)})
    if response.status_code == 200:
        keywords = response.json().get("keywords")
        st.write(f"Prediction: {keywords}")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")