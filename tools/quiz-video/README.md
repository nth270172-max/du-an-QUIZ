# Máy dựng video quiz (tools/quiz-video)

- `render.py` — ảnh gợi ý tạm (procedural) + bản dựng 1 (đơn giản). Giữ lại để lấy hàm `clue_img`.
- `render2.py` — bản dựng 2: bố cục chuẩn kênh quiz (4 đáp án A/B/C/D, trượt vào, timer phát sáng, pháo giấy, thanh tiến độ). Chạy: `python3 render2.py video2.mp4`.
- `audio2.py` — tách giọng đọc theo khoảng lặng (12 đoạn), đặt vào mốc, thêm tích tắc, ding, nhạc nền sinh bằng mã, ghép thành `quiz-mau-v2.mp4`. Cần `voice.mp3` cùng thư mục.

Thay ảnh Flow: đặt 5 ảnh 980×600 và sửa `CLUES` trong `render2.py` để nạp từ file thay vì `clue_img`.
Phông: Inter (đã có trên máy dựng). Màu khuôn: nền #0E163A→#261650, vàng #FFCD46, xanh #40DC78.
