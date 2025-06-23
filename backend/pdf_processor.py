import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF using PyMuPDF (fitz).
    Only extracts visible text—does not perform OCR.
    
    Args:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted plain text from all pages.
    """
    extracted_text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            extracted_text += page.get_text()
    return extracted_text
