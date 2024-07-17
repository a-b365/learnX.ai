#Standard library imports
import string
from typing import Union

#Third party imports
from rake_nltk import Rake
from fastapi import FastAPI

#Local application imports
from Mcq import get_distractors, get_sense, get_question

app = FastAPI()

@app.get("/")
def read_root():
    pass

@app.post("/mcqs")
def get_mcqs(q:str):
    sense, meaning, answer = get_sense(q)
    if sense is not None:
        distractors = get_distractors(sense, answer)
    else:
        distractors = ["Word not found in Wordnet"]
    sentence_for_t5 = q.replace("[TGT]"," ")
    sentence_for_t5 = " ".join(sentence_for_t5.split())
    question = get_question(sentence_for_t5, answer)
    return {"question":question, 
            "answer":answer, 
            "distractors": distractors, 
            "meaning": meaning
            }
    

@app.post("/blanks")
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

    return {"filtered_keywords": list(filtered_keywords)}

@app.post("/matches")
def generate_matches(q:str):
    """
    The function creates match the following kind of questions
    
    """
    #Keyword extraction using rake-nltk
    rake_nltk = Rake(max_length = 1, 
                include_repeated_phrases = False,
                punctuations = string.punctuation)

    rake_nltk.extract_keywords_from_text(q)
    keywords = rake_nltk.get_ranked_phrases()[:10]
    
    return {"keywords": list(keywords)}

    


    