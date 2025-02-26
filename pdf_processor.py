import fitz
import os

def extract_text_from_pdfs(pdf_folder):
    """Extract text from all PDFs in a folder."""
    all_texts = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            doc = fitz.open(pdf_path)
            for page in doc:
                text = page.get_text("text").strip()
                if text:
                    all_texts.append(text)
    return all_texts