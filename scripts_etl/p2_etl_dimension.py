import os
import pandas as pd
from sqlalchemy import create_engine, text

# ==============================
# CONFIG
# ==============================
DB_URL = "postgresql+psycopg2://postgres:tungpostgresql123@localhost:5432/Gov"
DATA_DIR = r"D:\Data Project\GOV\data_source" # thư mục chứa tất cả CSV + data_catalog.csv

CATALOG_PATH = os.path.join(DATA_DIR, "data_catalog.csv")

engine = create_engine(DB_URL, future=True)
catalog = pd.read_csv(CATALOG_PATH)

def split_columns(col_string: str):
    return [c.strip() for c in col_string.split(",")]


def tables_having_column(column_names: pd.Series, target_cols):
    """
    target_cols: list tên cột gốc trong CSV (ví dụ ['Giới tính'])
    trả về mask bool: bảng nào có ít nhất 1 trong các cột đó
    """
    target_cols = set(target_cols)
    mask = []
    for cols_str in column_names:
        cols = set(split_columns(cols_str))
        mask.append(len(cols & target_cols) > 0)
    return pd.Series(mask, index=column_names.index)


def load_simple_dim(
    dim_table: str,
    source_column_names,
    dest_column: str,
    schema: str = "stats",
):
    """
    Dimension kiểu đơn giản: chỉ cần 1 cột text (ví dụ Giới tính → dim_gender.gender_name_vi)
    source_column_names: list tên cột trong CSV (có thể có alias cũ/mới)
    """
    source_column_names = list(source_column_names)
    frames = []

    # chọn các bảng có bất kỳ cột nào trong source_column_names
    mask = tables_having_column(catalog["column_names"], source_column_names)
    selected = catalog[mask]

    for _, row in selected.iterrows():
        table = row["table_name"]
        cols = split_columns(row["column_names"])

        # tìm tên cột thực sự có trong bảng này
        src_col = None
        for cand in source_column_names:
            if cand in cols:
                src_col = cand
                break
        if src_col is None:
            continue

        path = os.path.join(DATA_DIR, table)
        df = pd.read_csv(path, usecols=[src_col])
        df = df.rename(columns={src_col: dest_column})
        frames.append(df)

    if not frames:
        print(f"[WARN] Không tìm thấy dữ liệu cho dimension {dim_table}")
        return

    dim_df = (
        pd.concat(frames)[[dest_column]]
        .dropna()
        .drop_duplicates()
        .sort_values(dest_column)
        .reset_index(drop=True)
    )

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE {schema}.{dim_table} RESTART IDENTITY CASCADE"))
        dim_df.to_sql(
            dim_table, conn, schema=schema, if_exists="append", index=False
        )
    print(f"[OK] Loaded {len(dim_df)} rows into {schema}.{dim_table}")


# ==============================
# 1) dim_time
# ==============================

def load_dim_time():
    frames = []
    mask = tables_having_column(catalog["column_names"], ["Năm"])
    selected = catalog[mask]

    for _, row in selected.iterrows():
        table = row["table_name"]
        path = os.path.join(DATA_DIR, table)
        df = pd.read_csv(path, usecols=["Năm"])
        frames.append(df)

    years = (
        pd.concat(frames)["Năm"]
        .dropna()
        .drop_duplicates()
        .astype(int)
        .sort_values()
        .reset_index(drop=True)
    )

    dim_df = pd.DataFrame(
        {
            "year": years,
            "year_label": years.astype(str),
        }
    )

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE stats.dim_time RESTART IDENTITY CASCADE"))
        dim_df.to_sql(
            "dim_time", conn, schema="stats", if_exists="append", index=False
        )
    print(f"[OK] Loaded {len(dim_df)} rows into stats.dim_time")


# ==============================
# 2) dim_region (Vùng)
# ==============================

def load_dim_region():
    load_simple_dim(
        dim_table="dim_region",
        source_column_names=["Vùng"],
        dest_column="region_name_vi",
        schema="stats",
    )


# ==============================
# 3) dim_area_type (Loại khu vực)
# ==============================

def load_dim_area_type():
    load_simple_dim(
        dim_table="dim_area_type",
        source_column_names=["Loại khu vực"],
        dest_column="area_type_name_vi",
        schema="stats",
    )


# ==============================
# 4) Các dim đơn giản khác
# ==============================

