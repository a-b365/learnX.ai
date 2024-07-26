#Standard library imports
import random

#Third party imports
import requests
import streamlit as st

value = """Kalki, final avatar (incarnation) of the Hindu god Vishnu, who is yet to appear."""

st.write("# :question: True or False Generator\n\n")
st.divider()
input_text = st.text_area(label="# ***Input Context***", value=value, placeholder="Paste here...", height=300)
button_four = st.button("***Generate***", use_container_width=True)

if button_four:

    url = "http://127.0.0.1:8000/true_false"
    response = requests.post(url, params={"q":str(input_text)})
    if response.status_code == 200:
        questions = response.json().get("questions")
        expander = st.expander(label="Prediction")
        for i,j in enumerate(random.sample(questions, 5)):
            st.write(j)
            st.button(label="True",key=i)
            st.button(label="False",key=5+i)
            st.divider()                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")