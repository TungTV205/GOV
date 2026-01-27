# DỰ ÁN GOV

## PHÂN TÍCH DÂN SỐ VÀ THỊ TRƯỜNG LAO ĐỘNG VIỆT NAM GIAI ĐOẠN 2019–2024

---

## 1. BỐI CẢNH & ĐẶT VẤN ĐỀ

Giai đoạn 2019–2024 là một giai đoạn đặc biệt của Việt Nam khi các xu hướng nhân khẩu học và thị trường lao động cùng lúc chịu tác động của nhiều yếu tố mang tính cấu trúc và cú sốc ngắn hạn. Về mặt dân số, Việt Nam vẫn đang nằm trong thời kỳ **“dân số vàng”**, với tỷ trọng dân số trong độ tuổi lao động duy trì ở mức cao – một điều kiện quan trọng cho tăng trưởng kinh tế, mở rộng sản xuất và thu hút đầu tư. Tuy nhiên, song hành với lợi thế đó là những dấu hiệu cho thấy cửa sổ cơ hội này đang dần thu hẹp do mức sinh giảm nhanh, tốc độ già hóa gia tăng và sự thay đổi trong hành vi xã hội của thế hệ trẻ.

Ở khía cạnh thị trường lao động, giai đoạn này chứng kiến những biến động lớn về cả cung và cầu lao động. Đại dịch COVID-19 tạo ra cú sốc nghiêm trọng, làm gián đoạn chuỗi cung ứng lao động và bộc lộ rõ tính dễ tổn thương của các nhóm lao động phi chính thức. Đồng thời, làn sóng chuyển đổi số, tự động hóa và sự phát triển của trí tuệ nhân tạo (AI) đang làm thay đổi cấu trúc ngành nghề, yêu cầu kỹ năng và mức độ bền vững của việc làm, đặc biệt trong các ngành thâm dụng lao động và có khả năng số hóa cao.

Trong bối cảnh đó, việc theo dõi và phân tích mối quan hệ giữa **dân số – lao động – chất lượng việc làm** trở nên cần thiết nhằm đánh giá mức độ tận dụng lợi thế dân số vàng, nhận diện sớm các rủi ro về già hóa, thiếu hụt kỹ năng và an sinh xã hội, từ đó cung cấp cơ sở dữ liệu và luận cứ định lượng cho nghiên cứu và thảo luận chính sách.
---

## 2. MỤC TIÊU NGHIÊN CỨU

Dự án hướng tới các mục tiêu chính sau:

* Phân tích xu hướng và đặc điểm của giai đoạn dân số vàng Việt Nam trong giai đoạn 2019–2024, làm nền tảng để đánh giá cơ hội và thách thức về nguồn nhân lực.
* Mô tả và so sánh các biến động chủ yếu của thị trường lao động trong bối cảnh các cú sốc và thay đổi cấu trúc (đặc biệt là COVID-19 và chuyển đổi số).
* Đánh giá tác động của dân số vàng đến thị trường lao động, tập trung vào thất nghiệp, thiếu việc làm và lao động phi chính thức.
* Làm rõ sự khác biệt và các yếu tố chi phối quá trình chuyển dịch lao động theo ngành, theo khu vực và theo trình độ kỹ năng.
* Xây dựng hệ thống báo cáo trực quan (dashboard) cho phép phân tích đa chiều, hỗ trợ diễn giải xu hướng và rút ra insight phục vụ nghiên cứu.

---

## 3. DỮ LIỆU & PHẠM VI NGHIÊN CỨU

### 3.1. Nguồn dữ liệu

Dữ liệu được thu thập chủ yếu từ:

* Trang web chính thức của **Cục Thống Kê – Bộ Tài chính Việt Nam**.
* Bổ sung từ **Thư Viện Pháp Luật** cho một số chỉ tiêu liên quan.

Tổng cộng dự án sử dụng khoảng **59–65 bảng dữ liệu thống kê**, bao phủ giai đoạn từ năm 2019 đến 2024.

### 3.2. Đặc điểm dữ liệu

Dữ liệu nguồn có đặc thù là các **bảng thống kê dạng cross-tab nhiều tầng**, với nhiều chỉ tiêu được cắt lát theo các chiều phân tích khác nhau. Để phục vụ ETL và phân tích, toàn bộ các bảng nguồn đã được chuẩn hóa thủ công về dạng **bảng phẳng (flat table)** thông qua Excel và Power Query Editor trước khi đưa vào pipeline xử lý tự động.

