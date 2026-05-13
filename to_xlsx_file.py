import re, json, pandas as pd
from io import BytesIO
from mistralai.client import Mistral

# Thống nhất 4 cột — tiếng Anh, khớp với prompt
COLUMNS = ['Product Name', 'Lot No.', 'Date Produced', 'Shelf Life']

def parse_ocr_with_ai(ocr_text: str, api_key: str) -> list[dict]:
    client = Mistral(api_key=api_key)

    prompt = f"""Extract information from the OCR text below and return a JSON array.
Each element must have exactly these 4 keys:
- "Product Name"
- "Lot No."
- "Date Produced"
- "Shelf Life"

Return ONLY raw JSON array, no explanation, no markdown.

OCR Text:
{ocr_text}
"""
    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    result = json.loads(raw)

    # Đảm bảo luôn trả về list
    if isinstance(result, dict):
        result = [result]
    return result


def to_excel(parsed_list: list[dict]) -> bytes:
    df = pd.DataFrame(parsed_list, columns=COLUMNS)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='KetQua')
        worksheet = writer.sheets['KetQua']
        for col in worksheet.columns:
            max_len = max((len(str(cell.value or "")) for cell in col), default=10)
            worksheet.column_dimensions[col[0].column_letter].width = max_len + 4
    return output.getvalue()