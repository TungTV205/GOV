-- ======================================================
-- 13. FACT: TỈNH/THÀNH × NĂM
--    Gom tất cả các bảng dạng: Khu vực, Năm, ...
--    (danso_khuvuc, matdodanso_khuvuc..., laodongcovieclam_khuvuc,
--     lucluonglaodong_khuvuc, nangsuatlaodong_khuvuc, tuoitho_khuvuc,
--     tyledansobietchu_khuvuc, tylelaodongdaquadaotao_khuvuc,
--     tylelaodongvieclamphichinhthuc_khuvuc, tyletangdanso_khuvuc,
--     tylethatnghiep_khuvuc, tylethieuvieclam_khuvuc, tysogioitinh_khuvuc,
--     tysuatdicuthuan_khuvuc_..., tysuatsinh_khuvuc,
--     tyletangtunhien_khuvuc_...)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_province_year (
    fact_id                bigserial PRIMARY KEY,
    time_id                integer NOT NULL,
    province_id            integer NOT NULL,

    population             numeric, -- Dân số
    area                   numeric, -- Diện tích
    population_density     numeric, -- Mật độ dân số

    employed               numeric, -- Lao động có việc làm
    labor_force            numeric, -- Lực lượng lao động
    labor_productivity     numeric, -- Năng suất lao động

    life_expectancy        numeric, -- Tuổi thọ
    literacy_rate          numeric, -- Tỷ lệ dân số biết chữ
    trained_labor_rate     numeric, -- Tỷ lệ lao động đã qua đào tạo
    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức

    population_growth_rate numeric, -- Tỷ lệ tăng dân số
    unemployment_rate      numeric, -- Tỷ lệ thất nghiệp
    underemployment_rate   numeric, -- Tỷ lệ thiếu việc làm

    sex_ratio              numeric, -- Tỷ số giới tính

    immigration_rate       numeric, -- Tỷ suất nhập cư
    emigration_rate        numeric, -- Tỷ suất xuất cư
    net_migration_rate     numeric, -- Tỷ suất di cư thuần

    tfr             	   numeric, -- Tổng tỷ suất sinh
    crude_birth_rate       numeric, -- Tỷ suất sinh thô
    crude_death_rate       numeric, -- Tỷ suất chết thô
    natural_increase_rate  numeric, -- Tỷ lệ tăng tự nhiên

    CONSTRAINT uq_fact_province_year UNIQUE (time_id, province_id)
);

-- ======================================================
-- 14. FACT: TỈNH/THÀNH × GIỚI TÍNH × NĂM
--    (danso_khuvuc_gioitinh)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_province_gender_year (
    fact_id       bigserial PRIMARY KEY,
    time_id       integer NOT NULL,
    province_id   integer NOT NULL,
    gender_id     integer NOT NULL,

    population    numeric,  -- Dân số

    CONSTRAINT uq_fact_province_gender_year
        UNIQUE (time_id, province_id, gender_id)
);

-- ======================================================
-- 15. FACT: TỈNH/THÀNH × LOẠI KHU VỰC × NĂM
--    (danso_khuvuc_loaikhuvuc)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_province_area_type_year (
    fact_id        bigserial PRIMARY KEY,
    time_id        integer NOT NULL,
    province_id    integer NOT NULL,
    area_type_id   integer NOT NULL,

    population     numeric, -- Dân số

    CONSTRAINT uq_fact_province_area_type_year
        UNIQUE (time_id, province_id, area_type_id)
);

