---
title: Hướng dẫn sử dụng Não
type: overview
created: 2026-08-27
updated: 2026-08-27
tags: [huong-dan, meta, cua-vao]
---

# HƯỚNG DẪN SỬ DỤNG NÃO

> Đọc file này khi bạn **mới nhận não** hoặc **lâu ngày không dùng, quên mất cách vận hành**.
> Muốn tra cứu nội dung → mở `wiki/index.md`. Muốn xem theo thời gian → mở `wiki/log.md`.

---

## 1. Não này là gì

Đây **không phải** một kho tài liệu để tìm kiếm. Đây là một **wiki tri thức tích lũy**:
mỗi nguồn mới (buổi Zoom, ghi âm, tài liệu, bài viết) được đọc **một lần**, rút ra ý chính,
rồi **tích hợp vào các trang đã có**. Tri thức được biên dịch một lần rồi giữ cho luôn
cập nhật — không tái tạo lại mỗi lần hỏi.

Khác biệt so với cách hỏi-đáp thông thường trên tài liệu:

| | Hỏi-đáp trên tài liệu | Não này |
|---|---|---|
| Mỗi lần hỏi | Đi tìm & ráp lại các mẩu tài liệu từ đầu | Đọc trang đã biên dịch sẵn |
| Nguồn mới | Chỉ thêm vào kho | **Tích hợp** vào trang cũ, ghi rõ mâu thuẫn nếu có |
| Giá trị theo thời gian | Đứng yên | **Dày lên** — tài sản cộng dồn |

**Mục tiêu của não**: nuôi chất liệu THẬT cho một **phễu sản phẩm thông tin**
(chuỗi nội dung dẫn người lạ thành người mua) — ngách hiện hành: dạy xây kênh YouTube
faceless (không lộ mặt) thị trường nước ngoài.

---

## 2. Bốn lớp — đâu là chỗ được đụng vào

```
não/
├── CLAUDE.md      ← BẢN QUY ƯỚC. Claude đọc đầu tiên. Bạn + Claude cùng sửa khi tìm ra cách làm tốt hơn
├── raw/           ← 🔒 NGUỒN GỐC — BẤT BIẾN. Claude chỉ ĐỌC, KHÔNG BAO GIỜ SỬA
├── wiki/          ← 🧠 TRI THỨC — Claude sở hữu hoàn toàn. Bạn đọc, Claude viết
├── production/    ← 📤 SẢN PHẨM PHỄU — đầu ra, nuôi bằng chất liệu từ wiki/
└── tools/         ← 🛠️ Bộ công cụ xử lý video/ảnh/dữ liệu
```

Ngoài vault còn một lớp thứ năm nằm ở máy:
`~/.claude/projects/<slug>/memory/` — **bộ nhớ dài hạn của Claude** (50 file ghi chú
ngắn: bạn là ai, đang làm dự án gì, đã dặn gì). Đây là thứ giúp Claude nhớ giữa các
phiên làm việc. Khi sao lưu **phải chép cả cái này**, nếu không não sẽ "mất trí nhớ".

> ⚠️ **Luật cứng số 1**: không sửa `raw/`. Nếu tư liệu gốc sai, ghi chú cái sai đó vào
> `wiki/`, đừng sửa nguồn — mất dấu vết là mất khả năng đối chiếu về sau.

---

## 3. Mở não lên

### Cách chính — Claude Code (làm việc)
```bash
cd ~/Documents/não && claude
```
Claude tự đọc `CLAUDE.md` để biết quy ước, rồi đọc `wiki/index.md` khi cần tra cứu.

### Cách phụ — Obsidian (đọc & xem sơ đồ)
Mở Obsidian → **Open folder as vault** → trỏ vào thư mục `não`.
Dùng để đọc thoải mái, bấm theo liên kết `[[...]]`, và xem **Graph view** (chế độ xem
đồ thị) để thấy trang nào là đầu mối, trang nào mồ côi.

---

## 4. Ba việc não làm được

### 4.1 NẠP NGUỒN — biến tư liệu thô thành tri thức

Thả file vào `raw/` rồi nói với Claude:

> *"Nạp `raw/zoom-2026-08-27.txt` vào não"*

Claude sẽ: đọc nguồn → **bàn ý chính với bạn trước khi ghi** → viết trang tóm tắt vào
`wiki/sources/` → cập nhật `index.md` → cập nhật các trang `entities/`, `concepts/`
liên quan (một nguồn thường chạm 10–15 trang) → ghi mâu thuẫn nếu nguồn mới phản bác
nguồn cũ → thêm một dòng vào `log.md`.

**Ba chỗ phải để ý khi nạp:**

