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