def load_dim_gender():
    load_simple_dim(
        dim_table="dim_gender",
        source_column_names=["Giới tính"],
        dest_column="gender_name_vi",
        schema="stats",
    )


def load_dim_age_group():
    load_simple_dim(
        dim_table="dim_age_group",
        source_column_names=["Nhóm tuổi"],
        dest_column="age_group_label_vi",
        schema="stats",
    )


def load_dim_education():
    load_simple_dim(
        dim_table="dim_education",
        source_column_names=["Trình độ"],
        dest_column="edu_level_vi",
        schema="stats",
    )


def load_dim_economic_sector():
    load_simple_dim(
        dim_table="dim_economic_sector",
        source_column_names=["Khu vực kinh tế"],
        dest_column="econ_sector_name_vi",
        schema="stats",
    )


def load_dim_economic_type():
    # phòng trường hợp đâu đó vẫn còn 'Loại kình kinh tế'
    load_simple_dim(
        dim_table="dim_economic_type",
        source_column_names=["Loại hình kinh tế"],
        dest_column="econ_type_name_vi",
        schema="stats",
    )


def load_dim_industry():
    load_simple_dim(
        dim_table="dim_industry",
        source_column_names=["Ngành kinh tế"],
        dest_column="industry_name_vi",
        schema="stats",
    )


def load_dim_occupation():
    # bạn nói đã đổi toàn bộ về 'Ngành nghề', nhưng ta cho thêm alias 'Nghề nghiệp' cho chắc
    load_simple_dim(
        dim_table="dim_occupation",
        source_column_names=["Ngành nghề"],
        dest_column="occupation_name_vi",
        schema="stats",
    )


def load_dim_job_status():
    load_simple_dim(
        dim_table="dim_job_status",
        source_column_names=["Vị thế việc làm"],
        dest_column="job_status_name_vi",
        schema="stats",
    )


# 5) dim_province (Tỉnh/thành)

def load_dim_province():
    # --- 1. Đọc file mapping province – region ---
    mapping_file = os.path.join(DATA_DIR, "khuvuc_vung.csv")

    # Đọc file; dùng dtype=str cho chắc, tránh lỗi kiểu số
    df = pd.read_csv(mapping_file, dtype=str)

    # Chuẩn hóa tên cột và khoảng trắng
    df.columns = df.columns.str.strip()

    # Đảm bảo có đủ 2 cột cần thiết
    required_cols = ["Khu vực", "Vùng"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Thiếu cột trong file mapping: {missing}")

    df["Khu vực"] = df["Khu vực"].astype(str).str.strip()
    df["Vùng"] = df["Vùng"].astype(str).str.strip()

    # Chỉ giữ 2 cột Khu vực + Vùng và loại bỏ duplicate
    df = df[["Khu vực", "Vùng"]].drop_duplicates()

    # Đổi tên cho khớp với dim_region và dim_province
    df = df.rename(
        columns={
            "Khu vực": "province_name_vi",
            "Vùng": "region_name_vi",
        }
    )

    # --- 2. Lấy id vùng từ dim_region ---
    with engine.begin() as conn:
        dim_region = pd.read_sql(
            "SELECT region_id, region_name_vi FROM stats.dim_region",
            conn,
        )

    # Join để lấy region_id
    df = df.merge(dim_region, on="region_name_vi", how="left")

    # Kiểm tra những tỉnh chưa map được region_id
    missing_region = df[df["region_id"].isna()]
    if not missing_region.empty:
        print("[WARN] Có tỉnh chưa map được region_id:\n", missing_region)

    # final_df: chỉ còn province_name_vi + region_id
    # Nếu vì lý do nào đó vẫn còn duplicate theo province_name_vi thì lấy 1 dòng đại diện
    final_df = (
        df[["province_name_vi", "region_id"]]
        .drop_duplicates(subset=["province_name_vi"])
    )

    # --- 3. Ghi vào dim_province ---
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE stats.dim_province RESTART IDENTITY CASCADE"))
        final_df.to_sql(
            "dim_province",
            conn,
            schema="stats",
            if_exists="append",
            index=False,
        )

# ==============================
# MAIN
# ==============================

def main():
    load_dim_time()
    load_dim_region()
    load_dim_area_type()
    load_dim_gender()
    load_dim_age_group()
    load_dim_education()
    load_dim_economic_sector()
    load_dim_economic_type()
    load_dim_industry()
    load_dim_occupation()
    load_dim_job_status()
    load_dim_province()


if __name__ == "__main__":
    main()
