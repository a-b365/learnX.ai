#Standard library imports
import random

#Third party imports
import requests
import streamlit as st
import nltk

st.write("# :1234: MCQ Generator\n\n")
st.divider()
input_text = st.text_area(label="# ***Input Context***", placeholder="Paste here...", height=300)
button_one = st.button("***Generate***", use_container_width=True)

if button_one:

    url = "http://127.0.0.1:8000/mcqs"
    response = requests.post(url, params={"q":str(input_text)})
    if response.status_code == 200:
        question = response.json().get("question")
        answer = response.json().get("answer")
        distractors = response.json().get("distractors")[:3]
        meaning = response.json().get("meaning")
        options = random.sample([answer.capitalize()]+distractors,4)
        
        expander = st.expander(label="**Prediction**")
        expander.write(question)
        expander.divider()
        expander.checkbox(label = options[0])
        expander.checkbox(label = options[1])
        expander.checkbox(label = options[2])
        expander.checkbox(label = options[3])
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")