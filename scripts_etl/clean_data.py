import pandas as pd
import os
import glob

def process_csv_files(input_folder, output_folder):
    # Tạo folder đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Lấy danh sách tất cả file .csv trong folder
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    
    print(f"Tìm thấy {len(csv_files)} file CSV. Bắt đầu xử lý...")

    for file_path in csv_files:
        try:
            # Lấy tên file
            file_name = os.path.basename(file_path)
            print(f"Đang xử lý: {file_name}")

            # 1. Đọc file CSV
            # encoding='utf-8-sig' giúp đọc tốt tiếng Việt và tránh lỗi ký tự lạ
            df = pd.read_csv(file_path, encoding='utf-8-sig')

            # 2. Xóa khoảng trắng thừa (Trim whitespace)
            # Chỉ áp dụng cho các cột có dữ liệu dạng chữ (object/string)
            df_obj = df.select_dtypes(['object'])
            df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

            # 4. Xóa dữ liệu trùng lặp 
            # keep='first': Giữ lại hàng đầu tiên tìm thấy, xóa các hàng trùng sau đó
            df = df.drop_duplicates(keep='first')

            # 5. Lưu file đã làm sạch sang folder mới
            output_path = os.path.join(output_folder, file_name)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_name}: {e}")

    print("Hoàn tất xử lý dữ liệu!")

# --- CẤU HÌNH ĐƯỜNG DẪN TẠI ĐÂY ---
# Thay đổi đường dẫn tới folder chứa file gốc của bạn
input_dir = r"D:\Data Project\GOV\data_source" 

# Thay đổi đường dẫn tới folder bạn muốn lưu file đã sửa
output_dir = r"D:\Data Project\GOV\data_source"

# Chạy hàm
process_csv_files(input_dir, output_dir)