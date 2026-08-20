import json as js 
import numpy as np
import pathlib as p
from sentence_transformers import SentenceTransformer as ST
from search import search_chunks


def eval():
  for chunk_size in range(200,250,50):
    with open("eval.json","r",encoding="utf-8") as f:
        query=js.load(f)
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
            
    with open(p.Path(__file__).parent/"eval/scores.json","w",encoding="utf-8") as f:
           f.write("size of chunk:"+str(chunk_size)+": Recall@1:"+f"{(TP1/len(query)):.3f}"+" Recall@5: "+f"{(TP5/len(query)):.3f}"+" Mean Reciprocal Rank:"+f"{(MRC/len(query)):.3f}"+"\n")       
    
if __name__ == "__main__":
    eval()