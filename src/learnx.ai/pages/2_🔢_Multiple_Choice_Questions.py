#Standard library imports
import random

#Third party imports
import requests
import streamlit as st
import nltk

st.write("# :1234: MCQ Generator\n\n")
st.divider()
input_text = st.text_area(label="# ***Input Context***", placeholder="Paste here...", height=300)
with st.container(border=True):
    radio_one = st.radio(label = "Choose one option", options = ["***Word2Vec***","***Sense2Vec***"], horizontal=True)
button_one = st.button("***Generate***", use_container_width=True)

if button_one:

    url = "http://127.0.0.1:8000/mcqs"
    response = requests.post(url, params={"q":str(input_text),"radio":str(radio_one.strip("***"))})
    if response.status_code == 200:
        question = response.json().get("question")
        answer = response.json().get("answer")
        distractors = response.json().get("distractors")[:3]

        if distractors:
            meaning = response.json().get("meaning")
            options = random.sample([answer.capitalize()]+distractors,len(distractors)+1)
        else:
            options = ["N/A"] * 4

        expander = st.expander(label="**Prediction**")
        expander.write(question)
        expander.divider()

        for i in range(len(options)):
            expander.checkbox(label = options[i], key=i)
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")