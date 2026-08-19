import json as js 
import numpy as np
from sentence_transformers import SentenceTransformer as ST
from search import searches


def eval():
  for chunksize in range(200,700,50):
    with open("eval.json","r",encoding="utf-8") as f:
        query=js.load(f)
    TP=0 
    
    for element in query:
        result=searches(element["qu"],[],False,chunksize,0)
       
        if result["Dateiname"]==element["data"]:
            TP+=1
  
    print("Für Chunksize"+str(chunksize)+":"+ str(TP/len(query)))