-- ======================================================
-- 16. FACT: LOẠI KHU VỰC × NĂM (TOÀN QUỐC)
--    (tuoitho_loaikhuvuc, lucluonglaodong_loaikhuvuc,
--     solaodongcovieclam_loaikhuvuc, tyledansobietchu_loaikhuvuc,
--     tylelaodongvieclamphichinhthuc_loaikhuvuc, tysogioitinh_loaikhuvuc,
--     tysuatsinh_loaikhuvuc, tyletangtunhien_loaikhuvuc_...)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_area_type_year (
    fact_id                 bigserial PRIMARY KEY,
    time_id                 integer NOT NULL,
    area_type_id            integer NOT NULL,

    life_expectancy         numeric, -- Tuổi thọ
    labor_force             numeric, -- Lực lượng lao động
    employed                numeric, -- Số lao động có việc làm
    literacy_rate           numeric, -- Tỷ lệ biết chữ
    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức
    sex_ratio               numeric, -- Tỷ số giới tính
    trained_labor_rate		numeric,

    tfr		                numeric, -- Tổng tỷ suất sinh
    crude_birth_rate        numeric, -- Tỷ suất sinh thô
    crude_death_rate        numeric, -- Tỷ suất chết thô
    natural_increase_rate   numeric, -- Tỷ lệ tăng tự nhiên

    CONSTRAINT uq_fact_area_type_year
        UNIQUE (time_id, area_type_id)
);

-- ======================================================
-- 17. FACT: LOẠI KHU VỰC × VÙNG × NĂM
--    (tylethatnghiep_loaikhuvuc_vung, tylethieuvieclam_loaikhuvuc_vung)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_area_type_region_year (
    fact_id               bigserial PRIMARY KEY,
    time_id               integer NOT NULL,
    area_type_id          integer NOT NULL,
    region_id             integer NOT NULL,

    unemployment_rate     numeric, -- Tỷ lệ thất nghiệp
    underemployment_rate  numeric, -- Tỷ lệ thiếu việc làm

    CONSTRAINT uq_fact_area_type_region_year
        UNIQUE (time_id, area_type_id, region_id)
);

-- ======================================================
-- 18. FACT: GIỚI TÍNH × NĂM (TOÀN QUỐC)
--    (tuoitho_gioitinh, lucluonglaodong_gioitinh,
--     solaodongcovieclam_gioitinh,
--     tylelaodongdaquadaotao_gioitinh,
--     tylelaodongvieclamphichinhthuc_gioitinh)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_gender_year (
    fact_id                  bigserial PRIMARY KEY,
    time_id                  integer NOT NULL,
    gender_id                integer NOT NULL,

    life_expectancy          numeric, -- Tuổi thọ
    labor_force              numeric, -- Lực lượng lao động
    employed                 numeric, -- Số lao động có việc làm
    trained_labor_rate       numeric, -- Tỷ lệ LĐ đã qua đào tạo
    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức

    CONSTRAINT uq_fact_gender_year
        UNIQUE (time_id, gender_id)
);

-- ======================================================
-- 19. FACT: GIỚI TÍNH × VÙNG × NĂM
--    (tylethieuvieclam_gioitinh_vung)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_gender_region_year (
    fact_id               bigserial PRIMARY KEY,
    time_id               integer NOT NULL,
    gender_id             integer NOT NULL,
    region_id             integer NOT NULL,

    underemployment_rate  numeric, -- Tỷ lệ thiếu việc làm

    CONSTRAINT uq_fact_gender_region_year
        UNIQUE (time_id, gender_id, region_id)
);

-- ======================================================
-- 20. FACT: VÙNG × NĂM
--    (tuoitho_vung, tysogioitinh_vung)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_region_year (
    fact_id          bigserial PRIMARY KEY,
    time_id          integer NOT NULL,
    region_id        integer NOT NULL,

    life_expectancy  numeric, -- Tuổi thọ
    sex_ratio        numeric, -- Tỷ số giới tính

    CONSTRAINT uq_fact_region_year
        UNIQUE (time_id, region_id)
);

-- ======================================================
-- 21. FACT: KHU VỰC KINH TẾ × NĂM
--    (tylelaodongvieclamphichinhthuc_khuvuckinhte,
--     tylethieuvieclam_khuvuckinhte)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_economic_sector_year (
    fact_id                  bigserial PRIMARY KEY,
    time_id                  integer NOT NULL,
    econ_sector_id           integer NOT NULL,

    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức
    underemployment_rate     numeric, -- Tỷ lệ thiếu việc làm

    CONSTRAINT uq_fact_economic_sector_year
        UNIQUE (time_id, econ_sector_id)
);