### 3.3. Nhóm chỉ tiêu chính

* **Dân số**: Quy mô dân số, mật độ, dân số trung bình, tỷ số giới tính, tỷ suất sinh – tử, tăng tự nhiên, tổng tỷ suất sinh (TFR), di cư, tuổi thọ, tỷ lệ biết chữ.
* **Lao động – việc làm**: Lực lượng lao động, số lao động có việc làm, cơ cấu ngành, thất nghiệp, thiếu việc làm, lao động phi chính thức, tỷ lệ qua đào tạo, năng suất lao động.

### 3.4. Nhóm chiều phân tích

Thời gian, địa phương, vùng, giới tính, thành thị/nông thôn, nhóm tuổi, ngành kinh tế, nghề nghiệp, vị thế việc làm, loại hình và khu vực kinh tế, trình độ chuyên môn kỹ thuật.

---

## 4. PHƯƠNG PHÁP & KIẾN TRÚC HỆ THỐNG

Dự án được xây dựng theo hướng **metadata-driven ETL**, trong đó file `data_catalog.csv` đóng vai trò lớp metadata trung tâm, cho phép hệ thống tự động quét, nhận diện và xử lý các bảng dữ liệu nguồn theo đúng grain phân tích.

Do đặc thù dữ liệu thống kê, dự án không sử dụng một fact table duy nhất mà xây dựng **Statistic Data Mart** gồm nhiều bảng fact, mỗi bảng đại diện cho một tập chỉ tiêu có chung chiều phân tích (ví dụ: theo địa phương, theo giới tính, theo nhóm tuổi). Cách tiếp cận này đảm bảo tính toàn vẹn thống kê và tránh việc gộp sai bản chất dữ liệu.

<img width="817" height="237" alt="image" src="https://github.com/user-attachments/assets/74209cde-c714-4044-a7f9-801f1c32bfa7" />
<img width="719" height="402" alt="image" src="https://github.com/user-attachments/assets/00720389-dac9-44c3-8203-07e8c74237c1" />



## 5. PHÂN TÍCH & KẾT QUẢ NGHIÊN CỨU

### 5.1. Xu hướng dân số vàng (Dashboard 1)

Phân tích cho thấy Việt Nam vẫn duy trì lợi thế về **quy mô dân số lớn** (hơn 101 triệu người), song **tốc độ tăng dân số tự nhiên giảm rõ rệt** trong giai đoạn 2019–2024. Đặc biệt, giai đoạn 2021–2022 ghi nhận cú sụt giảm mạnh do tác động của đại dịch COVID-19. Mặc dù có sự phục hồi sau đại dịch, xu hướng dài hạn cho thấy mức sinh tiếp tục suy giảm, với tổng tỷ suất sinh (TFR) chỉ còn khoảng 1,95 vào năm 2024.

Phân tích cơ cấu lực lượng lao động cho thấy nhóm tuổi 25–49 hiện vẫn là lực lượng nòng cốt, nhưng **chỉ số già hóa và tỷ số thay thế tăng nhanh**, phản ánh sự mất cân đối thế hệ ngày càng rõ rệt. Điều này cho thấy cửa sổ dân số vàng vẫn mở, nhưng đang khép lại nhanh chóng.

**<img width="1414" height="800" alt="image" src="https://github.com/user-attachments/assets/4f4bc60a-802c-4f46-9a45-6f9eabc71340" />**

* KPI tổng dân số, TFR.
* Biểu đồ kết hợp Cột/Đường về dân số và tăng tự nhiên.
* Biểu đồ cơ cấu tuổi và chỉ số già hóa lực lượng lao động.

### 5.2. Cơ cấu ngành & chất lượng nguồn nhân lực (Dashboard 2)

Mặc dù tỷ lệ thất nghiệp của Việt Nam ở mức thấp, phân tích sâu cho thấy **chất lượng việc làm còn hạn chế**. Tỷ lệ lao động qua đào tạo thấp trong khi lao động phi chính thức chiếm tỷ trọng rất lớn, phản ánh một thị trường lao động “rộng nhưng nông”.

Cấu trúc nghề nghiệp cho thấy lao động giản đơn vẫn chiếm ưu thế áp đảo, trong khi lao động kỹ năng cao tăng chậm. Phân tích mối quan hệ giữa đào tạo và thu nhập khẳng định đào tạo là yếu tố then chốt giúp nâng cao thu nhập và giảm rủi ro phi chính thức, song phần lớn lao động vẫn bị mắc kẹt trong khu vực đào tạo thấp – thu nhập thấp.

