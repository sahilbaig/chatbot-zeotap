from pdf_processor import extract_text_from_pdfs
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []
        self.metadata = []  # Store metadata (CDP name)

    def add_texts(self, texts):
        """Embeds and adds text chunks to FAISS."""
        embeddings = self.model.encode([t["text"] for t in texts], convert_to_numpy=True)
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadata.extend([t["cdp"] for t in texts])  # Store CDP source

    def load_pdfs(self, pdfs_root):
        """Extract and store PDF text by CDP type."""
        for cdp_name in os.listdir(pdfs_root):
            cdp_folder = os.path.join(pdfs_root, cdp_name)
            if os.path.isdir(cdp_folder):
                texts = extract_text_from_pdfs(cdp_folder, cdp_name)
                self.add_texts(texts)
                print(f"Loaded {len(texts)} chunks for {cdp_name} into FAISS.")

    def search(self, query, cdp_filter=None, top_k=3):
        """Finds top-k relevant chunks, optionally filtering by CDP."""
        if self.index is None:
            return ["No data loaded."]
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        _, indices = self.index.search(query_embedding, top_k)

        results = []
        for i in indices[0]:
            if cdp_filter is None or self.metadata[i] == cdp_filter:
                results.append({"text": self.texts[i]["text"], "cdp": self.metadata[i]})
        
        return results if results else ["No relevant info found."]

# Example Usage:
# store = VectorStore()
# store.load_pdfs("pdfs")  # Process all CDP docs
# print(store.search("How to set up Segment?", cdp_filter="segment"))
