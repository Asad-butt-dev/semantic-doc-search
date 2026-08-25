from fastapi import FastAPI,Query
from search import search_chunks
from fastapi.middleware.cors import CORSMiddleware
import os 
from read import DEFAULT_CHUNK_SIZE

app = FastAPI()
origins=os.environ.get("ALLOWED_ORIGINS","http://localhost:5173").split(",")
@app.get("/search")
def search(query:str,use_hybrid:bool,bonus:float=Query(default=0,ge=0,le=0.4),key_terms:list[str]=Query(default=[]),):
    return search_chunks(query,key_terms,use_hybrid,DEFAULT_CHUNK_SIZE,bonus)


@app.get("/health")
def health():
    return {"status":"ok"}