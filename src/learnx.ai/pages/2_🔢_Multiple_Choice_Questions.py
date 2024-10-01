#Standard library imports
import random

#Third party imports
import requests
import streamlit as st
import nltk

st.markdown("<h3 style='text-align: center;'>🔢 MCQ Generator</h3>", unsafe_allow_html=True)
st.divider()

input_text = st.text_area(
    label="## **Input Context**", 
    placeholder="Paste your text here...", 
    height=300
)

button = st.button("✨ Generate", use_container_width=True)

if "quizzes" not in st.session_state:
    st.session_state.quizzes = []

if "choices" not in st.session_state:
    st.session_state.choices = []
    
if button:

    url = "http://127.0.0.1:8000/mcqs"
    response = requests.post(url, params={"q":str(input_text)})

    if response.status_code == 200:
        data = response.json()
        questions = data.get("questions")
        answers = data.get("answers")
        distractors = data.get("distractors")
        print(questions)
        print(answers)

        for i in range(len(questions)):

            if distractors[i]:
                options = random.sample([i.capitalize() for i in distractors[i]]+[answers[i]], len(distractors[i])+1)[:4]
                expander = st.expander(label="Prediction")
                expander.write(questions[i].strip("question: "))
                expander.divider()

                for i in range(len(options)):
                    expander.checkbox(label = options[i], key=options[i])
            else:
                pass
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")