# ĐỌC ĐI - QUAN TRỌNG!

## 📌 Cài đặt cho máy mới (chưa có Python)

### CÁCH 1: Đơn giản nhất (Khuyến nghị)

1. **Cài Python trước:**
   - Vào: https://www.python.org/downloads/
   - Tải Python 3.11
   - Cài đặt - NHỚ TÍCH "Add Python to PATH"

2. **Chạy install.bat:**
   - Double-click `install.bat`
   - Đợi cài xong (1-2 phút)

3. **Chạy app:**
   - Double-click `run_app.bat`

### CÁCH 2: Cho người thạo

```bash
# Bước 1: Cài Python từ python.org (nhớ Add to PATH)

# Bước 2: Mở CMD trong folder này
cd "path\to\folder"

# Bước 3: Cài packages
pip install customtkinter openpyxl pillow tkinterdnd2

# Bước 4: Chạy
python customs_extractor_gui.py
```

---

## ❌ TẠI SAO install.bat KHÔNG TỰ TẢI PYTHON?

**Lý do:**
1. Windows PowerShell execution policy thường bị chặn
2. Download Python cần quyền admin
3. User khác nhau cần Python version khác nhau
4. Dễ bị lỗi hơn là hướng dẫn cài manual

**Giải pháp hiện tại:**
- Script chỉ cài pip packages (đơn giản, ít lỗi)
- Hướng dẫn user cài Python trước (reliable hơn)

---

## 🐛 Lỗi thường gặp

### "install.bat không làm gì cả"

**Có thể:**
1. Đang chạy dưới quyền user thường → Chạy "Run as Administrator"
2. Antivirus chặn → Tắt tạm thời
3. PowerShell execution policy → Dùng CMD thay vì PowerShell

**Fix:**
- Right-click `install.bat`
- Chọn "Run as administrator"

### "Python not found"

**Fix:**
1. Cài Python từ python.org
2. Khi cài, NHẤT ĐỊNH tích vào: ☑ "Add Python to PATH"
3. Restart máy
4. Test: Mở CMD, gõ `python --version`

### Chạy từ PowerShell bị lỗi

**Sai:**
```powershell
PS> install.bat
# Lỗi: không recognize
```

**Đúng - từ PowerShell:**
```powershell
PS> cmd /c install.bat
# hoặc
PS> .\install.bat
```

**Hoặc dùng CMD (khuyến nghị):**
```cmd
C:\> install.bat
```

---

## ✅ Checklist debug

Nếu có lỗi, kiểm tra theo thứ tự:

1. [ ] Python đã cài? → `python --version`
2. [ ] Python trong PATH? → Restart CMD và test lại
3. [ ] Có Internet? → ping google.com
4. [ ] Firewall/Antivirus? → Tắt tạm thời
5. [ ] Quyền Admin? → Run as Administrator

---

## 📦 Phân phối

### Cho 1 máy không có Python:

1. Copy toàn bộ folder
2. Hướng dẫn user:
   - Cài Python từ python.org (Add to PATH)
   - Chạy install.bat
   - Chạy run_app.bat

### Cho nhiều máy:

**Option 1: Installer**
- Build .exe: `python build_exe.py`
- Phân phối file `.exe` (không cần Python)

**Option 2: Portable Python**
- Download "Python Embeddable Package"
- Đóng gói cùng dependencies
- Tạo launcher script

---

## 💡 Lưu ý kỹ thuật

**install.bat hiện tại:**
- ✅ Kiểm tra Python có sẵn không
- ✅ Nếu không → Hướng dẫn + mở browser tới trang download
- ✅ Nếu có → Cài pip packages
- ✅ Verify cài đặt
- ❌ KHÔNG tự download Python (tránh execution policy issues)

**Tại sao không dùng PowerShell script?**
- Windows mặc định chặn PowerShell scripts
- Cần `Set-ExecutionPolicy` → Phức tạp với user
- `.bat` đơn giản hơn, luôn chạy được

---

Nếu vẫn gặp vấn đề, chụp màn hình lỗi và liên hệ hỗ trợ.
