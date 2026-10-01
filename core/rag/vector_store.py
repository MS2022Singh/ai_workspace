import os
import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "memory", "vector", "chroma_db")
os.makedirs(DB_DIR, exist_ok=True)

class RAGEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_DIR)
        self.collection = self.client.get_or_create_collection(name="workspace_knowledge")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_document(self, doc_id: str, text: str, source: str = "web"):
        embedding = self.model.encode(text).tolist()
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"source": source}]
        )

    def query_context(self, query: str, n_results: int = 3) -> str:
        if self.collection.count() == 0:
            return ""
        embedding = self.model.encode(query).tolist()
        results = self.collection.query(query_embeddings=[embedding], n_results=min(n_results, self.collection.count()))
        docs = results.get("documents", [[]])[0]
        return "\n---\n".join(docs)

rag_engine = RAGEngine()