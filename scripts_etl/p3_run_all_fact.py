# run_all.py
from etl_from_catalog import etl_all_facts_from_catalog

DATA_DIR = r"D:\Data Project\GOV\data_source"       # thư mục chứa ~56 file csv
CATALOG_PATH = r"D:\Data Project\GOV\data_source\data_catalog.csv"  # file data_catalog.csv

if __name__ == "__main__":
    etl_all_facts_from_catalog(
        data_dir=DATA_DIR,
        catalog_path=CATALOG_PATH,
    )
