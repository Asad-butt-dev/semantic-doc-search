import numpy as np
import json as js
from sentence_transformers import SentenceTransformer as ST
from read import DATA_DIR,model,model_name




def search_chunks(query:str,key_terms:list[str],use_hybrid:bool,chunk_size:int,bonus:float)->list[dict]:
    chunks=list()
    vectors=np.load(DATA_DIR/f"vectors_{chunk_size}_{model_name}.npy")
    with open(DATA_DIR/f"chunks_{chunk_size}_{model_name}.json","r",encoding="utf-8") as f:
       chunks=js.load(f)
    if model_name=="minilm-multi":
     query_vector=model.encode(query)
    elif model_name=="e5-base":
      query_vector=model.encode_query(query)
    scores=(query_vector*vectors)
    scores=scores.sum(axis=1)/(((query_vector**2).sum(axis=0)**0.5)*((vectors**2).sum(axis=1)**0.5))
    add_bonus_vector=scores.copy()
    if use_hybrid:
      dic=build_term_index(key_terms,str(chunk_size))
      bonus_list=np.zeros((len(chunks),))
      for values in dic.values():
          bonus_list[values]+=bonus
      add_bonus_vector+=bonus_list
    
    result=add_bonus_vector.argsort(axis=0)    
    if use_hybrid:
      return [{**chunks[i],"score":float(scores[i]),"bonus":float(bonus_list[i])} for i in result[-5:][::-1]]
    else:
      return [{**chunks[i],"score":float(scores[i])} for i in result[-5:][::-1]]


def build_term_index(key_terms:list[str],chunk_size:str)-> dict[str, list[int]]:
    list_of_chunks=list()
    dic={}
    with open(DATA_DIR/f"chunks_{chunk_size}.json","r",encoding="utf-8") as f:
        list_of_chunks=js.load(f)
    for element in key_terms:
        dic[element]=list()
        for i in range(len(list_of_chunks)):
            if element in list_of_chunks[i]["text"]:
                dic[element].append(i)
    return dic