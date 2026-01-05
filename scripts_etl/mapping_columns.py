"""
Mapping tên cột tiếng Việt sang tên cột tiếng Anh chuẩn (theo DDL trong Mục tiêu.docx)

- Dùng cho cả DIM và FACT.
- Các key là đúng y chang header trong data_catalog.csv (và file CSV gốc).
- Các value là tên cột tiếng Anh đúng như trong các câu lệnh CREATE TABLE stats.dim_*, stats.fact_*.
"""

import unicodedata
import re

COLUMN_MAPPING = {
    # ===== DIM / KHÓA TỰ NHIÊN =====
    'Năm': 'year',

    'Khu vực': 'province_name_vi',
    'Vùng': 'region_name_vi',
    'Loại khu vực': 'area_type_name_vi',

    'Giới tính': 'gender_name_vi',
    'Nhóm tuổi': 'age_group_label_vi',

    'Trình độ': 'edu_level_vi',

    'Khu vực kinh tế': 'econ_sector_name_vi',
    'Loại hình kinh tế': 'econ_type_name_vi',
    'Ngành kinh tế': 'industry_name_vi',
    'Ngành nghề': 'occupation_name_vi',
    'Vị thế việc làm': 'job_status_name_vi',

    # ===== MEASURES – đúng theo comment trong các bảng FACT =====
    'Dân số': 'population',
    'Diện tích': 'area',
    'Mật độ dân số': 'population_density',

    'Lao động có việc làm': 'employed',
    'Số lao động có việc làm': 'employed',
    'Lực lượng lao động': 'labor_force',
    'Năng suất lao động': 'labor_productivity',

    'Tuổi thọ': 'life_expectancy',
    'Tỷ lệ dân số biết chữ': 'literacy_rate',
    'Tỷ lệ biết chữ': 'literacy_rate',

    'Tỷ lệ lao động đã qua đào tạo': 'trained_labor_rate',

    'Tỷ lệ lao động việc làm phi chính thức': 'informal_employment_rate',

    'Tỷ lệ tăng dân số': 'population_growth_rate',
    'Tỷ lệ thất nghiệp': 'unemployment_rate',
    'Tỷ lệ thiếu việc làm': 'underemployment_rate',

    'Tỷ số giới tính': 'sex_ratio',

    'Tỷ suất nhập cư': 'immigration_rate',
    'Tỷ suất xuất cư': 'emigration_rate',
    'Tỷ suất di cư thuần': 'net_migration_rate',

    'Tỷ suất sinh': 'birth_rate',
    'Tỷ suất sinh thô': 'crude_birth_rate',
    'Tỷ suất chết thô': 'crude_death_rate',
    'Tỷ lệ tăng tự nhiên': 'natural_increase_rate',
    'Tổng tỷ suất sinh': 'tfr',
}


def _to_snake_ascii(vn_name: str) -> str:
    """
    Fallback: bỏ dấu + chuyển về snake_case ASCII.
    Dùng khi cột không có trong COLUMN_MAPPING.
    """
    # normalize unicode -> tách dấu
    nfkd = unicodedata.normalize("NFKD", vn_name)
    # bỏ ký tự dấu (combining)
    no_accent = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    # chuẩn hoá Đ/đ
    no_accent = no_accent.replace("Đ", "D").replace("đ", "d")
    # lower + thay chuỗi không phải [a-z0-9] bằng underscore
    s = no_accent.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    return s


def normalize_column_name(vn_name: str) -> str:
    """
    Chuyển tên cột tiếng Việt (như trong data_catalog & file CSV)
    sang tên cột tiếng Anh chuẩn dùng trong ETL / DDL.

    - Nếu có trong COLUMN_MAPPING thì dùng mapping.
    - Nếu không, fallback sang snake_case ASCII để không làm gãy ETL.
    """
    if vn_name is None:
        return vn_name

    vn_name = str(vn_name).strip()

    if vn_name in COLUMN_MAPPING:
        return COLUMN_MAPPING[vn_name]

    return _to_snake_ascii(vn_name)
