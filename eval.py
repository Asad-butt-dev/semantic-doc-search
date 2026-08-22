import json as js 
import numpy as np
import pathlib as p
from sentence_transformers import SentenceTransformer as ST
from search import search_chunks


def eval():
 score_list=list()
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
        unique=True
            

    score_list.append({"Size of chunk":chunk_size,"Recall@1":round(TP1/len(query),3), "Recall@5":round((TP5/len(query)),3),"Mean Reciprocal Rank":round((MRC/len(query)),3)})      
  js.dump(score_list,f)
if __name__ == "__main__":
    eval()