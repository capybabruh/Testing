import base64
import os 
from mistralai.client import Mistral
def process_pdf_with_mistral(pdf_bytes, api_key):
    """Mã hóa file PDF và gọi Mistral OCR API để lấy Markdown"""
    try:
        client = Mistral(api_key=api_key)
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
        
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{pdf_base64}"
            }
        )
        
        full_markdown = ""
        for page in ocr_response.pages:
            full_markdown += f"\n\n--- TRANG {page.index + 1} ---\n\n"
            full_markdown += page.markdown
            
        return full_markdown
    except Exception as e:
        return f"Lỗi API Mistral: {str(e)}"