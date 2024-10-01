# Standard library imports
import random

# Third party imports
import requests
import streamlit as st
import nltk

st.markdown("<h3 style='text-align: center;'>✅ Fill in the Blanks Generator</h3>", unsafe_allow_html=True)

st.divider()

input_text = st.text_area(
    label="## **Input Context**", 
    placeholder="Paste your text here...", 
    height=300,
    value="Kalki, final avatar (incarnation) of the Hindu god Vishnu, who is yet to appear. At the end of the present Kali yuga (age), when virtue and dharma have disappeared and the world is ruled by the unjust, Kalki will appear to destroy the wicked and to usher in a new age. He will be seated on a white horse with a naked sword in his hand, blazing like a comet. He is less commonly represented in painting and sculpture than the other avatars of Vishnu and is shown either on horseback or accompanied by his horse. According to some legends of the end of the world, Kalki’s horse will stamp the earth with its right foot, causing the tortoise which supports the world to drop into the deep. Then the gods will restore the earth once again to its former purity."
)

button = st.button("✨ Generate", use_container_width=True)

if 'question' not in st.session_state:
    st.session_state.question = None

if 'answers' not in st.session_state:
    st.session_state.answers = []

if button:

    if not input_text.strip():
        st.error("Please provide input text before generating.")
        
    else:
        url = "http://127.0.0.1:8000/blanks"
        response = requests.post(url, params={"q": str(input_text)})

        if response.status_code == 200:
            data = response.json()
            st.session_state.answers = data.get("answers")
            st.session_state.question = data.get("question")

        else:
            st.error(f"Failed to generate blanks. Status code: {response.status_code}")
            st.write(f"Error: {response.content}")

if st.session_state.question and st.session_state.answers:

    with st.container():
        st.success("See the results below!")
        st.divider()
        st.write("📝 Fill in the blanks with the correct word(s) from the list")
        st.write(f"🔑 [{', '.join(st.session_state.answers)}]")
        st.write(st.session_state.question)
            
