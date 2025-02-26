import fitz
import os

def chunk_text(text, chunk_size=500):
    """Splits text into smaller chunks of specified size."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def extract_text_from_pdfs(pdf_folder, cdp_name):
    """Extracts and chunks text from all PDFs in a given CDP's folder."""
    all_texts = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            doc = fitz.open(pdf_path)
            for page in doc:
                text = page.get_text("text").strip()
                if text:
                    chunks = chunk_text(text)
                    for chunk in chunks:
                        all_texts.append({"text": chunk, "cdp": cdp_name})
    return all_texts
