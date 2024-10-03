#Standard library imports
import os

#Third party imports
import torch
import spacy
from sense2vec import Sense2Vec
from transformers import pipeline
from transformers import AutoTokenizer, T5ForConditionalGeneration


os.environ["MODEL_PATH"] = "D:\\learnx.ai\\models\\qa-t5b.pth"
os.environ["PRETRAINED_VECTOR_DIR"] = "D:\\learnx.ai\\s2v_reddit_2015_md\\s2v_old"

nlp = spacy.load("en_core_web_sm")
# s2v = nlp.add_pipe("sense2vec")
s2v = Sense2Vec().from_disk(os.environ["PRETRAINED_VECTOR_DIR"])

def get_distractors(answer):
    
    distractors = []
    temp = []

    try:
        doc = nlp(answer)
        entities = []
        current_entity = []

        for i in doc:
            if  i.pos_ == 'PROPN':
                current_entity.append(i.text)
            else:
                if current_entity:
                    entities.append(" ".join(current_entity))
                    current_entity = []
        
        if current_entity:
            entities.append(" ".join(current_entity))

        for i in entities:

            try:
                print(i)
                sense = s2v.get_best_sense(i.replace(" ", "_"))
                most_similar = s2v.most_similar(sense, n=3)
                most_similar = list(tuple(zip(*list(most_similar)))[0])
                temp.append([item.split("|")[0].replace("_", " ") for item in most_similar])

            except TypeError:
                pass

        for j in list(zip(*temp)):
            distractor = answer
            for k in range(len(j)):
                distractor = distractor.replace(entities[k], j[k])
            distractors.append(distractor)
        
    except ValueError:
        pass

    return distractors

def generate_answer(question, context):
  qa_model = pipeline("question-answering")
  result = qa_model(question = question.strip("question: "), context = context.strip("context: "))
  return result["answer"]

def get_qa(text):
    
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    model.load_state_dict(torch.load(os.environ["MODEL_PATH"]))
    outputs = tokenizer("context: " + text, return_tensors="pt")
    preds = model.generate(input_ids = outputs["input_ids"], 
                       attention_mask = outputs["attention_mask"],
                       max_new_tokens=72,
                       do_sample=True,
                       top_k=20,
                       num_return_sequences=5
                    )
    questions = tokenizer.batch_decode(preds, skip_special_tokens=True)
    answers = [generate_answer(i, text) for i in questions]
    return questions, answers