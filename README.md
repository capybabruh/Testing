# 📄 Pharmaceutical OCR Data Extraction Tool
> Hệ thống trích xuất dữ liệu tự động từ file PDF dược phẩm sử dụng Mistral OCR AI

---

## 🖼️ Tổng quan

Ứng dụng web cho phép người dùng tải lên file PDF nhãn dược phẩm, tự động nhận diện và trích xuất 4 trường thông tin quan trọng, sau đó xuất ra file Excel `.xlsx` có cấu trúc.

**Luồng xử lý:**
```
PDF Upload → Mistral OCR (Markdown) → AI Extraction (JSON) → Excel (.xlsx)
```

---

## ✨ Tính năng

- 📤 Upload file PDF trực tiếp trên giao diện web
- 🔍 OCR bằng **Mistral OCR API** — nhận diện văn bản chính xác cao
- 🤖 Trích xuất có cấu trúc bằng **Mistral Large** (AI extraction)
- 📊 Preview bảng dữ liệu ngay trên giao diện trước khi tải xuống
- 💾 Xuất file `.xlsx` với tên file tự động theo tên PDF gốc
- ⚡ Cache kết quả OCR — không gọi API lại khi re-render

---

## 📋 Dữ liệu được trích xuất

| Cột | Mô tả |
|-----|-------|
| `Product Name` | Tên sản phẩm / thuốc |
| `Lot No.` | Số lô sản xuất |
| `Date Produced` | Ngày sản xuất |
| `Shelf Life` | Hạn sử dụng |

---

## 🗂️ Cấu trúc dự án

```
LuckyStarProject/
├── app.py              # Entry point — Streamlit UI chính
├── render.py           # Logic render kết quả + download button
├── ocr_service.py      # Gọi Mistral OCR API
├── to_xlsx_file.py     # AI extraction + xuất file Excel
├── requirements.txt    # Danh sách thư viện
└── README.md
```

---

## 🚀 Hướng dẫn cài đặt & chạy

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### 4. Cấu hình API Key

Mở file `render.py`, thay thế giá trị `MISTRAL_API_KEY`:

```python
MISTRAL_API_KEY = "your_mistral_api_key_here"
```

> ⚠️ **Lưu ý bảo mật:** Không commit API key lên GitHub. Nên dùng `.env` file hoặc `st.secrets` trong môi trường production.

### 5. Chạy ứng dụng

```bash
streamlit run app.py
```

Mở trình duyệt tại: `http://localhost:8501`

---

## 📦 Requirements

```
streamlit==1.45.0
pandas
numpy
mistralai
openpyxl
```

---

## 🔐 Bảo mật API Key (khuyến nghị)

Thay vì hardcode API key trong code, nên dùng Streamlit Secrets:

**Tạo file `.streamlit/secrets.toml`:**
```toml
MISTRAL_API_KEY = "your_api_key_here"
```

**Truy cập trong code:**
```python
MISTRAL_API_KEY = st.secrets["MISTRAL_API_KEY"]
```

**Thêm vào `.gitignore`:**
```
.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
```

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Mục đích |
|-----------|----------|
| [Streamlit](https://streamlit.io/) | Web UI framework |
| [Mistral OCR](https://mistral.ai/) | Nhận diện văn bản từ PDF |
| [Mistral Large](https://mistral.ai/) | Trích xuất thông tin có cấu trúc |
| [Pandas](https://pandas.pydata.org/) | Xử lý dữ liệu dạng bảng |
| [OpenPyXL](https://openpyxl.readthedocs.io/) | Xuất file Excel |

---

## 📄 License

MIT License © 2025 LuckyStar Project
