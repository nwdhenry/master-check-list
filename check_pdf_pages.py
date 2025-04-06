import sys
from PyPDF2 import PdfReader

def check_pdf_page_count(pdf_path):
    """Check if PDF has exactly one page"""
    try:
        reader = PdfReader(pdf_path)
        page_count = len(reader.pages)
        print(f"PDF has {page_count} pages")
        return page_count == 1
    except Exception as e:
        print(f"Error checking PDF: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_pdf_pages.py [PDF_FILE]")
        sys.exit(1)
    
    if check_pdf_page_count(sys.argv[1]):
        print("SUCCESS: PDF is one page")
        sys.exit(0)
    else:
        print("FAILURE: PDF is not one page")
        sys.exit(1)
