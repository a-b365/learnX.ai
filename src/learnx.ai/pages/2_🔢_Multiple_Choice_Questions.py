#Standard library imports
import random
from time import time_ns

#Third party imports
import requests
import streamlit as st

st.markdown("<h3 style='text-align: center;'>🔢 MCQ Generator</h3>", unsafe_allow_html=True)
st.divider()

input_text = st.text_area(
    label="## **Input Context**", 
    placeholder="Paste your text here...", 
    height=300,
    value = "World War II (1939-1945) was a global conflict that involved most of the world's nations, including the major powers divided into two alliances: the Allies (led by the United States, the Soviet Union, and the United Kingdom) and the Axis (primarily Nazi Germany, Imperial Japan, and Italy). Sparked by the invasion of Poland by Germany under Adolf Hitler, the war saw immense battles across Europe, Africa, and Asia. It led to the Holocaust, the devastation of cities, and the use of nuclear weapons on Japan by the U.S. The conflict ended with the unconditional surrender of the Axis powers, fundamentally reshaping global politics and establishing the United Nations to promote peace."
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

        for i in range(len(questions)):

            if distractors[i]:
                options = random.sample(distractors[i] + [answers[i]], len(distractors[i])+1)
                expander = st.expander(label="Prediction")
                expander.write(questions[i].strip("question: "))
                expander.divider()

                for j in range(len(options)):
                    expander.checkbox(label = options[j], key = str(i) + str(j))
            else:
                pass
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")