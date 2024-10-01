#Standard library imports
import os

#Third party imports
import torch
import spacy
from transformers import pipeline
from transformers import AutoTokenizer, T5ForConditionalGeneration


os.environ["MODEL_PATH"] = "D:\\learnx.ai\\models\\qa-t5b.pth"
os.environ["PRETRAINED_VECTOR_DIR"] = "D:\\learnx.ai\\s2v_reddit_2015_md\\s2v_old"

nlp = spacy.load("en_core_web_sm")
s2v = nlp.add_pipe("sense2vec")
s2v.from_disk(os.environ["PRETRAINED_VECTOR_DIR"])

def get_distractors(word):
    
    distractors = []
    try:
        doc = nlp("_".join(word.lower().split(" ")))
        most_similar = doc[:]._.s2v_most_similar()
        most_similar = list(tuple(zip(*list(zip(*most_similar))[0]))[0])
        for i in most_similar:
            if i not in [word.lower(), word.capitalize(), word.upper()] + distractors:
                distractors.append(i)
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
    outputs = tokenizer(text, return_tensors="pt")
    preds = model.generate(input_ids = outputs["input_ids"], 
                       attention_mask = outputs["attention_mask"],
                       do_sample=False,
                       num_beams=5, num_beam_groups=5, 
                       max_new_tokens=50, 
                       diversity_penalty=1.0, 
                       num_return_sequences=5
                    )
    questions = tokenizer.batch_decode(preds, skip_special_tokens=True)
    answers = [generate_answer(i, text) for i in questions]
    return questions, answers