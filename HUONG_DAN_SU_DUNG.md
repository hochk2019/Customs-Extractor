# 📖 Hướng Dẫn Sử Dụng Customs Extractor V2
**Customs Extractor V2** là giải pháp phần mềm tự động hóa việc trích xuất danh sách hàng hóa từ các file Excel **Tờ khai Hải quan (Export/Import)**. Công cụ này được thiết kế để giúp nhân viên xuất nhập khẩu tiết kiệm thời gian, giảm thiểu sai sót khi xử lý dữ liệu từ tờ khai.

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

---

Tài liệu này hướng dẫn chi tiết cách cài đặt và sử dụng phần mềm trích xuất dữ liệu tờ khai hải quan.

---

## 🛠️ Phần 1: Cài Đặt (Chỉ làm lần đầu)

Nếu máy tính bạn chưa cài đặt môi trường, hãy làm theo các bước sau:

1.  **Cài đặt Python:**
    *   Tải Python tại: [python.org](https://www.python.org/downloads/)
    *   Khi cài đặt, **BẮT BUỘC** tích vào ô `Add Python to PATH`.
2.  **Cài đặt thư viện:**
    *   Vào thư mục chứa phần mềm.
    *   Double-click (nhấn đúp) vào file `install.bat`.
    *   Đợi màn hình đen chạy xong và báo thành công.

*(Xem chi tiết tại file `HUONG_DAN_CAI_DAT.md` nếu gặp lỗi)*

---

## 🚀 Phần 2: Khởi Động Phần Mềm

1.  Tìm file `run_app_v2.bat` trong thư mục phần mềm.
2.  Nhấn đúp chuột vào file này.
3.  Giao diện phần mềm sẽ hiện lên với tiêu đề **"Trích xuất dữ liệu Tờ khai Hải quan V2"**.

---

## 💻 Phần 3: Thao Tác Trích Xuất Dữ Liệu

Giao diện phần mềm có 2 tab chính: **TK Xuất khẩu** và **TK Nhập khẩu**. Tùy vào loại tờ khai bạn đang xử lý mà chọn tab phù hợp.

### Bước 1: Chọn Tab
*   Click vào Tab **"TK Xuất khẩu"** nếu xử lý hàng xuất.
*   Click vào Tab **"TK Nhập khẩu"** nếu xử lý hàng nhập.

### Bước 2: Chọn File Đầu Vào
1.  Tại mục **"File Excel [xuất/nhập] khẩu"**, bấm nút `Browse`.
2.  Tìm và chọn file Excel tờ khai (`.xls` hoặc `.xlsx`) bạn muốn trích xuất.
3.  *Mẹo: Bạn có thể dùng nút `Recent ▼` (Sắp ra mắt) để chọn nhanh các file vừa làm việc.*

### Bước 3: Cấu Hình Đầu Ra (Tùy chọn)
Phần mềm tự động điền các thông số mặc định, nhưng bạn có thể thay đổi:
*   **Thư mục đầu ra:** Mặc định lưu cùng chỗ với file đầu vào. Bấm `Browse` nếu muốn lưu chỗ khác.
*   **Tên file đầu ra:** Bạn có thể đổi tên file kết quả tại ô `Tên file đầu ra`.

### Bước 4: Thực Thi
1.  Bấm nút to màu xanh **"⚡ Extract Data"**.
2.  **Quan sát:** Thanh tiến trình sẽ chạy và phần "Log" bên dưới sẽ hiện chi tiết các bước (Tìm thấy bao nhiêu dòng hàng, đang ghi dòng nào...).

### Bước 5: Kiểm Tra Kết Quả
*   Khi hoàn thành 100%, thông báo **"Thành công"** sẽ hiện ra.
*   Nếu bạn tích chọn `Tự động mở file sau khi extract`, file Excel kết quả sẽ tự động mở lên.
*   Mở file và kiểm tra các cột: `Mô tả`, `Xuất xứ`, `HS Code`, `Số lượng`, `Đơn giá`,...

---

## ⚙️ Tùy Chọn Nâng Cao
Tại mục **"Tùy chọn chung"** ở dưới cùng:
*   **☑ Tự động mở file...**: Bật tính năng này để không phải mất công tìm file sau khi xong.
*   **☑ Hiển thị preview...**: (Tính năng sắp có) Xem trước dữ liệu trước khi xuất.
*   **☑ Tự động cập nhật thư mục...**: Khi chọn file đầu vào mới, thư mục đầu ra sẽ tự đổi theo.

---

## ❓ Câu Hỏi Thường Gặp (FAQ)

**Q: Tại sao bấm Extract mà báo lỗi?**
A: Hãy kiểm tra file Excel đầu vào. Có thể file đang bị lỗi format hoặc đang được mở bởi chương trình khác. Hãy đóng file Excel đó lại trước khi chạy phần mềm.

**Q: Cột số lượng/giá trị bị sai định dạng?**
A: Phần mềm đã tự động xử lý. Nếu vẫn sai, kiểm tra xem máy tính của bạn đang dùng dấu phẩy (`,`) hay chấm (`.`) để ngăn cách hàng nghìn.

**Q: Cột "Xuất xứ" ở hàng xuất khẩu bị trống?**
A: Phần mềm tìm xuất xứ dựa trên quy tắc `#&[MãNước]` trong dòng mô tả (VD: `#&VN`). Nếu tờ khai không ghi theo quy tắc này, phần mềm sẽ không nhận diện được.

---
**Cần hỗ trợ?** Đọc file cấu hình `config.py` để chỉnh các thiết lập sâu hơn hoặc liên hệ đội ngũ phát triển.
