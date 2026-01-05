# etl_from_catalog.py

import os
import pandas as pd

from p1_etl_core import (
    map_dim_key,
    upsert_fact,
)
from mapping_columns import normalize_column_name

# =========================================================
# 1. META DIM & FACT
# =========================================================

# 1.1. Khóa tự nhiên của từng DIM (cột NK trong DIM – tiếng Anh)
DIM_NK_MAP = {
    "dim_time": "year",
    "dim_region": "region_name_vi",
    "dim_area_type": "area_type_name_vi",
    "dim_province": "province_name_vi",
    "dim_gender": "gender_name_vi",
    "dim_age_group": "age_group_label_vi",
    "dim_education": "edu_level_vi",
    "dim_economic_sector": "econ_sector_name_vi",
    "dim_economic_type": "econ_type_name_vi",
    "dim_industry": "industry_name_vi",
    "dim_occupation": "occupation_name_vi",
    "dim_job_status": "job_status_name_vi",
}

# 1.2. Tên ID (PK) của từng DIM
DIM_PK_MAP = {
    "dim_time": "time_id",
    "dim_region": "region_id",
    "dim_area_type": "area_type_id",
    "dim_province": "province_id",
    "dim_gender": "gender_id",
    "dim_age_group": "age_group_id",
    "dim_education": "edu_id",
    "dim_economic_sector": "econ_sector_id",
    "dim_economic_type": "econ_type_id",
    "dim_industry": "industry_id",
    "dim_occupation": "occupation_id",
    "dim_job_status": "job_status_id",
}

# map ngược: id -> dim_table
ID_TO_DIM = {pk: dim for dim, pk in DIM_PK_MAP.items()}


# 1.3. META FACT – danh sách DIM ID + MEASURE (tiếng Anh)
FACT_META = {
    "fact_province_year": {
        "dims": ["time_id", "province_id"],
        "measures": [
            "population",
            "area",
            "population_density",
            "employed",
            "labor_force",
            "labor_productivity",
            "life_expectancy",
            "literacy_rate",
            "trained_labor_rate",
            "informal_employment_rate",
            "population_growth_rate",
            "unemployment_rate",
            "underemployment_rate",
            "sex_ratio",
            "immigration_rate",
            "emigration_rate",
            "net_migration_rate",
            "tfr",
            "crude_birth_rate",
            "crude_death_rate",
            "natural_increase_rate",
        ],
    },
    "fact_province_gender_year": {
        "dims": ["time_id", "province_id", "gender_id"],
        "measures": ["population"],
    },
    "fact_province_area_type_year": {
        "dims": ["time_id", "province_id", "area_type_id"],
        "measures": ["population"],
    },
    "fact_area_type_year": {
        "dims": ["time_id", "area_type_id"],
        "measures": [
            "life_expectancy",
            "labor_force",
            "employed",
            "literacy_rate",
            "informal_employment_rate",
            "sex_ratio",
            "trained_labor_rate",
            "tfr",
            "crude_birth_rate",
            "crude_death_rate",
            "natural_increase_rate",
            
        ],
    },
    "fact_area_type_region_year": {
        "dims": ["time_id", "area_type_id", "region_id"],
        "measures": [
            "unemployment_rate",
            "underemployment_rate",
        ],
    },
    "fact_gender_year": {
        "dims": ["time_id", "gender_id"],
        "measures": [
            "life_expectancy",
            "labor_force",
            "employed",
            "trained_labor_rate",
            "informal_employment_rate",
        ],
    },
    "fact_gender_region_year": {
        "dims": ["time_id", "gender_id", "region_id"],
        "measures": [
            "underemployment_rate",
        ],
    },
    "fact_region_year": {
        "dims": ["time_id", "region_id"],
        "measures": [
            "life_expectancy",
            "sex_ratio",
        ],
    },
    "fact_economic_sector_year": {
        "dims": ["time_id", "econ_sector_id"],
        "measures": [
            "informal_employment_rate",
            "underemployment_rate",
        ],
    },
    "fact_economic_type_year": {
        "dims": ["time_id", "econ_type_id"],
        "measures": [
            "employed",
            "underemployment_rate",
        ],
    },
    "fact_industry_year": {
        "dims": ["time_id", "industry_id"],
        "measures": [
            "labor_productivity",
            "employed",
            "trained_labor_rate",
        ],
    },
    "fact_occupation_year": {
        "dims": ["time_id", "occupation_id"],
        "measures": [
            "employed",
            "informal_employment_rate",
        ],
    },
    "fact_age_group_year": {
        "dims": ["time_id", "age_group_id"],
        "measures": [
            "labor_force",
            "employed",
            "trained_labor_rate",
            "informal_employment_rate",
            "unemployment_rate",
            "underemployment_rate",
        ],
    },
    "fact_education_year": {
        "dims": ["time_id", "edu_id"],
        "measures": [
            "trained_labor_rate",
            "informal_employment_rate",
            "underemployment_rate",
        ],
    },
    "fact_job_status_year": {
        "dims": ["time_id", "job_status_id"],
        "measures": [
            "employed",
        ],
    },
}


