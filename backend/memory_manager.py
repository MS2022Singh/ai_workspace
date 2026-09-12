import os
import json
import logging
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MemoryManager")

DATA_DIR = "C:\\AI_Workspace\\ai_workspace_core\\data"
MEMORY_FILE = os.path.join(DATA_DIR, "long_term_memory.json")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")

os.makedirs(DATA_DIR, exist_ok=True)

class MemoryManager:
    def __init__(self):
        self.short_term_buffer: List[Dict[str, Any]] = []
        self.long_term_memory: Dict[str, Any] = self._load_long_term_memory()
        
        # Initialize ChromaDB Vector Store
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
        self.vector_collection = self.chroma_client.get_or_create_collection(name="workspace_rag")
        logger.info("Memory Manager & Vector Store initialized successfully.")

    def _load_long_term_memory(self) -> Dict[str, Any]:
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load long-term memory: {e}")
        return {"projects": {}, "entities": {}, "user_preferences": {}}

    def save_long_term_memory(self):
        try:
            with open(MEMORY_FILE, "w") as f:
                json.dump(self.long_term_memory, f, indent=2)
            logger.info("Long-term memory saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save long-term memory: {e}")

    def add_short_term(self, role: str, content: str):
        self.short_term_buffer.append({"role": role, "content": content})
        if len(self.short_term_buffer) > 20:  # Keep buffer under 20 messages
            self.short_term_buffer.pop(0)

    def add_document_to_vector_store(self, doc_id: str, document_text: str, metadata: dict = None):
        metadata = metadata or {}
        self.vector_collection.add(
            documents=[document_text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        logger.info(f"Indexed document '{doc_id}' into ChromaDB RAG vector store.")

    def search_vector_store(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        results = self.vector_collection.query(
            query_texts=[query],
            n_results=top_k
        )
        hits = []
        if results and "documents" in results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i] if "metadatas" in results else {}
                hits.append({"document": doc, "metadata": meta})
        return hits

memory_manager = MemoryManager()