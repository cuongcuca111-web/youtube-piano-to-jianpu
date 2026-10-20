# 🎹 JianpuPiano AI - Chuyển đổi YouTube Piano sang Sheet Giản Phổ

Hệ thống ứng dụng Web tự động phân tích và chuyển đổi video Piano trên YouTube sang định dạng **Nhạc Giản Phổ (Jianpu / Numbered Musical Notation)**:
> **Đô = 1, Rê = 2, Mi = 3, Pha = 4, Sol = 5, La = 6, Si = 7**

---

## 🌟 Tính Năng Nổi Bật

1. **Quét Link YouTube Trực Tiếp**:
   - Dán bất kỳ link bài piano nào từ YouTube (ví dụ: `https://www.youtube.com/watch?v=...`).
   - Tự động trích xuất luồng âm thanh và tiêu đề video.

2. **Công Nghệ Đa Tầng (Dual-Engine AI & DSP)**:
   - **Google Gemini Multimodal AI**: Tích hợp mô hình `gemini-2.5-flash` nghe và bóc tách từng cao độ, phách, nhịp và tiết tấu với độ chính xác cao.
   - **CSDL Âm Nhạc & Khớp Bài Hát Mẫu**: Sẵn sàng thử ngay các tác phẩm kinh điển (*Canon in D*, *Für Elise*, *River Flows in You*, *Gặp Mẹ Trong Mơ*, *See You Again*...).
   - **Hỗ trợ tải tệp**: Cho phép kéo thả trực tiếp tệp âm thanh `.mp3`, `.wav`, `.m4a` hoặc tệp `.mid` (MIDI).

3. **Giao Diện Hiển Thị Giản Phổ Chuẩn Quốc Tế**:
   - **Cao độ quãng tám**: Dấu chấm trên đầu (`1̇`, `2̇`) là quãng 8 cao; dấu chấm dưới chân (`1̣`, `2̣`) là quãng 8 trầm.
   - **Trường độ phách**: Nốt ngân dài dùng gạch ngang (`1 -`, `1 - - -`), móc đơn (`1_`), móc kép (`1‗`), nốt chấm dôi (`1.`), dấu lặng (`0`).
   - **Ghi chú nốt chữ bên dưới** (`C4`, `D4`, `E4`...) giúp người mới bắt đầu học đàn dễ dàng đối chiếu.
   - Hỗ trợ xem **Cả 2 tay** (Giai điệu tay phải + Hợp âm tay trái) hoặc **Chỉ tay phải**.

4. **Trình Phát Âm Thanh & Bàn Phím Piano Ảo Đồng Bộ**:
   - Tích hợp động cơ âm thanh Piano mộc thực tế phát ngay trên trình duyệt (Web Audio API) không cần cài thêm phần mềm.
   - Bàn phím Piano 44 phím hiển thị số nốt Giản Phổ tương ứng theo từng Tone (Giọng) và sáng đèn theo thời gian thực khi nốt được phát.
   - Điều chỉnh tốc độ tập đàn (0.75x, 1.0x, 1.25x).

5. **Dịch Giọng / Đổi Tone (Transposition) 1 Click**:
   - Chuyển đổi linh hoạt giữa các giọng `1 = C`, `1 = D`, `1 = E`, `1 = F`, `1 = G`, `1 = A`, `1 = B♭`...

6. **In Ấn & Xuất Bản**:
   - In khổ giấy A4 định dạng chuẩn trang sheet nhạc đẹp mắt.
   - Xuất tệp MIDI (`.mid`) để mở trên MuseScore, Synthesia, GarageBand hoặc FL Studio.
   - Sao chép toàn bộ văn bản Giản Phổ dạng Text để lưu vào Word hoặc Notepad.

---

## 🚀 Hướng Dẫn Khởi Chạy

### Cách 1: Chạy file Batch (trên Windows)
Nhấp đúp chuột vào file:
```
start.bat
```

### Cách 2: Chạy bằng lệnh Python
Mở Terminal trong thư mục dự án và chạy:
```bash
python start.py
```
Hoặc:
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
Trình duyệt sẽ tự động mở trang web tại địa chỉ: **`http://127.0.0.1:8000`**.

---

## 📁 Cấu Trúc Thư Mục Dự Án
```
youtube-piano-to-jianpu/
├── app.py                  # Máy chủ FastAPI & REST API
├── music_engine.py         # Quy tắc nhạc lý Giản Phổ, chuyển đổi MIDI & định dạng text
├── gemini_transcriber.py   # Module AI nghe âm thanh qua Google Gemini
├── sample_database.py      # CSDL các bài piano mẫu chất lượng cao
├── midi_converter.py       # Trình đọc/ghi tệp MIDI chuẩn
├── start.py                # Script khởi động tự động mở trình duyệt
├── start.bat               # File click-to-run trên Windows
├── static/
│   ├── index.html          # Giao diện chính người dùng (Tailwind CSS)
│   ├── app.js              # Xử lý tương tác, Web Audio Synthesizer, bộ đệm phím đàn
│   └── style.css           # Định dạng nốt nhạc Giản Phổ, phím đàn và bản in A4
└── README.md
```