- **Tài liệu dài** (>50 trang / >10.000 dòng, ví dụ transcript Zoom): đừng tin một lượt đọc.
  Bảo Claude đọc theo từng đoạn ~1.300 dòng rồi xác minh lại nhiều lượt — một lần nén
  thường bỏ sót khoảng 1/4 chi tiết.
- **Số liệu lớn** (cổng EEAT): con số lớn, thành tích, khẳng định mạnh — Claude **phải hỏi
  bạn xác nhận** trước khi ghi vào wiki. Và phải phân biệt rõ **mục tiêu** (tầm nhìn tương lai)
  với **thực tế** (hiện tại). Không ghi mục tiêu như thể là sự thật đã có.
- **Ghi âm**: đo âm lượng trước khi bóc chữ cả lô. Công cụ bóc chữ (whisper) **bịa lời trên
  đoạn im lặng** — có chữ không có nghĩa là có tiếng nói thật.

### 4.2 TRUY VẤN — hỏi não

Cứ hỏi bình thường:

> *"Quy trình tạo kênh của anh gồm mấy bước?"*
> *"So sánh chiến lược thị trường Ấn Độ và Mỹ"*
> *"Trong não có gì về ảnh thăm (thumbnail)?"*

Claude đọc `index.md` trước → mở các trang liên quan → trả lời **kèm trích dẫn nguồn**.
Định dạng tùy nhu cầu: đoạn văn, bảng so sánh, slide (Marp), biểu đồ, canvas.

> 💡 **Nếp quan trọng**: câu trả lời hay thì **lưu lại thành trang wiki**, đừng để nó
> biến mất vào lịch sử trò chuyện. Bảng so sánh → `wiki/comparisons/`. Phân tích khác →
> `wiki/analyses/`. Claude sẽ hỏi bạn trước khi lưu.

### 4.3 RÀ SOÁT SỨC KHỎE — dọn dẹp định kỳ

> *"Rà soát sức khỏe não"*

Claude tìm: mâu thuẫn giữa các trang · khẳng định cũ đã lỗi thời · trang mồ côi (không
ai trỏ tới) · khái niệm được nhắc nhiều nhưng thiếu trang riêng · thiếu liên kết chéo ·
lỗ hổng dữ liệu có thể lấp bằng tìm kiếm web. Rồi đề xuất câu hỏi cần điều tra tiếp.

Nên chạy sau mỗi đợt nạp nhiều nguồn.

---

## 5. Trong não hiện có gì (tính đến 27/08/2026)

**150 trang wiki · 92 mục nhật ký · 50 file bộ nhớ dài hạn**

| Thư mục | Số trang | Chứa gì |
|---|---|---|
| `wiki/concepts/` | 66 | Khái niệm & phương pháp — phần dày nhất |
| `wiki/sources/` | 50 | Mỗi nguồn đã nạp một trang tóm tắt |
| `wiki/entities/` | 11 | Người, tổ chức, sản phẩm (tiểu sử chủ nhân, BNC, Coach Hùng...) |
| `wiki/analyses/` | 11 | Phân tích đáng giữ lại |
| `wiki/comparisons/` | 2 | Bảng so sánh |
| `wiki/blog/` | 3 | Bài viết đã hoàn thiện |
| `wiki/_templates/` | 3 | Mẫu trang: khái niệm / nguồn / thực thể |

**Bốn cụm lớn nhất** (vào nhanh bằng trang trục):

| Cụm | Trang trục |
|---|---|
| 👤 Tiểu sử chủ nhân | `entities/tieu-su-moc-thoi-gian` |
| 🎯 Playbook YouTube faceless | `concepts/quy-trinh-xay-kenh` |
| 🧩 Phương pháp bộ não thứ 2 | `concepts/bo-nao-thu-2` |
| 💰 Hệ sản phẩm & bán hàng | `entities/he-san-pham-khoa-hoc` |

Hai cửa vào tổng: `wiki/overview.md` (dashboard) và `wiki/synthesis.md` (nối xuyên nguồn).

---

## 6. 16 kỹ năng — gọi bằng `/tên`

Kỹ năng (skill) là quy trình đóng gói sẵn. Gõ `/tên-skill` trong Claude Code.

**Viết & bán:**

