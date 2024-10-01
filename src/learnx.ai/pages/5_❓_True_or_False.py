import random
import requests
import streamlit as st

value = """Kalki, final avatar (incarnation) of the Hindu god Vishnu, who is yet to appear."""

st.markdown("<h3 style='text-align: center;'>❓ True or False Generator</h3>", unsafe_allow_html=True)

st.divider()

input_text = st.text_area(
    label="## **Input Context**", 
    placeholder="Paste your text here...",
    value=value, 
    height=300
)

button = st.button("✨ Generate", use_container_width=True)

if 'questions' not in st.session_state:
    st.session_state.questions = []

if 'answers' not in st.session_state:
    st.session_state.options = {}

if button:
    url = "http://127.0.0.1:8000/true_false"
    response = requests.post(url, params={"q": str(input_text)})
    
    if response.status_code == 200:
        questions = response.json().get("questions")
        st.session_state.questions = random.sample(questions, min(5, len(questions)))
        st.session_state.options = {}

    else:
        st.write(f"Request failed with status code {response.status_code}")
        st.write(f"Response content: {response.content}")

if st.session_state.questions:
    expander = st.expander(label="See the results below!")

    with expander:
        for i, question in enumerate(st.session_state.questions):
            st.write(f"📝 Q{i+1}. {question}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(label="True", key=f"true_{i}"):
                    st.session_state.options[i] = "True"
            with col2:
                if st.button(label="False", key=f"false_{i}"):
                    st.session_state.options[i] = "False"

            if i in st.session_state.options:
                st.write(f"Your answer: {st.session_state.options[i]}")
            else:
                st.write("You haven't answered this question yet.")

            st.divider()