import json as js 
import numpy as np
import pathlib as p
import copy
from search import search_chunks
from read import model_name,MODElS_MAX_TOKEN

def eval():
 hard_queries=list()
 score_list=list()
 if (p.Path(__file__).parent/"eval/scores.json").exists and (p.Path(__file__).parent/"eval/scores.json").stat().st_size>0:
  with open(p.Path(__file__).parent/"eval/scores.json","r",encoding="utf-8") as f:
    score_list.extend(js.load(f))
 with open("eval.json","r",encoding="utf-8") as f:
         query=js.load(f)
 with open(p.Path(__file__).parent/"eval/scores.json","w",encoding="utf-8") as f:
  for chunk_size in range(200,651,50):
    
    TP1=0
    TP5=0
    MRC=0
    unique=True
    for element in query:
        result=search_chunks(element["query"],[],False,chunk_size,0)
    
        for i,score in enumerate(result,start=1):
             if element["file_name"]==score["file_name"]:
               if unique:
                 TP5+=1
                 MRC+=1/i
                 unique=False
               if i==1:
                    TP1+=1
        if unique and element["content_type"]=="formula":
          hard_queries.append(element)
        unique=True
            

    score_list.append({"model":model_name,"max_tokens":MODElS_MAX_TOKEN[model_name],"chunk_size":chunk_size,"hybrid":False,"Recall@1":round(TP1/len(query),3), "Recall@5":round((TP5/len(query)),3),"Mean Reciprocal Rank":round((MRC/len(query)),3)})      
  js.dump(score_list,f)
  with open(p.Path(__file__).parent/"eval/hard_queries.json","w",encoding="utf-8") as f:
    js.dump(hard_queries,f)
  
def eval_category():
  score_list=list()
  unique=True
  evaluation_dict={"conceptual":{"Recall@1":0.0, "Recall@5":0.0,"Mean Reciprocal Rank":0.0}, "formula":{"Recall@1":0.0, "Recall@5":0.0,"Mean Reciprocal Rank":0.0},"broad":{"Recall@1":0.0, "Recall@5":0.0,"Mean Reciprocal Rank":0.0},"specific":{"Recall@1":0.0, "Recall@5":0.0,"Mean Reciprocal Rank":0.0}}
  
  with open(p.Path(__file__).parent/"eval.json","r",encoding="utf-8") as f:
    query=js.load(f)
  count_categories={"conceptual":0, "formula":0,"broad":0,"specific":0}
  for entry in query:
    count_categories[entry["specificity"]]+=1
    count_categories[entry["content_type"]]+=1
  
  with open(p.Path(__file__).parent/"eval/scores_categories.json","w",encoding="utf-8") as f:
    for chunk_size in range(200,651,50):
     evaluation_dict_current=copy.deepcopy(evaluation_dict)
     for entry in query:
      result=search_chunks(entry["query"],[],False,chunk_size,0)
      for i,score in enumerate(result,start=1):
         if entry["file_name"]==score["file_name"]:
          if unique:
           evaluation_dict_current[entry["specificity"]]["Recall@5"]+=1/count_categories[entry["specificity"]]
           evaluation_dict_current[entry["specificity"]]["Mean Reciprocal Rank"]+=1/(i*count_categories[entry["specificity"]])
           evaluation_dict_current[entry["content_type"]]["Recall@5"]+=1/count_categories[entry["content_type"]]
           evaluation_dict_current[entry["content_type"]]["Mean Reciprocal Rank"]+=1/(i*count_categories[entry["content_type"]])
           unique=False
          if i==1:
             evaluation_dict_current[entry["specificity"]]["Recall@1"]+=1/count_categories[entry["specificity"]]
             evaluation_dict_current[entry["content_type"]]["Recall@1"]+=1/count_categories[entry["content_type"]]
      unique=True
     score_list.append({chunk_size:evaluation_dict_current})
    
    js.dump(score_list,f)
if __name__ == "__main__":
    eval()