# =========================================================
# 2. ĐỌC DATA_CATALOG & CHUẨN HOÁ TÊN CỘT
# =========================================================

def load_catalog(catalog_path: str) -> pd.DataFrame:
    """
    Đọc file data_catalog.csv của Anh.

    File thực tế có các cột:
      - table_name
      - num_rows
      - num_columns
      - column_names   (chuỗi tên cột tiếng Việt, phân tách dấu phẩy)

    Hàm sẽ tạo:
      - column_list_vn: list tên cột tiếng Việt
      - column_list_en: list tên cột tiếng Anh sau khi normalize_column_name
    """
    cat = pd.read_csv(catalog_path)

    # chuẩn hóa tên cột
    cat.columns = [c.strip().lower() for c in cat.columns]

    # map column_names -> columns (nếu cần)
    if "column_names" in cat.columns and "columns" not in cat.columns:
        cat = cat.rename(columns={"column_names": "columns"})

    if "table_name" not in cat.columns or "columns" not in cat.columns:
        raise ValueError(
            f"data_catalog.csv phải có cột 'table_name' và 'columns/column_names', hiện tại: {set(cat.columns)}"
        )

    cat["table_name"] = cat["table_name"].astype(str).str.strip()

    def parse_vn_columns(s: str):
        if pd.isna(s):
            return []
        return [c.strip() for c in str(s).split(",") if c.strip()]

    cat["column_list_vn"] = cat["columns"].apply(parse_vn_columns)
    cat["column_list_en"] = cat["column_list_vn"].apply(
        lambda lst: [normalize_column_name(c) for c in lst]
    )

    return cat


# =========================================================
# 3. XÁC ĐỊNH CẤU HÌNH NGUỒN CHO 1 FACT
# =========================================================

def get_fact_config_from_catalog(
    fact_table: str,
    data_dir: str,
    catalog_path: str,
    file_ext: str = ".csv",
):
    """
    Xác định nguồn dữ liệu cho 1 fact_table (VD: fact_age_group_year).

    Dựa trên:
      - FACT_META: dim_id + measure tiếng Anh cho fact đó
      - DIM_NK_MAP + ID_TO_DIM: map dim_id -> dim_table -> NK (EN)
      - data_catalog.csv: cho biết mỗi file CSV có những cột tiếng Việt nào,
        sau đó được đổi sang EN bằng mapping_columns.normalize_column_name

    Kết quả:
      - dim_info: list( (dim_id_col, dim_table, dim_nk_col) )
      - nk_cols_en: list tên cột grain EN trong CSV (year, province_name_vi, ...)
      - all_measures: list measure EN cho fact
      - source_tables: list dict cho từng bảng nguồn:
            {
                "table_name": ... (không có .csv),
                "csv_path": ...,
                "nk_cols_en": [...],
                "measure_cols_en": [...],
            }
    """
    if fact_table not in FACT_META:
        raise ValueError(f"FACT_META không có cấu hình cho fact_table = {fact_table}")

    fact_def = FACT_META[fact_table]
    dim_id_cols = fact_def["dims"]
    all_measures = list(fact_def["measures"])

    # 3.1. lấy thông tin dim: dim_id -> dim_table -> dim_nk_col
    dim_info = []
    nk_cols_en = []

    for dim_id in dim_id_cols:
        if dim_id not in ID_TO_DIM:
            raise ValueError(f"ID_TO_DIM không có mapping cho dim_id {dim_id}")
        dim_table = ID_TO_DIM[dim_id]
        if dim_table not in DIM_NK_MAP:
            raise ValueError(f"DIM_NK_MAP không có NK cho dim_table {dim_table}")
        dim_nk_col = DIM_NK_MAP[dim_table]
        dim_info.append((dim_id, dim_table, dim_nk_col))
        nk_cols_en.append(dim_nk_col)

    nk_cols_set = set(nk_cols_en)

    # 3.2. tìm bảng nguồn phù hợp trong catalog
    catalog = load_catalog(catalog_path)

    source_tables = []

    for _, row in catalog.iterrows():
        table_name = row["table_name"]
        cols_en = row["column_list_en"]
        cols_en_set = set(cols_en)

        # phải chứa đủ tất cả các cột grain EN (VD: year + province_name_vi)
        if not nk_cols_set.issubset(cols_en_set):
            continue

        # --- RULE ĐẶC BIỆT CHO fact_province_year ---
        # Bỏ các bảng có grain chi tiết hơn: tỉnh + NĂM + GIỚI TÍNH / LOẠI KHU VỰC
        # tương ứng với:
        #   - danso_khuvuc_gioitinh.csv  -> fact_province_gender_year
        #   - danso_khuvuc_loaikhuvuc.csv-> fact_province_area_type_year
        if fact_table == "fact_province_year":
            lower_name = table_name.lower()
            if "_gioitinh" in lower_name or "_loaikhuvuc" in lower_name:
                continue

        # tìm các measure EN của fact nằm trong bảng này
        measures_here = sorted(list(set(all_measures).intersection(cols_en_set)))
        if not measures_here:
            # bảng này không đóng góp measure nào cho fact => bỏ
            continue

        csv_path = os.path.join(data_dir, table_name)
        # nếu data_catalog liệt kê "xxx.csv" thì Anh có thể để data_dir trỏ tới thư mục đó luôn
        # hoặc nếu chỉ là "xxx" thì có thể cần nối file_ext
        if not os.path.exists(csv_path) and file_ext:
            csv_path_ext = os.path.join(data_dir, table_name + file_ext)
            if os.path.exists(csv_path_ext):
                csv_path = csv_path_ext

        source_tables.append(
            {
                "table_name": table_name,
                "csv_path": csv_path,
                "nk_cols_en": nk_cols_en,
                "measure_cols_en": measures_here,
            }
        )

    if not source_tables:
        print(f"[WARN] Không tìm được bảng nguồn nào cho fact {fact_table} trong data_catalog")
    else:
        print(
            f"[INFO] Fact {fact_table} dùng {len(source_tables)} bảng nguồn: "
            + ", ".join(t["table_name"] for t in source_tables)
        )

    return dim_info, nk_cols_en, all_measures, source_tables