-- ======================================================
-- 22. FACT: LOẠI HÌNH KINH TẾ × NĂM
--    (solaodongcovieclam_loaihinhkinhte,
--     tylethieuvieclam_loaikinhkinhte)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_economic_type_year (
    fact_id              bigserial PRIMARY KEY,
    time_id              integer NOT NULL,
    econ_type_id         integer NOT NULL,

    employed             numeric, -- Số lao động có việc làm
    underemployment_rate numeric, -- Tỷ lệ thiếu việc làm

    CONSTRAINT uq_fact_economic_type_year
        UNIQUE (time_id, econ_type_id)
);

-- ======================================================
-- 23. FACT: NGÀNH KINH TẾ × NĂM
--    (nangsuatlaodong_nganhkinhte,
--     solaodongcovieclam_nganhkinhte,
--     tylelaodongvieclamdaquadaotao_nganhkinhte)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_industry_year (
    fact_id                 bigserial PRIMARY KEY,
    time_id                 integer NOT NULL,
    industry_id             integer NOT NULL,

    labor_productivity      numeric, -- Năng suất lao động
    employed                numeric, -- Số lao động có việc làm
    trained_labor_rate   numeric, -- Tỷ lệ LĐ việc làm đã qua đào tạo

    CONSTRAINT uq_fact_industry_year
        UNIQUE (time_id, industry_id)
);

-- ======================================================
-- 24. FACT: NGÀNH NGHỀ × NĂM
--    (solaodongcovieclam_nganhnghe,
--     tylelaodongvieclamphichinhthuc_nganhnghe)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_occupation_year (
    fact_id                  bigserial PRIMARY KEY,
    time_id                  integer NOT NULL,
    occupation_id            integer NOT NULL,

    employed                 numeric, -- Số lao động có việc làm
    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức

    CONSTRAINT uq_fact_occupation_year
        UNIQUE (time_id, occupation_id)
);

-- ======================================================
-- 25. FACT: NHÓM TUỔI × NĂM
--    (lucluonglaodong_nhomtuoi, solaodongcovieclam_nhomtuoi,
--     tylelaodongdaquadaotao_nhomtuoi,
--     tylelaodongvieclamphichinhthuc_nhomtuoi,
--     tylethatnghiep_nhomtuoi, tylethieuvieclam_nhomtuoi)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_age_group_year (
    fact_id                  bigserial PRIMARY KEY,
    time_id                  integer NOT NULL,
    age_group_id             integer NOT NULL,

    labor_force              numeric, -- Lực lượng lao động
    employed                 numeric, -- Số lao động có việc làm
    trained_labor_rate       numeric, -- Tỷ lệ LĐ đã qua đào tạo
    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức
    unemployment_rate        numeric, -- Tỷ lệ thất nghiệp
    underemployment_rate     numeric, -- Tỷ lệ thiếu việc làm

    CONSTRAINT uq_fact_age_group_year
        UNIQUE (time_id, age_group_id)
);

-- ======================================================
-- 26. FACT: TRÌNH ĐỘ × NĂM
--    (tylelaodongdaquadaotao_trinhdo,
--     tylelaodongvieclamphichinhthuc_trinhdo,
--     tylethieuvieclam_trinhdo)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_education_year (
    fact_id                  bigserial PRIMARY KEY,
    time_id                  integer NOT NULL,
    edu_id                   integer NOT NULL,

    trained_labor_rate       numeric, -- Tỷ lệ LĐ đã qua đào tạo
    informal_employment_rate numeric, -- Tỷ lệ LĐ việc làm phi chính thức
    underemployment_rate     numeric, -- Tỷ lệ thiếu việc làm

    CONSTRAINT uq_fact_education_year
        UNIQUE (time_id, edu_id)
);

-- ======================================================
-- 27. FACT: VỊ THẾ VIỆC LÀM × NĂM
--    (solaodongcovieclam_vithevieclam)
-- ======================================================
CREATE TABLE IF NOT EXISTS stats.fact_job_status_year (
    fact_id        bigserial PRIMARY KEY,
    time_id        integer NOT NULL,
    job_status_id  integer NOT NULL,

    employed       numeric, -- Số lao động có việc làm

    CONSTRAINT uq_fact_job_status_year
        UNIQUE (time_id, job_status_id)
);