| Lệnh | Làm gì |
|---|---|
| `/viet-bai-blog` | Blog — 2 chế độ: ngắn ~1000 từ (tâm sự) hoặc dài 2000–2500 từ chuẩn SEO (5 bước đa tác tử). Kèm tạo ảnh minh họa gốc + đăng thẳng lên phuc.vn |
| `/ban-hang` | Chuyên gia bán hàng: offer, kịch bản chốt, xử lý từ chối, định giá, CTA |
| `/salepage-warrior-plus` | Trang bán hàng dài, cấu trúc Jay Abraham 16 bước |
| `/ke-chuyen-7-buoc` | Kể chuyện bán hàng theo công thức 7 thành phần |
| `/viet-van-truyen-cam-hung` | Văn truyền cảm hứng thuần (không bán trực tiếp) |
| `/xac-dinh-de-tai` | Tìm đề tài đáng tiền nhất — giao thoa hồ sơ cá nhân × 10 thị trường mãi xanh |

**Video:**

| Lệnh | Làm gì |
|---|---|
| `/cut-clip-4k` | Băm video dài thành clip 10–30s, cắt theo chuyển cảnh, loại đoạn mờ/rung |
| `/bam-footage-mua` | Băm footage thành clip 5–50s tái dùng + sinh meta + upload baniclip.com |
| `/phan-loai-clip` | Xếp clip vào cây thư mục con-vật / hành-động bằng AI nhìn hình |
| `/chinh-mau` | Chỉnh màu hàng loạt về chất "giờ vàng ấm" |
| `/video-quy-trinh` | Ghép cả lô footage thô thành một video kể trọn một quy trình |
| `/content-ralex-safari` | Sinh kịch bản video thư giãn safari 4K kèm link tải footage |

**Khác:**

| Lệnh | Làm gì |
|---|---|
| `/thu-thach-youtube` | Dựng thử thách trên app ymm.vn (Expedition + task theo ngày) |
| `/hoi-thay-long` | Dẫn dắt xây một câu hỏi hoàn chỉnh gửi thầy Phạm Thành Long |

> ⚖️ **Bản quyền**: hai skill có tem © của học viên (kể chuyện, salepage) **không được
> import nguyên bản** — chỉ học rồi viết lại bằng lời mình.

---

## 7. 11 bộ công cụ trong `tools/`

`bam-footage-mua` · `cut-clip-4k` · `phan-loai-clip` · `video-quy-trinh` · `video-shorts` ·
`mau-gio-vang` (LUT màu) · `seo-video` (nhồi metadata) · `nhan-ban-khoa-hoc` (lồng tiếng Anh
+ phụ đề) · `keo-phuc-vn` (kéo bài WordPress) · `ban-do-cuoc-doi` · `xuat-nao` (sao lưu).

Cần cài: `ffmpeg`, `python3` + Pillow, `node`, `exiftool`, `whisper.cpp`.
`node_modules/` không nằm trong bản sao lưu — chạy `npm install` trong thư mục tool khi cần.

---

## 8. Hai cổng kiểm soát — không có ngoại lệ

Mọi sản phẩm ra khỏi não phải đi qua hai cổng này.

### 🟢 Cổng EEAT — chất liệu phải THẬT
EEAT = **E**xperience (trải nghiệm thật) · **E**xpertise (chuyên môn) ·
**A**uthoritativeness (uy tín) · **T**rust (tin cậy) — bốn yếu tố Google dùng đánh giá
chất lượng nội dung.

**Trước khi viết bất cứ thứ gì: phải đọc `wiki/` để rút ra trải nghiệm và chuyên môn
thật.** Không bịa kinh nghiệm, không bịa con số, không bịa thành tích.

Khi gặp số liệu chưa xác minh, não ghi rõ là **CHƯA XÁC MINH** và treo lại chờ chủ nhân
xác nhận — hiện đang có vài bảng số như thế. Đừng đem số treo đi làm nội dung.

### 🔴 Cổng YMYL — không gây hại
YMYL = *Your Money or Your Life* — nhóm chủ đề đụng trực tiếp tới **tiền bạc, sức khỏe,
an toàn** của người đọc. Dạy kiếm tiền trên YouTube rơi đúng vào nhóm này.

Bắt buộc: không hứa hẹn sai về tiền bạc · không khuyên thiếu căn cứ · nêu rõ rủi ro ·
số liệu chỉ là **tham chiếu của một ca cụ thể**, không phải cam kết kết quả.

### 🇻🇳 Luật ngôn ngữ
Mọi thứ — đọc, bàn, viết, đặt tên, ghi log — đều bằng **tiếng Việt**. Buộc phải dùng
thuật ngữ nước ngoài thì **giải thích ngay sau đó**: "lead magnet (mồi thu hút — quà tặng
miễn phí để lấy thông tin liên hệ)". Tên file dùng `kebab-case` không dấu; tiêu đề và
nội dung thì tiếng Việt có dấu đầy đủ.

---

## 9. Quy ước trang (khi Claude viết wiki)

