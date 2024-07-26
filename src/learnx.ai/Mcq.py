#Standard library imports
import os
import re

#Third party imports
import spacy
from nltk.corpus import wordnet as wn
from pywsd.lesk import adapted_lesk
from transformers import AutoTokenizer, T5ForConditionalGeneration
from sense2vec import Sense2Vec

os.environ["BASE_DIR"] = "D:\\learnx.ai\\models\\t5_question_generation_model"
os.environ["PRETRAINED_VECTOR_DIR"] = "D:\\learnx.ai\\s2v_reddit_2015_md\\s2v_old"

nlp = spacy.load("en_core_web_sm")
s2v = nlp.add_pipe("sense2vec")
s2v.from_disk(os.environ["PRETRAINED_VECTOR_DIR"])
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained(os.environ["BASE_DIR"])

def get_distractors(syn, word, name):
    
    distractors = []

    if name == "Word2Vec":
        word = word.lower()
        orig_word = word
        if len(word.split()) > 0:
            word = word.replace(" ","_")
        hypernym = syn.hypernyms()
        if len(hypernym) == 0:
            return distractors
        for item in hypernym[0].hyponyms():
            name = item.lemma_names()[0]
            if name == orig_word:
                continue
            name = name.replace("_"," ")
            name = " ".join(w.capitalize() for w in name.split())
            if name is not None and name not in distractors:
                distractors.append(name)
    else:
        doc = nlp(word)
        most_similar = doc[:]._.s2v_most_similar()
        most_similar = list(tuple(zip(*list(zip(*most_similar))[0]))[0])
        
        for i in most_similar:
            if i not in [word.lower(), word.capitalize(), word.upper()] + distractors:
                distractors.append(i)

    return distractors

def get_sense(sent):
    re_result = re.search(r"\[TGT\](.*)\[TGT\]", sent)
    if re_result is None:
        print("Incorrect input format. Please try again.")
    sent = sent.replace("[TGT]"," ")
    sent = " ".join(i for i in sent.split())
    ambiguous_word = re_result.group(1).strip()
    wn_pos = wn.NOUN
    sense = adapted_lesk(sent, ambiguous_word, pos=wn_pos)
    meaning = sense.definition()
    return (sense, meaning, ambiguous_word)


def get_question(context, answer):
    text = "answer: {} context: {}".format(answer, context)
    tokens = tokenizer(text, return_tensors="pt")
    input_ids = tokens.input_ids
    attention_mask = tokens.attention_mask
    outputs = model.generate(input_ids = input_ids, attention_mask = attention_mask, max_length=200)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return question.replace("question:","").strip()