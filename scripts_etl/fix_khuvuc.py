import pandas as pd
import os

def fix_province_names_in_csv(input_dir):
    # Danh sách các tỉnh cần sửa
    province_corrections = {
        "Hoà Bình": "Hòa Bình",
        "Khánh Hoà": "Khánh Hòa",
        "Thanh Hoá": "Thanh Hóa"
        "TP. Hồ Chí Minh": "TP.Hồ Chí Minh",
        "Thừa Thiên Huế": "Huế"
    }

    # Lặp qua tất cả các file CSV trong thư mục đầu vào
    for filename in os.listdir(input_dir):
        if filename.endswith('.csv'):
            # Đọc dữ liệu từ file CSV với mã hóa UTF-8
            file_path = os.path.join(input_dir, filename)
            df = pd.read_csv(file_path, encoding='utf-8')

            # Kiểm tra xem cột 'Khu vực' có tồn tại trong DataFrame không
            if 'Khu vực' in df.columns:
                # Thay thế các tên tỉnh thành trong cột "Khu vực"
                df['Khu vực'] = df['Khu vực'].replace(province_corrections)

                # Kiểm tra lại dữ liệu kiểu cột để đảm bảo giữ nguyên các cột số
                for column in df.select_dtypes(include=['float64', 'int64']).columns:
                    df[column] = pd.to_numeric(df[column], errors='coerce')

                # Lưu lại file CSV đã sửa (sửa trực tiếp trong file gốc) với mã hóa UTF-8
                df.to_csv(file_path, index=False, encoding='utf-8')
                print(f"Đã sửa file: {file_path}")
            else:
                print(f"File {file_path} không chứa cột 'Khu vực'")

# Ví dụ sử dụng hàm
fix_province_names_in_csv(input_dir=r'D:\Data Project\GOV\data_source')
