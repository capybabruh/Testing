import streamlit as st
import os
import pandas as pd
from render import *


def main():
    st.set_page_config(page_title="Công cụ OCR Dược phẩm", page_icon="📄", layout="centered")
    st.title("Hệ thống Trích xuất Dữ liệu (OCR)")
    
    uploaded_file = st.file_uploader("Chọn file PDF của bạn:", type=["pdf"])
    
    if uploaded_file is not None:
        # Lấy tên file gốc và đổi đuôi thành .xlsx
        base_name = os.path.splitext(uploaded_file.name)[0]
        excel_filename = f"{base_name}.xlsx"
        
        if st.button("Bắt đầu trích xuất OCR", type="primary", use_container_width=True):
            with st.spinner("Hệ thống đang xử lý..."):
                pdf_bytes = uploaded_file.read()
                ocr_result = run_ocr(pdf_bytes, MISTRAL_API_KEY)
                
                # Lưu cả kết quả text và tên file vào session_state
                st.session_state['ocr_result'] = ocr_result
                st.session_state['file_name_output'] = excel_filename
                st.success("Trích xuất thành công!")

    st.divider() 
    render_results()

if __name__ == "__main__":
    main()