# =========================================================
# 4. ETL 1 FACT DỰA TRÊN CATALOG + MAPPING
# =========================================================

def etl_one_fact_from_catalog(
    fact_table: str,
    data_dir: str,
    catalog_path: str,
    file_ext: str = ".csv",
):
    """
    Quy trình ETL cho 1 bảng fact:

      1. Xác định:
         - các dim_id (time_id, province_id, ...)
         - các cột NK EN (year, province_name_vi, ...)
         - các measure EN (population, labor_force, ...)
         - các bảng nguồn phù hợp (chứa đủ NK + measure tương ứng)

      2. Đọc từng CSV:
         - rename cột tiếng Việt -> tiếng Anh bằng normalize_column_name
         - chọn các cột cần: NK + measure
         - merge dần vào staging trên NK

      3. Map từ NK EN sang dim_id bằng map_dim_key

      4. Chọn các cột ID + measure, ép numeric, upsert vào stats.fact_xxx
    """
    from pandas.api.types import is_string_dtype

    if fact_table not in FACT_META:
        print(f"[WARN] Bỏ qua {fact_table}: không có trong FACT_META")
        return

    dim_info, nk_cols_en, all_measures, source_tables = get_fact_config_from_catalog(
        fact_table=fact_table,
        data_dir=data_dir,
        catalog_path=catalog_path,
        file_ext=file_ext,
    )

    if not source_tables:
        return

    # =========================
    # WARN: measure thiếu nguồn
    # =========================
    covered_measures = set()
    for t in source_tables:
        covered_measures |= set(t.get("measure_cols_en", []))

    missing_measures = set(all_measures) - covered_measures
    if missing_measures:
        print(
            f"[WARN] Fact {fact_table} thiếu nguồn cho measures: {sorted(missing_measures)}"
        )

    # =========================================
    # Helper: normalize NK values (Ð/Đ, NBSP...)
    # =========================================
    def _normalize_nk_values(df_in: pd.DataFrame, nk_cols: list[str]) -> pd.DataFrame:
        df_out = df_in.copy()

        for c in nk_cols:
            if c not in df_out.columns:
                continue

            # normalize text NK
            if is_string_dtype(df_out[c]):
                df_out[c] = (
                    df_out[c]
                    .astype(str)
                    .str.replace("Ð", "Đ", regex=False)
                    .str.replace("\u00A0", " ", regex=False)  # NBSP -> space
                    .str.strip()
                )

            # normalize year if present
            if c == "year":
                df_out[c] = pd.to_numeric(df_out[c], errors="coerce").astype("Int64")

        return df_out

    # ==================================================
    # 4.1. Đọc & merge các file nguồn theo grain NK (EN)
    #      FIX: merge có coalesce khi trùng measure
    # ==================================================
    stg = None

    for src in source_tables:
        csv_path = src["csv_path"]
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Không tìm thấy file: {csv_path}")

        df = pd.read_csv(csv_path)

        # rename toàn bộ cột VN -> EN bằng mapping_columns.normalize_column_name
        df = df.rename(columns={c: normalize_column_name(c) for c in df.columns})

        usecols = list(set(src["nk_cols_en"] + src["measure_cols_en"]))
        missing = [c for c in usecols if c not in df.columns]
        if missing:
            raise KeyError(
                f"File {csv_path} thiếu các cột (sau khi rename sang EN) {missing}"
            )

        df = df[usecols]

        # normalize NK values để join/map DIM không bị rụng
        df = _normalize_nk_values(df, nk_cols_en)

        if stg is None:
            stg = df
        else:
            # detect overlap measures (không tính NK)
            overlap = [
                c for c in df.columns
                if (c in stg.columns) and (c not in nk_cols_en)
            ]

            # merge và suffix phần trùng
            stg = stg.merge(df, on=nk_cols_en, how="outer", suffixes=("", "_new"))

            # coalesce: ưu tiên stg[c], thiếu thì lấy stg[c_new]
            for c in overlap:
                new_col = f"{c}_new"
                if new_col in stg.columns:
                    stg[c] = stg[c].combine_first(stg[new_col])
                    stg = stg.drop(columns=[new_col])

    # WARN: nếu vẫn còn cột nhân bản (để bắt lỗi sớm)
    dup_cols = [
        c for c in stg.columns
        if c.endswith("_x") or c.endswith("_y") or c.endswith("_new")
    ]
    if dup_cols:
        print(
            f"[WARN] Fact {fact_table} có cột bị nhân bản do merge: "
            f"{dup_cols[:20]}{'...' if len(dup_cols) > 20 else ''}"
        )

    # =========================
    # 4.2. Map DIM: từ NK EN -> ID
    # =========================
    for dim_id, dim_table, dim_nk_col in dim_info:
        if dim_nk_col not in stg.columns:
            raise KeyError(
                f"Staging cho fact {fact_table} không có cột NK {dim_nk_col} để map sang {dim_id}"
            )

        stg = map_dim_key(
            df_stg=stg,
            dim_table=dim_table,
            stg_col=dim_nk_col,      # cột EN trong staging
            dim_nk_col=dim_nk_col,   # cột EN trong DIM
            dim_id_col=dim_id,
            fact_fk_col=dim_id,
        )

    dim_id_cols = [d[0] for d in dim_info]

    # ==================================
    # 4.3. Chuẩn bị DataFrame để upsert
    #      (đảm bảo đủ tất cả measures)
    # ==================================
    for m in all_measures:
        if m in stg.columns:
            continue

        # fallback: nếu lỡ còn _x/_y thì coalesce để cứu dữ liệu
        mx, my = f"{m}_x", f"{m}_y"
        if mx in stg.columns and my in stg.columns:
            print(f"[WARN] Fact {fact_table}: coalesce {mx}/{my} -> {m}")
            stg[m] = stg[mx].combine_first(stg[my])
        elif mx in stg.columns:
            print(f"[WARN] Fact {fact_table}: dùng {mx} -> {m}")
            stg[m] = stg[mx]
        elif my in stg.columns:
            print(f"[WARN] Fact {fact_table}: dùng {my} -> {m}")
            stg[m] = stg[my]
        else:
            stg[m] = pd.NA

    fact_cols = dim_id_cols + all_measures
    fact_df = stg[fact_cols].copy()

    # ép numeric measures
    for m in all_measures:
        fact_df[m] = pd.to_numeric(fact_df[m], errors="coerce")

    # WARN: duplicate grain sau merge/map (nếu có)
    dup_grain = fact_df.duplicated(subset=dim_id_cols).sum()
    if dup_grain:
        print(f"[WARN] Fact {fact_table}: có {dup_grain} dòng trùng grain {dim_id_cols}")

    # =========================
    # 4.4. Upsert
    # =========================
    upsert_fact(
        table_name=fact_table,
        df=fact_df,
        grain_cols=dim_id_cols,
    )


# =========================================================
# 5. CHẠY TẤT CẢ FACT
# =========================================================

def etl_all_facts_from_catalog(
    data_dir: str,
    catalog_path: str,
):
    """
    Chạy ETL cho tất cả fact trong FACT_META.
    """
    for fact_table in sorted(FACT_META.keys()):
        print("=" * 80)
        print(f"ĐANG ETL FACT: {fact_table}")
        print("=" * 80)
        etl_one_fact_from_catalog(
            fact_table=fact_table,
            data_dir=data_dir,
            catalog_path=catalog_path,
        )
