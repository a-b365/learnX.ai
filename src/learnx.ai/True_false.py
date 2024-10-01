#Standard library imports
import re

#Third party imports
import spacy
import benepar
import nltk
from nltk import tokenize
from nltk.tree import Tree
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from sentence_transformers import SentenceTransformer, util


nlp = spacy.load("en_core_web_md")
nlp.add_pipe("benepar", config={"model":"benepar_en3"})

GPT2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
GPT2_model = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=GPT2_tokenizer.eos_token_id)

def get_tree(full_text):
  doc = nlp(full_text)
  sent = list(doc.sents)[0]
  tree = Tree.fromstring(sent._.parse_string)
  return tree


def get_flattened(phrase_content):
  flattened_str = None
  if phrase_content is not None:
    pre_flattened_str = [" ".join(x.leaves()) for x in list(phrase_content)]
    flattened_str = [" ".join(pre_flattened_str)]
    flattened_str = flattened_str[0]
  return flattened_str


def get_rvp_nvp(parse_tree, last_np = None, last_vp = None):
  if len(parse_tree.leaves()) == 1:
    return last_np, last_vp
  last_subtree = parse_tree[-1]
  if last_subtree.label() == 'NP':
    last_np = last_subtree
  elif last_subtree.label() == "VP":
    last_vp = last_subtree
  return get_rvp_nvp(last_subtree, last_np, last_vp)


def get_termination_portion(main_string, sub_string):
  combined_sub_string = sub_string.replace(" ","")
  main_string_list = main_string.split()
  last_index = len(main_string_list)
  for i in range(last_index):
    check_string_list = main_string_list[i:]
    check_string = "".join(check_string_list)
    check_string = check_string.replace(" ","")
    if check_string == combined_sub_string:
      return " ".join(main_string_list[:i])

  return None

def get_true_false_questions(partial_sentence):
  
  input_ids = GPT2_tokenizer.encode(partial_sentence, return_tensors='pt')
  maximum_length = len(partial_sentence.split()) + 40
  sample_outputs = GPT2_model.generate(
    input_ids, 
    do_sample=True, 
    max_length=maximum_length, 
    top_p=0.80, # 0.85 
    top_k=60,   #30
    repetition_penalty  = 10.0,
    num_return_sequences=5
)
  generated_sentences = []
  for i,sample_output in enumerate(sample_outputs):
    decoded_sentence = GPT2_tokenizer.decode(sample_output, skip_special_tokens=True)
    final_sentence = tokenize.sent_tokenize(decoded_sentence)[0]
    generated_sentences.append(final_sentence)
  return generated_sentences

def semantic_textual_similarity(generated_sentences, q):

  model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
  embedding_two = model.encode(q, convert_to_tensor=True)
  for i in generated_sentences:
    embedding_one = model.encode(i, convert_to_tensor=True)
  
if __name__ == "__main__":
  nltk.download("punkt")
  benepar.download("benepar_en3")