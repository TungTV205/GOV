-- ======================================================
-- A. FK GIỮA CÁC DIM
-- ======================================================

ALTER TABLE stats.dim_province
    ADD CONSTRAINT fk_dim_province_region
        FOREIGN KEY (region_id) REFERENCES stats.dim_region (region_id);


-- ======================================================
-- B. FK TỪ FACT -> DIM
-- ======================================================

-- fact_province_year
ALTER TABLE stats.fact_province_year
    ADD CONSTRAINT fk_fact_province_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_province_year
    ADD CONSTRAINT fk_fact_province_year_province
        FOREIGN KEY (province_id) REFERENCES stats.dim_province (province_id);

-- fact_province_gender_year
ALTER TABLE stats.fact_province_gender_year
    ADD CONSTRAINT fk_fact_province_gender_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_province_gender_year
    ADD CONSTRAINT fk_fact_province_gender_year_province
        FOREIGN KEY (province_id) REFERENCES stats.dim_province (province_id);

ALTER TABLE stats.fact_province_gender_year
    ADD CONSTRAINT fk_fact_province_gender_year_gender
        FOREIGN KEY (gender_id) REFERENCES stats.dim_gender (gender_id);

-- fact_province_area_type_year
ALTER TABLE stats.fact_province_area_type_year
    ADD CONSTRAINT fk_fact_province_area_type_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_province_area_type_year
    ADD CONSTRAINT fk_fact_province_area_type_year_province
        FOREIGN KEY (province_id) REFERENCES stats.dim_province (province_id);

ALTER TABLE stats.fact_province_area_type_year
    ADD CONSTRAINT fk_fact_province_area_type_year_area_type
        FOREIGN KEY (area_type_id) REFERENCES stats.dim_area_type (area_type_id);

-- fact_area_type_year
ALTER TABLE stats.fact_area_type_year
    ADD CONSTRAINT fk_fact_area_type_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_area_type_year
    ADD CONSTRAINT fk_fact_area_type_year_area_type
        FOREIGN KEY (area_type_id) REFERENCES stats.dim_area_type (area_type_id);

-- fact_area_type_region_year
ALTER TABLE stats.fact_area_type_region_year
    ADD CONSTRAINT fk_fact_area_type_region_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_area_type_region_year
    ADD CONSTRAINT fk_fact_area_type_region_year_area_type
        FOREIGN KEY (area_type_id) REFERENCES stats.dim_area_type (area_type_id);

ALTER TABLE stats.fact_area_type_region_year
    ADD CONSTRAINT fk_fact_area_type_region_year_region
        FOREIGN KEY (region_id) REFERENCES stats.dim_region (region_id);

-- fact_gender_year
ALTER TABLE stats.fact_gender_year
    ADD CONSTRAINT fk_fact_gender_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_gender_year
    ADD CONSTRAINT fk_fact_gender_year_gender
        FOREIGN KEY (gender_id) REFERENCES stats.dim_gender (gender_id);

-- fact_gender_region_year
ALTER TABLE stats.fact_gender_region_year
    ADD CONSTRAINT fk_fact_gender_region_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_gender_region_year
    ADD CONSTRAINT fk_fact_gender_region_year_gender
        FOREIGN KEY (gender_id) REFERENCES stats.dim_gender (gender_id);

ALTER TABLE stats.fact_gender_region_year
    ADD CONSTRAINT fk_fact_gender_region_year_region
        FOREIGN KEY (region_id) REFERENCES stats.dim_region (region_id);

-- fact_region_year
ALTER TABLE stats.fact_region_year
    ADD CONSTRAINT fk_fact_region_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_region_year
    ADD CONSTRAINT fk_fact_region_year_region
        FOREIGN KEY (region_id) REFERENCES stats.dim_region (region_id);

-- fact_economic_sector_year
ALTER TABLE stats.fact_economic_sector_year
    ADD CONSTRAINT fk_fact_economic_sector_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_economic_sector_year
    ADD CONSTRAINT fk_fact_economic_sector_year_sector
        FOREIGN KEY (econ_sector_id) REFERENCES stats.dim_economic_sector (econ_sector_id);

-- fact_economic_type_year
ALTER TABLE stats.fact_economic_type_year
    ADD CONSTRAINT fk_fact_economic_type_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_economic_type_year
    ADD CONSTRAINT fk_fact_economic_type_year_type
        FOREIGN KEY (econ_type_id) REFERENCES stats.dim_economic_type (econ_type_id);

-- fact_industry_year
ALTER TABLE stats.fact_industry_year
    ADD CONSTRAINT fk_fact_industry_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_industry_year
    ADD CONSTRAINT fk_fact_industry_year_industry
        FOREIGN KEY (industry_id) REFERENCES stats.dim_industry (industry_id);

-- fact_occupation_year
ALTER TABLE stats.fact_occupation_year
    ADD CONSTRAINT fk_fact_occupation_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_occupation_year
    ADD CONSTRAINT fk_fact_occupation_year_occupation
        FOREIGN KEY (occupation_id) REFERENCES stats.dim_occupation (occupation_id);

-- fact_age_group_year
ALTER TABLE stats.fact_age_group_year
    ADD CONSTRAINT fk_fact_age_group_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_age_group_year
    ADD CONSTRAINT fk_fact_age_group_year_age_group
        FOREIGN KEY (age_group_id) REFERENCES stats.dim_age_group (age_group_id);

-- fact_education_year
ALTER TABLE stats.fact_education_year
    ADD CONSTRAINT fk_fact_education_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_education_year
    ADD CONSTRAINT fk_fact_education_year_edu
        FOREIGN KEY (edu_id) REFERENCES stats.dim_education (edu_id);

-- fact_job_status_year
ALTER TABLE stats.fact_job_status_year
    ADD CONSTRAINT fk_fact_job_status_year_time
        FOREIGN KEY (time_id) REFERENCES stats.dim_time (time_id);

ALTER TABLE stats.fact_job_status_year
    ADD CONSTRAINT fk_fact_job_status_year_status
        FOREIGN KEY (job_status_id) REFERENCES stats.dim_job_status (job_status_id);
