import base64
import os
from mistralai.client import Mistral

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma 

#CẤU HÌNH
MISTRAL_API_KEY = "YOUR_API_KEY" 
PDF_PATH = r"D:\LuckyStarProject\COA - BM VB5.pdf"
OUTPUT_FILE = "ket_qua_test.md" 
def encode_pdf(path):
    try:
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file tại {path}")
        return None

def main():
    client = Mistral(api_key=MISTRAL_API_KEY)
    
    print(f"Đang đọc file PDF: {PDF_PATH}")
    #encode de mistral doc ocr
    pdf_base64 = encode_pdf(PDF_PATH)
    if not pdf_base64: return

    print("Đang gửi yêu cầu sang Mistral OCR")
    try:
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{pdf_base64}"#ocr 
            }
        )
    except Exception as e:
        print(f"Lỗi API Mistral: {e}")
        return

    print(f"Đang lưu nội dung gốc ra file '{OUTPUT_FILE}' để kiểm tra")
    
    full_markdown = ""
    docs = []
    
    for page in ocr_response.pages:
        # Tạo header để biết trang nào là trang nào
        page_header = f"\n\n--- TRANG {page.index + 1} ---\n\n"
        
        # Cộng dồn vào file tổng để xem
        full_markdown += page_header + page.markdown
        
        # Tạo document cho Chroma       
        docs.append(Document(
            page_content=page.markdown, 
            metadata={"page": page.index + 1, "source": PDF_PATH}
        ))
    
    # Ghi ra file .md (Markdown)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_markdown)
        
    print(f"mở file {OUTPUT_FILE} để xem")
    print("ok")

if __name__ == "__main__":
    main()