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

### Vai trò và tầm quan trọng của Metadata trong dữ liệu thống kê chính thức

Dữ liệu thống kê do Cục Thống Kê công bố có đặc thù khác biệt so với dữ liệu giao dịch hoặc dữ liệu vi mô. Phần lớn các bảng dữ liệu là **dữ liệu đã được tổng hợp sẵn**, trong đó cùng một chỉ tiêu (metric) có thể được trình bày dưới dạng nhiều bảng khác nhau, mỗi bảng là một **lát cắt (slice)** theo một hoặc nhiều chiều phân tích riêng biệt.

Ví dụ, cùng là chỉ tiêu **thất nghiệp**, nhưng tồn tại các bảng:
- Thất nghiệp theo tỉnh/thành
- Thất nghiệp theo trình độ chuyên môn
- Thất nghiệp theo giới tính và vùng
- Thất nghiệp theo nhóm tuổi hoặc khu vực kinh tế

Các bảng này:
- Có **chung metric**
- Nhưng **khác grain phân tích**
- Không thể gộp thủ công hoặc gộp tùy ý mà không làm sai bản chất thống kê

Trong bối cảnh đó, **metadata trở thành yếu tố then chốt** để:
- Nhận diện chính xác **grain thống kê** của từng bảng
- Phân biệt các bảng có thể kết hợp và các bảng cần được tách riêng
- Tránh việc cộng gộp sai chỉ tiêu (double counting hoặc aggregation mismatch)
- Đảm bảo mỗi bảng fact phản ánh đúng một cấu trúc phân tích nhất quán

Thay vì coi metadata chỉ là tài liệu mô tả, dự án này sử dụng metadata như một **lớp logic trung gian**, giúp hệ thống:
- Hiểu được mối quan hệ giữa các bảng dữ liệu tổng hợp
- Tự động hóa quá trình phân loại và tổ chức dữ liệu
- Duy trì tính toàn vẹn thống kê trong toàn bộ pipeline phân tích

Cách tiếp cận này đặc biệt phù hợp với dữ liệu thống kê nhà nước, nơi trọng tâm không nằm ở khối lượng dữ liệu lớn mà ở **độ đúng của grain và ngữ cảnh phân tích**.

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

## 5. PHÂN TÍCH & KẾT QUẢ NGHIÊN CỨU 

### 5.1. Xu hướng dân số vàng (Dashboard 1) 

Phân tích cho thấy Việt Nam vẫn duy trì lợi thế về 
**quy mô dân số lớn** (hơn 101 triệu người), song **tốc độ tăng dân số tự nhiên giảm rõ rệt** trong giai đoạn 2019–2024. Đặc biệt, giai đoạn 2021–2022 ghi nhận cú sụt giảm mạnh do tác động của đại dịch COVID-19. Mặc dù có sự phục hồi sau đại dịch, xu hướng dài hạn cho thấy mức sinh tiếp tục suy giảm, với tổng tỷ suất sinh (TFR) chỉ còn khoảng 1,95 vào năm 2024. 
Phân tích cơ cấu lực lượng lao động cho thấy nhóm tuổi 25–49 hiện vẫn là lực lượng nòng cốt, nhưng **chỉ số già hóa và tỷ số thay thế tăng nhanh**, phản ánh sự mất cân đối thế hệ ngày càng rõ rệt. Điều này cho thấy cửa sổ dân số vàng vẫn mở, nhưng đang khép lại nhanh chóng. 

**<img width="1414" height="800" alt="image" src="https://github.com/user-attachments/assets/4f4bc60a-802c-4f46-9a45-6f9eabc71340" />** 


### 5.2. Cơ cấu ngành & chất lượng nguồn nhân lực (Dashboard 2) 

