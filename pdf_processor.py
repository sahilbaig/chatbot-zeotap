import fitz
import os
import re
from summa.summarizer import summarize  # TextRank-based summarization

def chunk_text(text, chunk_size=500):
    """Splits text into smaller chunks of specified size."""
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def clean_and_filter_text(text):
    """Cleans extracted text and filters relevant content."""
    lines = text.split("\n")
    filtered_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Ignore empty lines and junk text
        if not line or len(line) < 5:
            continue

        # Ignore boilerplate (adjust patterns as needed)
        if re.search(r"(copyright|all rights reserved|terms of use)", line, re.I):
            continue
        
        # Keep lines that seem relevant (contain action words)
        if re.search(r"(setup|configure|enable|create|integration|how to|step|process)", line, re.I):
            filtered_lines.append(line)
    
    return " ".join(filtered_lines)

def summarize_text(text):
    """Summarizes text using TextRank if it's too long."""
    return summarize(text, ratio=0.3) if len(text) > 1000 else text

def extract_text_from_pdfs(pdf_folder, cdp_name):
    """Extracts, cleans, and chunks text from all PDFs in a given CDP's folder."""
    all_texts = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            doc = fitz.open(pdf_path)
            for page in doc:
                raw_text = page.get_text("text").strip()
                filtered_text = clean_and_filter_text(raw_text)
                
                if filtered_text:
                    summarized_text = summarize_text(filtered_text)
                    chunks = chunk_text(summarized_text)
                    for chunk in chunks:
                        all_texts.append({
                            "text": chunk,
                            "cdp": cdp_name,
                            "source": filename  # ✅ Store source file
                        })
    
    return all_texts
