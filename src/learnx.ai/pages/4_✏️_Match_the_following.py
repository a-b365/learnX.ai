# Standard library imports
import string
import random
from time import time_ns

# Third party imports
import requests
import streamlit as st
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize

st.markdown("<h3 style='text-align: center;'>✏️ Match the Following Generator</h3>", unsafe_allow_html=True)

st.divider()

input_text = st.text_area(
    label="## **Input Context**", 
    placeholder="Paste your text here...", 
    height=300,
    value="Kalki, final avatar (incarnation) of the Hindu god Vishnu, who is yet to appear. At the end of the present Kali yuga (age), when virtue and dharma have disappeared and the world is ruled by the unjust, Kalki will appear to destroy the wicked and to usher in a new age. He will be seated on a white horse with a naked sword in his hand, blazing like a comet. He is less commonly represented in painting and sculpture than the other avatars of Vishnu and is shown either on horseback or accompanied by his horse. According to some legends of the end of the world, Kalki’s horse will stamp the earth with its right foot, causing the tortoise which supports the world to drop into the deep. Then the gods will restore the earth once again to its former purity."
)

button = st.button("✨ Generate", use_container_width=True)

if 'keywords' not in st.session_state:
    st.session_state.keywords = []

if 'definitions' not in st.session_state:
    st.session_state.definitions = []

if button:

    if not input_text.strip():
        st.error("Please provide input text before generating.")

    else:
        url = "http://127.0.0.1:8000/matches"

        response = requests.post(url, params={"q": str(input_text)})
        
        if response.status_code == 200:
            data = response.json()
            keywords = data.get("keywords")
            word_tokens = word_tokenize(input_text)

            try:
                for keyword in keywords:
                    if keyword not in st.session_state.keywords:
                        definition = lesk(word_tokens, keyword)
                        if definition:
                            st.session_state.definitions.append(definition.definition())
                            st.session_state.keywords.append(keyword)

            except AttributeError:
                pass

        else:
            st.error(f"Status code: {response.status_code}")
            st.write(f"Error: {response.content}")

if st.session_state.definitions:
    
    sample = random.sample(st.session_state.keywords, len(st.session_state.keywords))

    st.success("See the results below!")
    with st.container():
        for i in range(len(sample)):
            col1, col2 = st.columns(2)
            col1.write(f"🔑 {sample[i]}")
            col2.write(f"📖 {st.session_state.definitions[i]}")
