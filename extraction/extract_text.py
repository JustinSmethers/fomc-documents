import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_path):
    """Extract text from a PDF using PyMuPDF."""
    # Open the PDF file
    document = fitz.open(file_path)
    text = []

    # Extract text from each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text.append(page.get_text("text"))

    # Join all pages together
    return "\n".join(text)

def clean_text(text):
    """Preprocess the extracted text."""
    # Remove 'For Release at 200 p.m. EDT' from the beginning of the text
    text = re.sub(r"For release at 2:00 p.m. EDT", "", text).strip()

    # Remove special characters and extra whitespaces keeping only letters, numbers, and common punctuation and dashes and slashes
    text = re.sub(r"[^a-zA-Z0-9\s.,-\/]", "", text)
    # text = re.sub(r"[^a-zA-Z0-9\s.,]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Change deimals in percentages to commas
    # Then I can split the text into sentences
    text = re.sub(r"(\d+)\.(\d+) percent", r"\1,\2 percent", text)

    return text

def get_text_from_pdf(file_path):
    """Extract and clean text from a PDF file."""
    extracted_text = extract_text_from_pdf(file_path)
    cleaned_text = clean_text(extracted_text)
    return cleaned_text
