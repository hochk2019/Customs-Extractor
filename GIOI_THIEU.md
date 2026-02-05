# 🚀 Giới Thiệu Phần Mềm Customs Extractor V2

**Customs Extractor V2** là giải pháp phần mềm tự động hóa việc trích xuất danh sách hàng hóa từ các file Excel **Tờ khai Hải quan (Export/Import)**. Công cụ này được thiết kế để giúp nhân viên xuất nhập khẩu tiết kiệm thời gian, giảm thiểu sai sót khi xử lý dữ liệu từ tờ khai.

---

## 🌟 Tính Năng Nổi Bật

### 1. Hỗ Trợ Đa Dạng Tờ Khai
*   **Tờ khai Xuất khẩu (TKX):** Tự động nhận diện và trích xuất thông tin từ các mẫu tờ khai xuất khẩu. Đặc biệt có khả năng tách thông tin **Xuất xứ (Origin)** từ dòng mô tả hàng hóa (ví dụ: `#&VN`).
*   **Tờ khai Nhập khẩu (TKN):** Hỗ trợ trích xuất chi tiết từ tờ khai nhập khẩu, bao gồm cả vị trí các trường dữ liệu đặc thù khác với tờ khai xuất.

### 2. Xử Lý Dữ Liệu Thông Minh
*   **Tự động nhận diện khối dữ liệu:** Thuật toán thông minh quét toàn bộ file Excel để tìm và trích xuất chính xác từng dòng hàng hóa dựa trên Mã HS (HS Code).
*   **Chuẩn hóa định dạng số:** Tự động chuyển đổi định dạng số Việt Nam (ví dụ: `1.000,50` hoặc `1,000.50`) sang định dạng số chuẩn Excel để dễ dàng tính toán (Sum, Average...).
*   **Làm sạch dữ liệu:** Loại bỏ các ký tự thừa, khoảng trắng không cần thiết để file kết quả luôn gọn gàng.

### 3. Giao Diện Người Dùng Hiện Đại (GUI)
*   **Giao diện Tab:** Tách biệt rõ ràng giữa tab **Xuất khẩu** và **Nhập khẩu**, dễ dàng thao tác.
*   **Dark Mode:** Giao diện tối màu hiện đại, giúp giảm mỏi mắt khi làm việc lâu.
*   **Tiến trình trực quan:** Thanh tiến trình (Progress Bar) và Log chi tiết giúp bạn theo dõi từng bước xử lý của phần mềm.

### 4. Tiện Ích Đi Kèm
*   **Tùy chọn linh hoạt:** Cho phép chọn thư mục lưu file kết quả, đặt tên file tùy ý.
*   **Tự động mở file:** Tùy chọn tự động mở file kết quả ngay sau khi trích xuất xong.
*   **Lịch sử:** Ghi nhớ thư mục làm việc gần nhất để tiết kiệm thao tác tìm kiếm.

---

## 💡 Lợi Ích Khi Sử Dụng
*   **Tiết kiệm 90% thời gian** so với việc copy-paste thủ công từng dòng hàng.
*   **Độ chính xác tuyệt đối**, loại bỏ rủi ro sai sót do thao tác tay (nhầm dòng, nhầm cột).
*   **File kết quả chuẩn Excel**, có định dạng đẹp, sẵn sàng để gửi khách hàng hoặc nhập liệu vào hệ thống khác.

---

## 📋 Thông Tin Kỹ Thuật
*   **Ngôn ngữ phát triển:** Python
*   **Xử lý Excel:** Thư viện `openpyxl`, `xlrd` (Hỗ trợ cả `.xls` và `.xlsx`)
*   **Giao diện:** `customtkinter`
*   **Hệ điều hành:** Windows (10/11)
