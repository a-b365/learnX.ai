#Standard library imports
import string
import random

#Third party imports
import requests
import streamlit as st
from nltk.wsd import lesk
from nltk.corpus import stopwords, wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

st.write("# :pencil2: Match the Following Generator \n\n")
st.divider()
input_text = st.text_area(label="# ***Input Context***", placeholder="Paste here...", height=300)
button_three = st.button("***Generate***" , use_container_width=True)

if button_three:

    wn_keywords = []
    wn_definitions = []

    url = "http://127.0.0.1:8000/matches"
    response = requests.post(url, params={"q":str(input_text)})

    if response.status_code == 200:
        keywords = response.json().get("keywords")

        #punctuation and stopwords removal from the text followed by lemmatization
        stop_words = set(stopwords.words("english"))
        text_no_punc = input_text.translate(str.maketrans("","",string.punctuation))
        word_tokens = word_tokenize(text_no_punc.lower())
        #filtered_sentence = [w for w in word_tokens if not w in stop_words]
        lemmatizer = WordNetLemmatizer()
        lemmatized_sentence = [lemmatizer.lemmatize(w) for w in word_tokens]
        
        try:
            for i in keywords:
                wn_keywords.append(i)
                wn_definitions.append(lesk(lemmatized_sentence, i).definition())
        except AttributeError:
            pass

        #Sampling withput replacement and Generate the output
        sample = random.sample(wn_keywords, len(wn_keywords)-1)
        try:
            with st.container(border=True):
                for i in range(len(sample)):
                    #print("{:100}{:10}".format(sample[i], wn_definitions[i]))
                    s1, s2 = st.columns(2)
                    s1.write(sample[i])
                    s2.write(wn_definitions[i])
        except AttributeError:
            pass

    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Response content: {response.content}")