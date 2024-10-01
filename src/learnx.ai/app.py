#Standard library imports
import string
from typing import Union

#Third party imports
from rake_nltk import Rake
from fastapi import FastAPI

#Local application imports
from Mcq import get_distractors, get_qa
from True_false import get_tree, get_flattened, get_rvp_nvp, get_termination_portion, get_true_false_questions, semantic_textual_similarity
from TokenClassification import post_processing, aggregate_entities

app = FastAPI()

@app.get("/")
def read_root():
    pass

@app.post("/mcqs")
def get_mcqs(q:str):
    questions, answers = get_qa(q)
    
    distractors = [get_distractors(i) for i in answers]

    return {"questions":questions, 
            "answers":answers, 
            "distractors": distractors, 
            }


@app.post("/blanks")
def generate_blanks(q:str):
    """
    The function creates fill in the blanks questions
    
    """
    answers = []
    question = q
    results = post_processing(q)
    print(results)
    entities = aggregate_entities(results)
    for i in entities:
        answer = q[i[0][0]:i[-1][-1]]
        answers.append(answer)
        print(answer)
        question = question.replace(answer,"____________")

    return {"answers":answers,"question":question}
    


@app.post("/matches")
def generate_matches(q:str):
    """
    The function creates match the following kind of questions
    
    """
    keywords = []
    results = post_processing(q)
    entities = aggregate_entities(results)
    for i in entities:
        keyword = q[i[0][0]:i[-1][-1]]
        keywords.append(keyword)
    return {"keywords": keywords}


@app.post("/true_false")
def generate_true_false(q:str):
    """
    The function creates true/false questions
    
    """
    tree = get_tree(q.strip("."))
    last_np, last_vp = get_rvp_nvp(tree)
    last_np_flattened = get_flattened(last_np)
    last_vp_flattened = get_flattened(last_vp)
    longest_phrase = max(last_np_flattened, last_vp_flattened)
    split_sentence = get_termination_portion(q.strip("."), longest_phrase)
    questions = get_true_false_questions(split_sentence)
    # answers = semantic_textual_similarity(list(questions), q)
    return {"questions": list(questions)}

@app.post("/flashcards")
def get_flashcards(q:str):
    questions, answers = get_qa(q)
    return {"questions":questions, 
            "answers":answers, 
            }
    


    