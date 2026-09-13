# Semantic Document Search
A semantic search engine over PDF corpora, benchmarked across 3 embedding models and 10 chunk sizes with Recall@1/@5 and MRR.

[Live Demo](https://search.asadbutt.de)

<img width="973" height="923" alt="Animation" src="https://github.com/user-attachments/assets/40bd1e48-3be4-448d-9b12-3ec2def321f0" />



## Evaluation







 ## Architecture

 ```mermaid
flowchart LR
    Browser["Browser"]

    subgraph compose["Docker Compose · Hetzner"]
        Caddy["Caddy<br/>TLS termination"]
        Nginx["nginx<br/>serves React build"]
        Backend["FastAPI backend"]
    end

    Data[("data/<br/>chunks + embeddings (.npy)")]

    Browser -- HTTPS --> Caddy
    Caddy --> Nginx
    Nginx -- "/api/*" --> Backend
    Backend -. loads at startup .-> Data
```

## Tech Stack

**Backend**
- Python
- FastAPI
- sentence-transformers
- numpy (manual cosine similarity, no vector DB)

**Frontend**
- React
- TypeScript
- Vite
- Mantine (component library)

**Deployment**
- Docker Compose (backend, frontend, caddy services)
- nginx (serves Vite build, proxies `/api/` to backend)
- Caddy (reverse proxy, automatic HTTPS)
- Hetzner Cloud (Ubuntu 24, 4 GB RAM)

## Features

- Natural-language search over a PDF corpus using embedding similarity
- Hybrid search with an additive term-match bonus (keyword + semantic signal combined)
- Loading state, error handling, and empty-query guard
- Example query buttons for a quick first try
- Clickable links to the source arXiv paper for each result

 ## Limitations

- **No OCR** — image-based PDFs (scanned slides, no text layer) yield zero extractable chunks
- **Linear scan** — cosine similarity is computed against every chunk; fine at ~500 chunks, won't scale to millions without an index
- **Hybrid search is an additive bonus, not true hybrid retrieval** — a real implementation would combine BM25 and embedding scores via something like Reciprocal Rank Fusion (RRF)
- **Token truncation** — MiniLM-based models only encode the first ~90 words of a chunk; longer chunks are silently cut off
- **Eval set is LLM-generated** — phrasing may sit closer to the source wording than a human query would, which can inflate the reported scores



## Setup / Run locally

1. Clone the repo
   \```bash
   git clone https://github.com/<your-username>/semantic-doc-search.git
   cd semantic-doc-search
   \```

2. Build the local corpus (downloads arXiv papers, chunks and embeds them)
   \```bash
   python fetch_arxiv.py
   python read.py
   \```
   This populates `data/` with chunk JSON and `.npy` embedding files used by the backend.

3. Start the full stack
   \```bash
   docker compose up --build
   \```

4. Open `http://localhost` in your browser.

## Project Structure

```
semantic-doc-search/
api.py — FastAPI endpoints
search.py — search logic (search_chunks function)
read.py — text extraction, chunking, model loading
eval.py — evaluation script (Recall@1, Recall@5, MRR)
plot.py — matplotlib charts
fetch_arxiv.py — downloads papers from arXiv API
Dockerfile — backend container
docker-compose.yml — full stack (backend, frontend, caddy)
Caddyfile — reverse proxy config
requirements.txt
eval.json — 100 labelled queries
data/ — chunk JSON + vector .npy files (gitignored)
images/ — matplotlib PNGs for README
frontend/
Dockerfile — multi-stage: node build → nginx
nginx.conf — proxies /api/ to backend:8000
src/
App.tsx — main component
ResultList.tsx — extracted result display component
types.ts — SearchResult interface
```