Mặc dù tỷ lệ thất nghiệp của Việt Nam ở mức thấp, phân tích sâu cho thấy **chất lượng việc làm còn hạn chế**. Tỷ lệ lao động qua đào tạo thấp trong khi lao động phi chính thức chiếm tỷ trọng rất lớn, phản ánh một thị trường lao động “rộng nhưng nông”. 
Cấu trúc nghề nghiệp cho thấy lao động giản đơn vẫn chiếm ưu thế áp đảo, trong khi lao động kỹ năng cao tăng chậm. Phân tích mối quan hệ giữa đào tạo và thu nhập khẳng định đào tạo là yếu tố then chốt giúp nâng cao thu nhập và giảm rủi ro phi chính thức, song phần lớn lao động vẫn bị mắc kẹt trong khu vực đào tạo thấp – thu nhập thấp. 

**<img width="1424" height="803" alt="image" src="https://github.com/user-attachments/assets/9086ef0a-7834-4598-b3e7-2674e74bf8c4" />** 

### 5.3. Sức khỏe thị trường lao động (Dashboard 3) 

Các chỉ số tổng quan cho thấy thị trường lao động Việt Nam có vẻ ổn định sau đại dịch, với lực lượng lao động và số người có việc làm duy trì ở mức cao. Tuy nhiên, phân tích tăng trưởng lực lượng lao động cho thấy **động lực tăng trưởng dựa trên mở rộng số lượng đang chậm lại**, đặc biệt trong năm 2024. 
Quá trình chuyển dịch lao động từ nông nghiệp sang công nghiệp và dịch vụ diễn ra đúng hướng nhưng chậm. Đáng chú ý, khu vực lao động tự làm và lao động gia đình vẫn chiếm tỷ trọng lớn, tạo ra khoảng trống an sinh đáng kể. Điều này làm tăng mức độ dễ tổn thương của thị trường lao động trước các cú sốc trong tương lai. 

**<img width="1422" height="802" alt="image" src="https://github.com/user-attachments/assets/129de573-77f5-410f-be52-44380e1ed72a" />** 

### 5.4. Di cư và đô thị hóa (Dashboard 4) 
Phân tích cho thấy đô thị hóa là xu hướng tất yếu, song dòng di cư mang tính phân cực rõ rệt. Một số tỉnh công nghiệp như Bình Dương, Bắc Ninh trở thành điểm đến hấp dẫn lao động, trong khi nhiều tỉnh thuộc Đồng bằng sông Cửu Long chứng kiến tình trạng xuất cư mạnh. 
Nguyên nhân cốt lõi của dòng di cư này là **chênh lệch năng suất lao động và thu nhập** giữa các vùng. Chênh lệch năng suất gấp nhiều lần tạo ra lực đẩy kinh tế khiến lao động rời bỏ khu vực nông nghiệp năng suất thấp để tìm đến các trung tâm công nghiệp, kéo theo áp lực hạ tầng tại đô thị và suy giảm nguồn lực tại các vùng xuất cư. 

**<img width="1421" height="800" alt="image" src="https://github.com/user-attachments/assets/307ed9ee-6472-441e-99f5-e8817b302080" />** 

### 5.5. Bảng tra cứu khu vực (Dashboard 5) 
* Tra cứu nhanh chỉ số theo tỉnh/thành, vùng miền và năm.
* So sánh đa chỉ tiêu giữa các địa phương trong cùng một màn hình.
* Hỗ trợ drill-down từ tổng thể quốc gia xuống cấp vùng và tỉnh.

**<img width="1423" height="810" alt="image" src="https://github.com/user-attachments/assets/5314e7ad-a2fe-4a85-be96-21be0c9be8db" />**

---

## 6. KẾT LUẬN

Dự án cho thấy Việt Nam vẫn đang trong giai đoạn dân số vàng, nhưng lợi thế này đang suy giảm nhanh chóng. Thị trường lao động ổn định về quy mô nhưng còn nhiều hạn chế về chất lượng việc làm, kỹ năng và an sinh.

Bên cạnh các kết quả phân tích, dự án còn minh họa cách **metadata có thể được sử dụng như một công cụ phân tích và thiết kế hệ thống dữ liệu**, không chỉ đơn thuần là tài liệu mô tả. Cách tiếp cận metadata-driven giúp đảm bảo tính nhất quán, khả năng mở rộng và tái sử dụng cho các dự án phân tích dữ liệu thống kê trong tương lai.
