---
title: Video mẫu gig Quiz — "Guess the Animal" 60 giây
type: production
created: 2026-10-26
updated: 2026-10-26
tags: [fiverr, gig, quiz, video-mau, ai33, flow]
---

# Video mẫu gig Quiz — "Can You Guess the Animal?" (60 giây, 16:9)

**Mục đích:** video gig trên Fiverr. Không cần hay, cần **đúng chuẩn kênh quiz**: nhịp đều, chữ to, timer rõ, reveal gọn.
**Khuôn:** 5 câu × 10 giây = 50 giây + mở 5 giây + kết 5 giây. Ảnh gợi ý câu hỏi là ảnh **cận cảnh một phần con vật** (mắt, lông, chân) để người xem đoán.

## 1. Bảng thời gian

| Mốc | Khối | Hình | Chữ trên màn | Giọng ai33 |
|---|---|---|---|---|
| 0:00–0:05 | Mở | Nền tối, 5 ảnh con vật lướt nhanh | CAN YOU GUESS THE ANIMAL? · 5 QUESTIONS | Đoạn A |
| 0:05–0:15 | Câu 1 | Cận cảnh mắt mèo | QUESTION 1 · timer 5s → reveal: CAT | Đoạn B1, B1r |
| 0:15–0:25 | Câu 2 | Cận cảnh lông vằn hổ | QUESTION 2 · timer → TIGER | B2, B2r |
| 0:25–0:35 | Câu 3 | Cận cảnh móng guốc dê núi trên đá | QUESTION 3 · timer → MOUNTAIN GOAT | B3, B3r |
| 0:35–0:45 | Câu 4 | Cận cảnh mắt cú | QUESTION 4 · timer → OWL | B4, B4r |
| 0:45–0:55 | Câu 5 | Cận cảnh da voi và ngà | QUESTION 5 · timer → ELEPHANT | B5, B5r |
| 0:55–1:00 | Kết | Bảng điểm 0–5 | HOW MANY DID YOU GET? · SUBSCRIBE FOR MORE | Đoạn C |

Mỗi câu 10 giây = hỏi 2s + đếm ngược 5s (tiếng tích tắc) + reveal 3s (tiếng "ding" + tên con vật bật lên).

## 2. Văn bản cho ai33 (chia sẵn từng file, giọng nam hoặc nữ, nhịp vừa, hào hứng)

| Mã | Văn bản | Thời lượng mục tiêu |
|---|---|---|
| A | Can you guess the animal from just one clue? Five questions. Five seconds each. Let's go! | ≤5s |
| B1 | Question one. Whose eye is this? | 2s |
| B1r | It's a cat! | 1,5s |
| B2 | Question two. Whose stripes are these? | 2s |
| B2r | A tiger! | 1,5s |
| B3 | Question three. Who stands on hooves like these? | 2s |
| B3r | A mountain goat! | 1,5s |
| B4 | Question four. Whose eye is watching you? | 2s |
| B4r | An owl! | 1,5s |
| B5 | Question five. Whose skin is this? | 2s |
| B5r | An elephant! | 1,5s |
| C | How many did you get right? Tell me in the comments, and subscribe for more quizzes! | ≤5s |

Xuất mỗi mã thành 1 file `.mp3` đặt tên theo mã (A.mp3, B1.mp3, B1r.mp3, ...). Nếu ai33 chỉ xuất một file, đọc theo thứ tự trên và nghỉ 1 giây giữa các mã; em cắt theo khoảng lặng.

## 3. Prompt ảnh cho Flow (16:9, phong cách ảnh thật, nền tối sạch để chèn chữ)

Thêm đuôi chung cho mọi prompt: `photorealistic, extreme close-up, dark clean background, soft studio light, 16:9, no text, no watermark`

| Mã | Prompt | Dùng ở |
|---|---|---|
| H1 | Extreme close-up of a single green cat eye with vertical pupil, fur texture visible | Câu 1 gợi ý |
| H1r | Full portrait of a tabby cat looking at camera | Câu 1 reveal |
| H2 | Extreme close-up of orange and black tiger stripes fur, no face visible | Câu 2 |
| H2r | Bengal tiger portrait, head and shoulders | Câu 2 reveal |
| H3 | Extreme close-up of a white mountain goat hoof gripping a grey rock ledge, snow dust | Câu 3 |
| H3r | White mountain goat standing on a cliff ledge, portrait | Câu 3 reveal |
| H4 | Extreme close-up of a large round amber owl eye with feather ring | Câu 4 |
| H4r | Great horned owl portrait facing camera | Câu 4 reveal |
| H5 | Extreme close-up of wrinkled grey elephant skin with part of a tusk | Câu 5 |
| H5r | African elephant portrait, head on | Câu 5 reveal |
| H0 | Dark blue gradient background with soft bokeh lights, empty, for title screen | Mở và kết |

Tổng 11 ảnh. Không cần video Flow cho mẫu này; chuyển động do khâu dựng tạo (zoom chậm 1,05× trên mỗi ảnh gợi ý, đúng mẹo "ảnh tĩnh + zoom").

## 4. Khâu dựng (Claude làm bằng ffmpeg/Python khi có file)

Đầu vào anh gửi: 11 ảnh PNG/JPG đặt tên theo mã, các file mp3 ai33, logo nếu có.
Em sinh: timer đếm ngược 5→1 (vòng tròn rút dần + số to), khung chữ QUESTION N, hiệu ứng reveal (ảnh reveal trượt vào + tên con vật IN HOA), bảng điểm cuối, tiếng tích tắc và "ding" (tự sinh bằng mã, không dùng âm bản quyền), nhạc nền nhẹ (sinh bằng mã hoặc anh đưa file có bản quyền sử dụng).
Xuất: `quiz-mau-60s.mp4` 1920×1080 30fps, cộng bản 9:16 nếu anh muốn làm ảnh gig "có cả Shorts".

**Màu khuôn mẫu:** nền #0B1B3A, chữ trắng, timer #FFC43D, reveal #4CD964. Khách đặt sẽ đổi theo màu kênh họ.