**<img width="1424" height="803" alt="image" src="https://github.com/user-attachments/assets/9086ef0a-7834-4598-b3e7-2674e74bf8c4" />**

* KPI thất nghiệp, qua đào tạo, phi chính thức.
* Biểu đồ cơ cấu nghề và kỹ năng.
* Scatter Plot giữa đào tạo và thu nhập.

### 5.3. Sức khỏe thị trường lao động (Dashboard 3)

Các chỉ số tổng quan cho thấy thị trường lao động Việt Nam có vẻ ổn định sau đại dịch, với lực lượng lao động và số người có việc làm duy trì ở mức cao. Tuy nhiên, phân tích tăng trưởng lực lượng lao động cho thấy **động lực tăng trưởng dựa trên mở rộng số lượng đang chậm lại**, đặc biệt trong năm 2024.

Quá trình chuyển dịch lao động từ nông nghiệp sang công nghiệp và dịch vụ diễn ra đúng hướng nhưng chậm. Đáng chú ý, khu vực lao động tự làm và lao động gia đình vẫn chiếm tỷ trọng lớn, tạo ra khoảng trống an sinh đáng kể. Điều này làm tăng mức độ dễ tổn thương của thị trường lao động trước các cú sốc trong tương lai.

**<img width="1422" height="802" alt="image" src="https://github.com/user-attachments/assets/129de573-77f5-410f-be52-44380e1ed72a" />**

* Biểu đồ tăng trưởng LLLĐ và thất nghiệp.
* Biểu đồ chuyển dịch cơ cấu ngành.
* Treemap vị thế việc làm và biểu đồ tham gia bảo hiểm.

### 5.4. Di cư và đô thị hóa (Dashboard 4)

Phân tích cho thấy đô thị hóa là xu hướng tất yếu, song dòng di cư mang tính phân cực rõ rệt. Một số tỉnh công nghiệp như Bình Dương, Bắc Ninh trở thành điểm đến hấp dẫn lao động, trong khi nhiều tỉnh thuộc Đồng bằng sông Cửu Long chứng kiến tình trạng xuất cư mạnh.

Nguyên nhân cốt lõi của dòng di cư này là **chênh lệch năng suất lao động và thu nhập** giữa các vùng. Chênh lệch năng suất gấp nhiều lần tạo ra lực đẩy kinh tế khiến lao động rời bỏ khu vực nông nghiệp năng suất thấp để tìm đến các trung tâm công nghiệp, kéo theo áp lực hạ tầng tại đô thị và suy giảm nguồn lực tại các vùng xuất cư.

**<img width="1421" height="800" alt="image" src="https://github.com/user-attachments/assets/307ed9ee-6472-441e-99f5-e8817b302080" />**

* Biểu đồ tỷ suất nhập cư – xuất cư.
* Biểu đồ năng suất lao động theo tỉnh.
* Bản đồ phân bố dân số và di cư.

### 5.5. Bảng tra cứu khu vực (Dashboard 5)

* Tra cứu nhanh chỉ số theo tỉnh/thành, vùng miền và năm.
* So sánh đa chỉ tiêu giữa các địa phương trong cùng một màn hình.
* Hỗ trợ drill-down từ tổng thể quốc gia xuống cấp vùng và tỉnh.
**<img width="1423" height="810" alt="image" src="https://github.com/user-attachments/assets/5314e7ad-a2fe-4a85-be96-21be0c9be8db" />**

---

## 6. KẾT LUẬN & HÀM Ý CHÍNH SÁCH

Kết quả phân tích cho thấy Việt Nam vẫn đang trong giai đoạn dân số vàng, nhưng lợi thế này đang suy giảm nhanh chóng do mức sinh thấp và tốc độ già hóa cao. Thị trường lao động tuy ổn định về số lượng, song còn nhiều hạn chế về chất lượng việc làm, kỹ năng và an sinh xã hội.

Nếu không tận dụng hiệu quả giai đoạn 10 năm tới để nâng cao năng suất, chất lượng nguồn nhân lực và mở rộng khu vực việc làm chính thức, Việt Nam có nguy cơ rơi vào bẫy “già trước khi giàu”. Dự án cung cấp một nền tảng dữ liệu và phân tích định lượng, hỗ trợ các cơ quan quản lý, nhà nghiên cứu và cộng đồng quan tâm trong việc theo dõi, đánh giá và đề xuất các giải pháp phù hợp cho phát triển nguồn nhân lực và thị trường lao động trong giai đoạn tới.
