#Standard library imports
import random

#Third party imports
import requests
import streamlit as st
import nltk

st.markdown("<h3 style='text-align: center;'>📚 Flash Cards Generator</h3>", unsafe_allow_html=True)
st.divider()

input_text = st.text_area(
    label="## **Input Context**", 
    placeholder="Paste your text here...", 
    height=300,
    value="context: World War II (1939-1945) was a global conflict that involved most of the world's nations, including the major powers divided into two alliances: the Allies (led by the United States, the Soviet Union, and the United Kingdom) and the Axis (primarily Nazi Germany, Imperial Japan, and Italy). Sparked by the invasion of Poland by Germany under Adolf Hitler, the war saw immense battles across Europe, Africa, and Asia. It led to the Holocaust, the devastation of cities, and the use of nuclear weapons on Japan by the U.S. The conflict ended with the unconditional surrender of the Axis powers, fundamentally reshaping global politics and establishing the United Nations to promote peace."
)

button = st.button("✨ Generate", use_container_width=True)
    
if button:

    url = "http://127.0.0.1:8000/flashcards"
    response = requests.post(url, params={"q":str(input_text)})

    if response.status_code == 200:
        data = response.json()
        questions = data.get("questions")
        answers = data.get("answers")

        for i in range(len(questions)):

            expander = st.expander(label=f"Flash Card {i}")
            expander.write(questions[i].strip("question: "))
            expander.divider()
            expander.write(answers[i])
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")