- Tên file `kebab-case.md` không dấu: `nguyen-van-a.md`, `tiep-thi-lien-ket.md`.
- **Chống trùng tên**: hai người khác nhau cùng tên phải tách riêng bằng hậu tố —
  `anh-khanh-gom.md` vs `anh-khanh-o-to.md`. **Không bao giờ gộp hai thực thể cùng tên
  vào một trang.**
- Mỗi trang mở đầu bằng khối frontmatter: `title`, `type`, `created`, `updated`,
  `sources`, `tags`.
- Liên kết chéo `[[ten-trang]]` — **liên kết rộng tay**, đó là thứ làm wiki sống.
- Mâu thuẫn với nguồn cũ → **ghi rõ mâu thuẫn kèm trích dẫn cả hai phía**, đừng âm thầm
  ghi đè.
- Khẳng định quan trọng phải trích nguồn: `(nguồn: [[sources/ten-nguon]])`.

**`index.md` vs `log.md`**: `index.md` sắp theo *nội dung* (mục lục, đọc đầu tiên khi tra cứu).
`log.md` sắp theo *thời gian*, chỉ thêm vào cuối, không sửa mục cũ. Lấy 5 mục gần nhất:
```bash
grep "^## \[" wiki/log.md | tail -5
```

---

## 10. Sao lưu & mang đi

```bash
tools/xuat-nao/xuat-nao.sh "/Volumes/TÊN-Ổ"
```

Script tự làm 7 bước: chép vault → chép bộ nhớ Claude → **che mọi khóa/mật khẩu** →
kèm `KHOI-PHUC.md` + `DA-CHE-BI-MAT.md` → dọn rác → **quét lại tìm khóa sót và DỪNG nếu
còn** → đối chiếu số file + checksum.

Danh sách khóa cần che nằm **ngoài vault** ở `~/.claude/nao-khoa-can-che.txt` (mỗi dòng
`<chuỗi thật>|||<chuỗi thay thế>`). Để ngoài vì nếu để trong script thì chính script trở
thành file chứa khóa. Thêm khóa mới thì sửa file đó, **không sửa script**.

Muốn dựng lại trên máy khác: đọc `KHOI-PHUC.md` trong bản đã xuất.

---

## 11. Bẫy đã gặp thật — đọc để khỏi vấp lại

| Bẫy | Dấu hiệu | Cách xử |
|---|---|---|
| **Ổ exFAT nuốt file** | Chép hàng nghìn file nhỏ thì báo `Invalid argument` hàng loạt, thư mục đích rỗng nhưng ổ vẫn hụt dung lượng | Driver exFAT mới (fskit) của macOS 26 lỗi. Đổi ổ khác, hoặc gói thành một file `.tar` rồi chép |
| **Rút ổ giữa chừng** | Lỗi `Device not configured` | Chờ script báo xong 7/7 mới rút. Bản dở phải xóa, chép lại từ đầu |
| **Mất quyền chạy script** | `.sh` trên ổ ngoài không chạy được | exFAT không giữ quyền file → `chmod +x tools/**/*.sh` |
| **Rác `._*`** | exFAT sinh thêm một file `._` cho mỗi file | `find <thư-mục> -name '._*' -delete` |
| **Whisper bịa lời** | Transcript có chữ ở đoạn thực ra im lặng | Đo `mean_volume` + xem phổ 60 giây trước khi bóc cả lô. Mic hỏng vẫn ra chữ |
| **Đọc một lượt thiếu 1/4** | Tóm tắt tài liệu dài bỏ sót nhiều | Đọc theo đoạn ~1.300 dòng, liệt kê phân đoạn kèm số dòng, xác minh nhiều lượt |
| **Đồng hồ thiết bị lệch** | Mốc thời gian file ghi âm sai cả năm | Đối chiếu với nội dung buổi học, đừng tin metadata |

---

## 12. Nguyên tắc cốt lõi — nếu chỉ nhớ được một đoạn

> Não là **tài sản bền vững, cộng dồn**. Không tái tạo tri thức mỗi lần hỏi — biên dịch
> một lần, giữ cập nhật. `raw/` bất biến. `wiki/` do Claude duy trì có kỷ luật. `CLAUDE.md`
> cùng bạn tiến hóa. Mọi đầu ra phục vụ **một mục tiêu duy nhất**: xây phễu sản phẩm
> thông tin **bằng tiếng Việt**, dựa trên chất liệu **THẬT** (EEAT), **trung thực và
> không gây hại** (YMYL).

---

*Chi tiết đầy đủ về cấu trúc và quy trình nằm trong `CLAUDE.md` — file quy ước gốc.*
