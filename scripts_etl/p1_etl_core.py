# etl_core.py
from typing import List
import pandas as pd
import unicodedata
from sqlalchemy import create_engine
from psycopg2.extras import execute_values
from contextlib import closing

# =========================================================
# CẤU HÌNH KẾT NỐI DB
# =========================================================

DB_URL = "postgresql+psycopg2://postgres:tungpostgresql123@localhost:5432/Gov"

engine = create_engine(DB_URL)


# =========================================================
# HELPER: DIM
# =========================================================

def load_dim(table_name: str) -> pd.DataFrame:
    """
    Đọc toàn bộ 1 bảng dim_xxx trong schema stats.
    """
    query = f"SELECT * FROM stats.{table_name}"
    return pd.read_sql(query, engine)


def normalize_text(s: pd.Series) -> pd.Series:
    """
    Chuẩn hoá text để join.

    Các bước:
      - Ép về string
      - Chuẩn hoá Unicode (NFC)
      - Đổi 'Ð/ð' (ETH) thành 'Đ/đ' tiếng Việt
      - strip + lower

    Dùng cho các cột khóa tự nhiên kiểu text.
    """

    # Đảm bảo là string
    s = s.astype(str)

    # Chuẩn hoá Unicode + thay ETH -> Đ tiếng Việt
    def _normalize_one(x: str) -> str:
        # Chuẩn hoá Unicode dạng NFC
        x = unicodedata.normalize("NFC", x)
        # Đổi ETH (U+00D0 / U+00F0) thành Đ/đ (U+0110 / U+0111)
        x = x.replace("Ð", "Đ").replace("ð", "đ")
        return x

    s = s.map(_normalize_one)

    # Cuối cùng mới strip + lower để chuẩn hoá key
    return s.str.strip().str.lower()


def map_dim_key(
    df_stg: pd.DataFrame,
    dim_table: str,
    stg_col: str,
    dim_nk_col: str,
    dim_id_col: str,
    fact_fk_col: str,
) -> pd.DataFrame:
    """
    Map 1 cột khóa tự nhiên trong staging sang surrogate key từ bảng dim_xxx.

    - df_stg[stg_col] join với stats.dim_table[dim_nk_col]
    - Thêm cột fact_fk_col = dim_id_col
    """
    dim_df = load_dim(dim_table)

    left = df_stg.copy()
    right = dim_df[[dim_id_col, dim_nk_col]].copy()

    left["_join_key"] = normalize_text(left[stg_col])
    right["_join_key"] = normalize_text(right[dim_nk_col])

    merged = left.merge(
        right[["_join_key", dim_id_col]],
        on="_join_key",
        how="left",
    )

    not_mapped = merged[merged[dim_id_col].isna()][[stg_col]].drop_duplicates()
    if not not_mapped.empty:
        print(f"[WARN] Không map được {fact_fk_col} cho các giá trị:")
        print(not_mapped.to_string(index=False))

    merged = merged.drop(columns=["_join_key"])
    merged = merged.rename(columns={dim_id_col: fact_fk_col})

    return merged


# =========================================================
# HELPER: UPSERT FACT
# =========================================================

def upsert_fact(table_name: str, df: pd.DataFrame, grain_cols: List[str]) -> None:
    """
    Upsert vào bảng stats.fact_xxx với ON CONFLICT (grain_cols) DO UPDATE.

    - Tự động drop duplicates theo grain_cols để tránh lỗi
      "ON CONFLICT DO UPDATE command cannot affect row a second time"
    - Kiểm tra range INT32 cho các cột số để tránh
      "psycopg2.errors.NumericValueOutOfRange: integer out of range"

    YÊU CẦU:
      - Trong DB đã có UNIQUE (grain_cols) cho bảng fact đó.
    """

    if df.empty:
        print(f"[INFO] Không có dữ liệu để load vào stats.{table_name}")
        return

    # =====================================================
    # 1) DROP DUPLICATES THEO GRAIN
    # =====================================================
    before = len(df)
    df = df.drop_duplicates(subset=grain_cols, keep="first")
    after = len(df)

    if after < before:
        print(
            f"[WARN] Tự động drop {before - after} dòng trùng key "
            f"({', '.join(grain_cols)}) trong fact {table_name}"
        )

    # =====================================================
    # 2) CHECK RANGE SỐ NGUYÊN (INT32) TRƯỚC KHI INSERT
    # =====================================================
    INT32_MAX = 2_147_483_647
    INT32_MIN = -2_147_483_648

    num_df = df.select_dtypes(include="number")
    if not num_df.empty:
        too_big_mask = num_df > INT32_MAX
        too_small_mask = num_df < INT32_MIN

        has_too_big = bool(too_big_mask.any().any())
        has_too_small = bool(too_small_mask.any().any())

        if has_too_big or has_too_small:
            print(f"[ERROR] Dữ liệu số của fact {table_name} vượt range INTEGER của Postgres:")

            if has_too_big:
                cols_big = too_big_mask.any(axis=0)
                print("  > Cột vượt INT32_MAX và giá trị lớn nhất:")
                print(num_df.loc[:, cols_big].max())

            if has_too_small:
                cols_small = too_small_mask.any(axis=0)
                print("  > Cột nhỏ hơn INT32_MIN và giá trị nhỏ nhất:")
                print(num_df.loc[:, cols_small].min())

            raise ValueError(
                f"Dữ liệu fact {table_name} có giá trị số vượt range INTEGER "
                f"({INT32_MIN}..{INT32_MAX}). Cần xử lý/scale lại trước khi upsert."
            )

    # =====================================================
    # 3) INSERT ... ON CONFLICT
    # =====================================================

    cols = list(df.columns)
    grain_cols = list(grain_cols)

    col_list_sql = ", ".join(cols)
    placeholders = ", ".join([f"%({c})s" for c in cols])

    conflict_cols_sql = ", ".join(grain_cols)
    non_key_cols = [c for c in cols if c not in grain_cols]
    update_assignments = ", ".join(
        f"{c} = EXCLUDED.{c}" for c in non_key_cols
    )

    sql = f"""
        INSERT INTO stats.{table_name} ({col_list_sql})
        VALUES %s
        ON CONFLICT ({conflict_cols_sql})
        DO UPDATE SET
            {update_assignments};
    """

    records = df.to_dict(orient="records")

    with closing(engine.raw_connection()) as conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                sql,
                records,
                template=f"({placeholders})"
            )
        conn.commit()

    print(f"[OK] Upsert {len(df)} dòng vào stats.{table_name}")
