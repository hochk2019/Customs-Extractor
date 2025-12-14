# 🚀 Hướng dẫn cài đặt nhanh - Customs Extractor

## ⚡ Cài đặt trong 2 bước

### Bước 1: Cài Python (nếu chưa có)

1. **Download Python:**
   - Truy cập: https://www.python.org/downloads/
   - Click "Download Python 3.11" (hoặc version mới hơn)

2. **Cài đặt Python:**
   - Chạy file `.exe` vừa tải
   - ⚠️ **QUAN TRỌNG**: Tích vào ☑ **"Add Python to PATH"**
   - Click "Install Now"
   - Đợi cài đặt hoàn tất (2-3 phút)

3. **Kiểm tra:**
   - Mở Command Prompt (cmd)
   - Gõ: `python --version`
   - Nếu hiện "Python 3.x.x" → OK ✅

### Bước 2: Chạy file cài đặt

1. **Double-click** file `install.bat`
2. Đợi script tự động cài các thư viện (1-2 phút)
3. Thấy "CAI DAT HOAN THANH!" → Xong! ✅

---

## 📱 Chạy ứng dụng

**Double-click** file `run_app.bat`

hoặc

Mở cmd và gõ:
```bash
python customs_extractor_gui.py
```

---

## ❗ Xử lý lỗi

### Lỗi: "Python not found"

**Nguyên nhân:** Python chưa cài hoặc chưa thêm vào PATH

**Giải pháp:**
1. Cài lại Python
2. Nhớ tích ☑ "Add Python to PATH"
3. Restart máy (optional)

### Lỗi: "install.bat không chạy được"

**Nếu chạy từ PowerShell:**
```powershell
# ĐÚNG - từ PowerShell
cmd /c install.bat

# ĐÚNG - từ PowerShell  
.\install.bat

# SAI - không chạy được
install.bat
```

**Khuyến nghị:** Dùng CMD thay vì PowerShell

### Lỗi: "Co loi khi cai dat"

**Nguyên nhân:** Không có Internet

**Giải pháp:**
1. Kiểm tra kết nối Internet
2. Tắt firewall/antivirus tạm thời
3. Chạy lại `install.bat`

---

## 🎯 Checklist cài đặt

- [ ] Python 3.11+ đã cài
- [ ] Python đã thêm vào PATH
- [ ] Đã chạy `install.bat` thành công
- [ ] Tất cả thư viện hiện [OK]
- [ ] Chạy `run_app.bat` thành công

---

## 💡 Tips

1. **Dành cho IT/người thạo:**
   ```bash
   pip install customtkinter openpyxl pillow tkinterdnd2
   python customs_extractor_gui.py
   ```

2. **Dành cho người mới:**
   - Chỉ cần double-click `install.bat`
   - Rồi double-click `run_app.bat`

3. **Nếu cài nhiều máy:**
   - Cài Python 1 lần
   - Copy folder này sang máy khác
   - Chạy `install.bat` trên mỗi máy

---

## 📞 Hỗ trợ

**Vấn đề thường gặp:**

| Vấn đề | Giải pháp |
|--------|-----------|
| Python not found | Cài Python + Add to PATH |
| pip not found | Cài lại Python, tích "Include pip" |
| Permission denied | Chạy cmd/install.bat với quyền Admin |
| No Internet | Kiểm tra mạng, tắt firewall |

---

**Lưu ý:** Script `install.bat` đã được đơn giản hóa - chỉ cài packages, không tự download Python. Bạn cần cài Python thủ công trước.
