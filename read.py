
import pathlib as p
import pypdf as pdf
import numpy as np
import json as js
from typing import TypedDict
from sentence_transformers import SentenceTransformer as ST
import os
os.environ["HF_HUB_OFFLINE"] = "1"
MODELS = {
    "minilm-multi": "paraphrase-multilingual-MiniLM-L12-v2",
    "e5-base": "intfloat/multilingual-e5-base",
    "minilm-en": "sentence-transformers/all-MiniLM-L6-v2",
}
MODElS_MAX_TOKEN={   "minilm-multi": 128,
    "e5-base": 512,
    "minilm-en": 256,
    
}
model=ST(MODELS["minilm-en"])
model_name="minilm-en"
DATA_DIR=p.Path(__file__).parent/"data"
DATA_DIR.mkdir(exist_ok=True)
class Chunk(TypedDict):
    text:str 
    file_name:str
    chunk_number:int



def read_data(path: p.Path)->str: 
   if p.Path.is_file(path):
     pdf_reader=pdf.PdfReader(path)
     pages=[pdf_reader.get_page(i) for i in range(pdf_reader.get_num_pages())]
     text=[pages[i].extract_text() for i in range(len(pages))]
     extract=""
     for c in text:
         extract+="\n"+c
     return extract
    
   else:
       raise Exception
   
def load_chunks(path:p.Path,chunk_size:int)->list[Chunk]:
    extract=read_data(path)
    n_Chunks=len(extract)//chunk_size
    chunk_per_file=list()
    for i in range(n_Chunks):
        chunk_per_file.append({"text":extract[i*chunk_size:chunk_size+i*chunk_size],"file_name":path.name,"chunk_number":i})
    return chunk_per_file
    



def read_all_data(chunk_size:int)->list[Chunk]:
    chunks=list()
    for i in p.Path.iterdir(p.Path(p.Path(__file__).parent/"dokumente")):
        chunks.extend(load_chunks(i,chunk_size))
    return chunks
def embedd(chunk_size:str,chunks:list):
  vectors=model.encode_document([chunks[i]["text"] for i in range(0,len(chunks))],show_progress_bar=True)
  np.save(DATA_DIR/f"vectors_{chunk_size}_{model_name}.npy",vectors)
  with open(DATA_DIR/f"chunks_{chunk_size}_{model_name}.json","w",encoding="utf-8") as f:
        
     js.dump(chunks,f,ensure_ascii=False)
    



if __name__=="__main__":
 for chunk_size in range(200,651,50):
   chunks=read_all_data(chunk_size)
   embedd(str(chunk_size),chunks)
   