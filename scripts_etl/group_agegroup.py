import pandas as pd

# Đọc file CSV
file_path = "D:\\Data Project\\GOV\\data_source\\tylelaodongvieclamphichinhthuc_nhomtuoi.csv"  # Đường dẫn file gốc

df = pd.read_csv(file_path)

# Hiển thị vài dòng đầu để kiểm tra cấu trúc dữ liệu
print(df.head())

# Hàm để gộp nhóm tuổi
def reassign_age_group(age_group):
    if age_group in ['15-19', '20-24']:
        return '15-24'
    elif age_group in ['25-29', '30-34', '35-39', '40-44', '45-49']:
        return '25-49'
    elif age_group in ['50+']:
        return '50+'
    else:
        return age_group

# Áp dụng hàm để gộp nhóm tuổi
df['Nhóm tuổi'] = df['Nhóm tuổi'].apply(reassign_age_group)

# Nhóm dữ liệu theo nhóm tuổi và năm, tính tổng số lao động có việc làm
df_grouped = df.groupby(['Nhóm tuổi', 'Năm'], as_index=False)['Tỷ lệ lao động việc làm phi chính thức'].sum()

# Ghi trực tiếp kết quả vào file CSV gốc
df_grouped.to_csv(file_path, index=False)

print(f"File đã được sửa trực tiếp tại {file_path}")
