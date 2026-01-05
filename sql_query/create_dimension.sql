-- ======================================================
-- 0. TẠO SCHEMA
-- ======================================================
CREATE SCHEMA IF NOT EXISTS stats;

-- ======================================================
-- 1. DIM THỜI GIAN
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_time (
    time_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year         integer NOT NULL,          -- cột 'Năm'
    year_label   text    NOT NULL,          -- ví dụ '2019'
    CONSTRAINT uq_dim_time_year UNIQUE (year)
);

-- ======================================================
-- 2. DIM VÙNG (REGION)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_region (
    region_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    region_name_vi text NOT NULL,    -- ví dụ: 'Đồng bằng sông Hồng'
    region_code    text,             -- nếu sau này có mã vùng
    CONSTRAINT uq_dim_region_name UNIQUE (region_name_vi)
);

-- ======================================================
-- 3. DIM LOẠI KHU VỰC (AREA TYPE: THÀNH THỊ / NÔNG THÔN)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_area_type (
    area_type_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    area_type_name_vi text NOT NULL,  -- 'Thành thị', 'Nông thôn'
    CONSTRAINT uq_dim_area_type_name UNIQUE (area_type_name_vi)
);

-- ======================================================
-- 4. DIM TỈNH/THÀNH (PROVINCE)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_province (
    province_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    province_name_vi text NOT NULL,    -- tên tỉnh/thành
    province_code    text,             -- mã tỉnh (nếu có)
    region_id        integer,          -- FK -> stats.dim_region(region_id)
    CONSTRAINT uq_dim_province_name UNIQUE (province_name_vi)
);

-- ======================================================
-- 5. DIM GIỚI TÍNH
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_gender (
    gender_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    gender_name_vi text NOT NULL,    -- 'Nam', 'Nữ'
    CONSTRAINT uq_dim_gender_name UNIQUE (gender_name_vi)
);

-- ======================================================
-- 6. DIM NHÓM TUỔI
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_age_group (
    age_group_id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    age_group_label_vi  text NOT NULL,   -- ví dụ '15-24'
    CONSTRAINT uq_dim_age_group_label UNIQUE (age_group_label_vi)
);

-- ======================================================
-- 7. DIM TRÌNH ĐỘ HỌC VẤN
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_education (
    edu_id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    edu_level_vi  text NOT NULL,    -- từ cột 'Trình độ'
    CONSTRAINT uq_dim_education_level UNIQUE (edu_level_vi)
);

-- ======================================================
-- 8. DIM KHU VỰC KINH TẾ
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_economic_sector (
    econ_sector_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    econ_sector_name_vi text NOT NULL,   -- từ 'Khu vực kinh tế'
    econ_sector_code    text,
    CONSTRAINT uq_dim_econ_sector_name UNIQUE (econ_sector_name_vi)
);

-- ======================================================
-- 9. DIM LOẠI HÌNH KINH TẾ
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_economic_type (
    econ_type_id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    econ_type_name_vi   text NOT NULL,   -- từ 'Loại hình kinh tế'
    econ_type_code      text,            -- nếu sau này có mã
    CONSTRAINT uq_dim_econ_type_name UNIQUE (econ_type_name_vi)
);

-- ======================================================
-- 10. DIM NGÀNH KINH TẾ
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_industry (
    industry_id        integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    industry_name_vi   text NOT NULL,   -- từ 'Ngành kinh tế'
    CONSTRAINT uq_dim_industry_name UNIQUE (industry_name_vi)
);

-- ======================================================
-- 11. DIM NGÀNH NGHỀ
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_occupation (
    occupation_id       integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    occupation_name_vi  text NOT NULL,   -- từ 'Ngành nghề'
    CONSTRAINT uq_dim_occupation_name UNIQUE (occupation_name_vi)
);

-- ======================================================
-- 12. DIM VỊ THẾ VIỆC LÀM
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.dim_job_status (
    job_status_id      integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    job_status_name_vi text NOT NULL,   -- từ 'Vị thế việc làm'
    CONSTRAINT uq_dim_job_status_name UNIQUE (job_status_name_vi)
);
