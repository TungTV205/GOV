# DỰ ÁN GOV

## PHÂN TÍCH DÂN SỐ VÀ THỊ TRƯỜNG LAO ĐỘNG VIỆT NAM  
## GIAI ĐOẠN 2019–2024  
*(Metadata-driven Analytics Project)*

---

## 1. BỐI CẢNH & ĐẶT VẤN ĐỀ

Giai đoạn 2019–2024 là một giai đoạn đặc biệt của Việt Nam khi các xu hướng nhân khẩu học và thị trường lao động đồng thời chịu tác động của các yếu tố mang tính cấu trúc dài hạn và các cú sốc ngắn hạn. Về dân số, Việt Nam vẫn đang trong thời kỳ **“dân số vàng”**, với tỷ trọng dân số trong độ tuổi lao động ở mức cao – một lợi thế quan trọng cho tăng trưởng kinh tế. Tuy nhiên, lợi thế này đang suy giảm nhanh do mức sinh giảm mạnh, tốc độ già hóa tăng nhanh và sự thay đổi trong hành vi xã hội.

Ở khía cạnh thị trường lao động, đại dịch COVID-19 tạo ra cú sốc lớn, làm gián đoạn cung – cầu lao động và bộc lộ rõ tính dễ tổn thương của lao động phi chính thức. Song song đó, quá trình chuyển đổi số và tự động hóa đang làm thay đổi sâu sắc cơ cấu ngành nghề, yêu cầu kỹ năng và chất lượng việc làm.

Trong bối cảnh đó, nhu cầu không chỉ là **phân tích chỉ tiêu đơn lẻ**, mà là xây dựng một **nền tảng dữ liệu có cấu trúc, linh hoạt và có thể mở rộng**, cho phép theo dõi mối quan hệ giữa **dân số – lao động – chất lượng việc làm** một cách nhất quán và có hệ thống.

---

## 2. MỤC TIÊU NGHIÊN CỨU

Dự án hướng tới các mục tiêu chính sau:

- Phân tích xu hướng và đặc điểm của giai đoạn dân số vàng Việt Nam giai đoạn 2019–2024.
- Đánh giá các biến động của thị trường lao động trong bối cảnh COVID-19 và chuyển đổi số.
- Làm rõ mối quan hệ giữa dân số vàng, chất lượng nguồn nhân lực và trạng thái việc làm.
- Phân tích sự khác biệt và chuyển dịch lao động theo ngành, vùng, kỹ năng và vị thế việc làm.
- Xây dựng **hệ thống phân tích dựa trên metadata**, cho phép mở rộng và tái sử dụng dữ liệu hiệu quả.

---

## 3. DỮ LIỆU & PHẠM VI NGHIÊN CỨU

### 3.1. Nguồn dữ liệu

- **Cục Thống Kê – Bộ Tài chính Việt Nam** (nguồn chính)
- **Thư Viện Pháp Luật** (bổ sung một số chỉ tiêu)

Tổng cộng sử dụng khoảng **59–65 bảng thống kê**, bao phủ giai đoạn 2019–2024.

### 3.2. Đặc thù dữ liệu nguồn

Dữ liệu nguồn mang đặc trưng của **thống kê chính thức**:

- Các bảng đã **được tổng hợp sẵn**, không phải dữ liệu vi mô
- Mỗi bảng là một **lát cắt (slice)** theo một hoặc nhiều chiều phân tích
- Grain không đồng nhất giữa các bảng

Để phục vụ phân tích và tự động hóa xử lý, toàn bộ dữ liệu được chuẩn hóa thủ công về **bảng phẳng (flat table)** trước khi đưa vào pipeline.

---

## 4. PHƯƠNG PHÁP & KIẾN TRÚC HỆ THỐNG  
### 4.1. Metadata-driven ETL

Trọng tâm kỹ thuật của dự án là cách tiếp cận **metadata-driven ETL**, trong đó metadata không chỉ dùng để mô tả dữ liệu mà đóng vai trò **điều phối toàn bộ pipeline xử lý**.

File `data_catalog.csv` được sử dụng như một **lớp metadata trung tâm**, lưu trữ thông tin về:

- Tên file dữ liệu nguồn
- Danh sách trường dữ liệu
- Số dòng, số cột
- Các chiều phân tích hiện diện trong từng bảng
- Grain thống kê của bảng

Python script đọc metadata này để:
- Tự động quét và phân loại các bảng theo **grain chung**
- Nhận diện các bảng có thể **merge thành cùng một fact**
- Tránh việc gộp dữ liệu sai bản chất thống kê
- Load dữ liệu vào đúng bảng fact và dimension trong cơ sở dữ liệu phân tích

Cách tiếp cận này giúp xử lý hiệu quả bài toán **nhiều bảng tổng hợp – nhiều grain**, vốn rất phổ biến trong dữ liệu thống kê nhà nước.

---

### 4.2. Mô hình dữ liệu phân tích

Thay vì xây dựng một fact table duy nhất, dự án triển khai **Statistic Data Mart**, gồm:

- Nhiều bảng **fact theo nhóm chỉ tiêu**
- Mỗi fact đại diện cho một grain thống kê cụ thể
- Các bảng dimension dùng chung (thời gian, địa phương, giới tính, ngành, kỹ năng…)

Cách thiết kế này:
- Đảm bảo **tính toàn vẹn thống kê**
- Tránh cộng gộp sai chỉ tiêu
- Phù hợp với phân tích mô tả và so sánh xu hướng

<img width="817" height="237" src="https://github.com/user-attachments/assets/74209cde-c714-4044-a7f9-801f1c32bfa7" />
<img width="719" height="402" src="https://github.com/user-attachments/assets/00720389-dac9-44c3-8203-07e8c74237c1" />

---

## 5. PHÂN TÍCH & KẾT QUẢ

*(Phần dashboard và phân tích giữ nguyên nội dung như phiên bản hiện tại, tập trung vào insight và diễn giải chính sách.)*

---

## 6. KẾT LUẬN

Dự án cho thấy Việt Nam vẫn đang trong giai đoạn dân số vàng, nhưng lợi thế này đang suy giảm nhanh chóng. Thị trường lao động ổn định về quy mô nhưng còn nhiều hạn chế về chất lượng việc làm, kỹ năng và an sinh.

Bên cạnh các kết quả phân tích, dự án còn minh họa cách **metadata có thể được sử dụng như một công cụ phân tích và thiết kế hệ thống dữ liệu**, không chỉ đơn thuần là tài liệu mô tả. Cách tiếp cận metadata-driven giúp đảm bảo tính nhất quán, khả năng mở rộng và tái sử dụng cho các dự án phân tích dữ liệu thống kê trong tương lai.
