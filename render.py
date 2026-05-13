import streamlit as st
import pandas as pd
from ocr_service import process_pdf_with_mistral
from to_xlsx_file import parse_ocr_with_ai, to_excel, COLUMNS  

MISTRAL_API_KEY = "YOUR_API_KEY"

@st.cache_data(show_spinner=False)
def run_ocr(pdf_bytes, api_key):
    return process_pdf_with_mistral(pdf_bytes, api_key)

def render_results():
    if 'ocr_result' not in st.session_state:
        return

    st.text_area("Nội dung OCR thô", value=st.session_state['ocr_result'], height=300)

    if 'parsed_data' not in st.session_state:
        with st.spinner("Đang trích xuất thông tin có cấu trúc..."):
            st.session_state['parsed_data'] = parse_ocr_with_ai(
                st.session_state['ocr_result'], MISTRAL_API_KEY
            )

    # Preview — dùng COLUMNS thống nhất
    df_preview = pd.DataFrame(st.session_state['parsed_data'], columns=COLUMNS)
    st.dataframe(df_preview, use_container_width=True)

    excel_data = to_excel(st.session_state['parsed_data'])
    st.download_button(
        label="Tải xuống file Excel?",
        data=excel_data,
        file_name=st.session_state.get('file_name_output', 'ket_qua.xlsx'),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )