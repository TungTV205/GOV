import os
import pandas as pd

# ===== 1. Cấu hình đường dẫn =====
FOLDER_PATH = r"D:\Data Project\GOV\data_source"   # sửa lại nếu cần
CATALOG_FILE = "data_catalog.csv"

# ===== 2. Duyệt toàn bộ file CSV =====
catalog_records = []

for file_name in os.listdir(FOLDER_PATH):
    if not file_name.endswith(".csv"):
        continue

    # Bỏ qua chính file data_catalog.csv
    if file_name == CATALOG_FILE:
        continue

    file_path = os.path.join(FOLDER_PATH, file_name)

    try:
        df = pd.read_csv(file_path)

        num_rows = len(df)
        num_columns = len(df.columns)
        column_names = ", ".join(df.columns)

        catalog_records.append({
            "table_name": file_name,
            "num_rows": num_rows,
            "num_columns": num_columns,
            "column_names": column_names
        })

    except Exception as e:
        print(f"Lỗi khi đọc {file_name}: {e}")

# ===== 3. Tạo DataFrame data catalog =====
catalog_df = pd.DataFrame(catalog_records)

# ===== 4. Ghi đè trực tiếp data_catalog.csv =====
catalog_path = os.path.join(FOLDER_PATH, CATALOG_FILE)
catalog_df.to_csv(catalog_path, index=False, encoding="utf-8-sig")

print("Đã cập nhật data_catalog.csv thành công.")
