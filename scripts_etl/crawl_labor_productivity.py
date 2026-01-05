import json
import sys
import requests
import pandas as pd
from io import StringIO

CANDIDATE_API_URLS = [
    # Thử NSO trước
    "https://pxweb.nso.gov.vn/pxweb/api/v1/vi/D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng/D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng/V02.58.px",
    # Thử GSO
    "https://pxweb.gso.gov.vn/pxweb/api/v1/vi/D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng/D%C3%A2n%20s%E1%BB%91%20v%C3%A0%20lao%20%C4%91%E1%BB%99ng/V02.58.px",
]

def get_metadata(url: str) -> dict:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    return r.json()

def pick_var(meta: dict, keywords: list[str]) -> str:
    # PxWeb metadata thường có meta["variables"] với fields: code, text, values, valueTexts
    for v in meta.get("variables", []):
        text = (v.get("text") or "").lower()
        if all(k.lower() in text for k in keywords):
            return v["code"]
    # fallback: tìm theo code gần đúng
    for v in meta.get("variables", []):
        code = (v.get("code") or "").lower()
        if any(k.lower() in code for k in keywords):
            return v["code"]
    raise ValueError(f"Không tìm thấy biến với keywords={keywords}")

def download_csv(url: str, years=("2023","2024")) -> pd.DataFrame:
    meta = get_metadata(url)
    year_code = pick_var(meta, ["năm"])
    # địa phương có thể là "Địa phương" hoặc "Tỉnh, thành phố"
    try:
        geo_code = pick_var(meta, ["địa"])
    except Exception:
        geo_code = pick_var(meta, ["tỉnh"])

    # lấy danh sách value codes hợp lệ
    var_map = {v["code"]: v for v in meta["variables"]}
    year_values = set(var_map[year_code]["values"])
    geo_values = list(var_map[geo_code]["values"])  # chọn tất cả địa phương

    chosen_years = [y for y in years if y in year_values]
    if len(chosen_years) == 0:
        raise ValueError(f"Không thấy năm {years} trong bảng. Năm hiện có: {sorted(year_values)[:10]}...")

    query = {
        "query": [
            {"code": geo_code, "selection": {"filter": "item", "values": geo_values}},
            {"code": year_code, "selection": {"filter": "item", "values": chosen_years}},
        ],
        "response": {"format": "CSV"}
    }

    r = requests.post(url, json=query, timeout=180)
    r.raise_for_status()

    # PxWeb CSV đôi khi có BOM/encoding khác; cố đọc linh hoạt
    text = r.text
    df = pd.read_csv(StringIO(text))
    return df

last_err = None
for API_URL in CANDIDATE_API_URLS:
    try:
        df = download_csv(API_URL)
        out = "nang_suat_lao_dong_theo_tinh_2023_2024.csv"
        df.to_csv(out, index=False, encoding="utf-8-sig")
        print(f"OK: đã lưu {out} (rows={len(df):,}) từ {API_URL}")
        sys.exit(0)
    except Exception as e:
        last_err = (API_URL, e)

print("Không tải được từ các candidate URLs.")
print("Lỗi gần nhất:", last_err[0], "-", repr(last_err[1]))
sys.exit(1)
