BEGIN;

-- 1) Thêm cột econ_sector_id vào dim.industry
ALTER TABLE dim.industry
ADD COLUMN IF NOT EXISTS econ_sector_id INT;

-- 2) Update econ_sector_id theo mapping 3 khu vực:
-- 1 = Công nghiệp - Xây dựng
-- 2 = Dịch vụ
-- 3 = Nông, lâm nghiệp và thủy sản
UPDATE dim.industry i
SET econ_sector_id = m.econ_sector_id
FROM (
    VALUES
      ('Bán buôn và bán lẻ; sửa chữa ô tô, mô tô, xe máy và xe có động cơ khác', 2),
      ('Cung cấp nước; hoạt động quản lý và xử lý rác thải, nước thải', 1),
      ('Công nghiệp chế biến, chế tạo', 1),
      ('Dịch vụ lưu trú và ăn uống', 2),
      ('Giáo dục và đào tạo', 2),
      ('Hoạt động chuyên môn, khoa học và công nghệ', 2),
      ('Hoạt động của Đảng Cộng sản, tổ chức chính trị - xã hội; quản lý Nhà nước, an ninh quốc phòng; đảm bảo xã hội bắt buộc', 2),
      ('Hoạt động dịch vụ khác', 2),
      ('Hoạt động hành chính và dịch vụ hỗ trợ', 2),
      ('Hoạt động kinh doanh bất động sản', 2),
      ('Hoạt động làm thuê các công việc trong các hộ gia đình, sản xuất sản phẩm vật chất và dịch vụ tiêu dùng của hộ gia đình', 2),
      ('Hoạt động tài chính, ngân hàng và bảo hiểm', 2),
      ('Khai khoáng', 1),
      ('Nghệ thuật, vui chơi và giải trí', 2),
      ('Nông nghiệp, lâm nghiệp và thủy sản', 3),
      ('Sản xuất và phân phối điện, khí đốt, nước nóng, hơi nước và điều hòa không khí', 1),
      ('Thông tin và truyền thông', 2),
      ('Vận tải, kho bãi', 2),
      ('Xây dựng', 1),
      ('Y tế và hoạt động trợ giúp xã hội', 2)
) AS m(industry_name_vi, econ_sector_id)
WHERE i.industry_name_vi = m.industry_name_vi;

-- Tạo index để join/filter nhanh hơn
CREATE INDEX IF NOT EXISTS ix_dim_industry_econ_sector_id
ON dim.industry (econ_sector_id);

-- 3) Tạo khóa ngoại tới dim.economic_sector(econ_sector_id)
ALTER TABLE dim.industry
ADD CONSTRAINT fk_dim_industry_econ_sector
FOREIGN KEY (econ_sector_id)
REFERENCES dim.economic_sector (econ_sector_id);

COMMIT;
