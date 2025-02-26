from pdf_processor import extract_text_from_pdfs
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []

    def add_texts(self, texts):
        """Embeds and adds text chunks to FAISS."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.texts.extend(texts)

    def load_pdfs(self, pdf_folder):
        """Extract and store PDF text into FAISS."""
        texts = extract_text_from_pdfs(pdf_folder)
        self.add_texts(texts)
        print(f"Loaded {len(texts)} text chunks into FAISS.")

    def search(self, query, top_k=3):
        """Finds top-k relevant chunks."""
        if self.index is None:
            return ["No data loaded."]
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        _, indices = self.index.search(query_embedding, top_k)
        return [self.texts[i] for i in indices[0]]

