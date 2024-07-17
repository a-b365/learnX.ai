#Standard library imports
import random

#Third party imports
import requests
import streamlit as st
import nltk

st.write("# :white_check_mark: Fill in the Blanks Generator\n\n")
st.divider()
input_text = st.text_area(label="# ***Input Context***", placeholder="Paste here...", height=300)
button_two = st.button("***Generate***", use_container_width=True)

if button_two:

    url = "http://127.0.0.1:8000/blanks"
    response = requests.post(url, params={"q":str(input_text)})
    if response.status_code == 200:
        filtered_keywords = response.json().get("filtered_keywords")
        sample = random.sample(filtered_keywords, 5)
        cased_keywords = ([(i.upper(), i.lower(), i.capitalize(), i.title()) for i in sample])
        temp = input_text

        for i,j,k,l in cased_keywords:
            temp = temp.replace(i,"[MASK]").replace(j,"[MASK]").replace(k,"[MASK]").replace(l,"[MASK]")

        with st.container(border=True):
            for i in nltk.sent_tokenize(temp):
                if "[MASK]" in i:
                    st.write(i)
                
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")