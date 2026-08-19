from fastapi import FastAPI,Query
from search import searches
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins=[
    "http://localhost:5173"
]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.get("/search")
def search(query:str,use_hybrid:bool,chunk_size:int=Query(default=500,ge=199,le=651),bonus:float=Query(default=0,ge=0,le=0.6),key_terms:list[str]=Query(default=[]),):
    return searches(query,key_terms,use_hybrid,chunk_size,bonus)


@app.get("/health")
def health():
    return {"status":"ok"}