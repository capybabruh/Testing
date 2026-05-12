import streamlit as st
import base64
from mistralai.client import Mistral

#cấu hình api key của mistral
MISTRAL_API_KEY = "xUxOBWFsnhGgO2IbwOFYVe7GuTNFtCzd" 

# Cấu hình giao diện trang web
st.set_page_config(page_title="Công cụ OCR Dược phẩm", page_icon="📄", layout="centered")

#Hàm ocr
@st.cache_data(show_spinner=False)
def process_pdf_with_mistral(pdf_bytes):
    """Mã hóa file PDF và gọi Mistral OCR API để lấy Markdown"""
    client = Mistral(api_key=MISTRAL_API_KEY)
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    
    try:
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

#Giao diện
st.title("Hệ thống Trích xuất Dữ liệu (OCR)")
st.markdown("Tải lên tài liệu PDF (Scan hoặc Text gốc). Hệ thống sẽ tự động đọc và chuyển đổi thành văn bản để phục vụ nhập liệu.")

# Khu vực Upload File
uploaded_file = st.file_uploader("Chọn file PDF của bạn:", type=["pdf"])

# Nút xử lý
if uploaded_file is not None:
    # Hiển thị nút bấm nổi bật
    if st.button("Bắt đầu trích xuất OCR", type="primary", use_container_width=True):
        with st.spinner("Hệ thống đang đọc tài liệu, vui lòng chờ trong giây lát"):
            # Đọc byte từ file upload và chạy OCR
            pdf_bytes = uploaded_file.read()
            ocr_result = process_pdf_with_mistral(pdf_bytes)
            
            # Lưu kết quả vào session_state
            st.session_state['ocr_result'] = ocr_result
            st.success("Trích xuất thành công!")

st.divider() 

# Khu vực hiển thị kết quả
if 'ocr_result' in st.session_state:
    st.subheader("Kết quả trích xuất:")
    
    # Text area để người dùng dễ dàng copy từng đoạn
    st.text_area("Nội dung Text (Markdown)", value=st.session_state['ocr_result'], height=400)
    
    # Layout 2 cột cho các nút hành động (Copy / Tải xuống)
    col1, col2 = st.columns(2)
    
    with col1:
        # Streamlit mặc định không có nút Copy to Clipboard chuẩn cho text area, 
        # nhưng nhân viên có thể bôi đen copy trực tiếp từ ô phía trên.
        st.info("Bạn có thể bôi đen văn bản ở ô trên để Copy sang hệ thống nhập liệu.")
        
    with col2:
        st.download_button(
            label="Tải xuống file .md",
            data=st.session_state['ocr_result'],
            file_name="ket_qua_ocr.md",
            mime="text/markdown",
            use_container_width=True
        )