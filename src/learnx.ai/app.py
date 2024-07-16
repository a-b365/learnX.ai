import random
import string
from typing import Union

import nltk
from nltk.wsd import lesk
from nltk.corpus import stopwords, wordnet as wn
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake, Metric
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str,None] = None):
    return {"item_id": item_id,"q":q}

@app.post("/predict")
def generate_blanks(q:str):
    """
    The function creates fill in the blanks questions
    
    """
    rake_nltk = Rake(max_length=3, include_repeated_phrases=False)
    rake_nltk.extract_keywords_from_text(q)
    keywords = rake_nltk.get_ranked_phrases()
    filtered_keywords = set()

    #punctuation removal from the text
    for i in keywords:
        i = i.translate(str.maketrans("","",string.punctuation)).strip()
        filtered_keywords.add(i)

    return {"keywords": list(filtered_keywords)}

    


    