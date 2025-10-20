"""
Resume Parser using PyMuPDF (fitz) for fast PDF text extraction.
"""
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from all pages
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")
