FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt 
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
ENV HF_HUB_OFFLINE=1
COPY read.py api.py search.py ./
COPY data/chunks_350_minilm-en_arxiv.json data/vectors_350_minilm-en_arxiv.npy ./data/
EXPOSE 8000 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
