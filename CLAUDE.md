# Não — Wiki tri thức tự xây, phục vụ phễu sản phẩm thông tin

Đây là một **wiki tri thức bền vững** do Claude xây và duy trì. Khác với cách hỏi-đáp
thông thường trên tài liệu (gọi là RAG — *retrieval-augmented generation*, nghĩa là
"sinh nội dung có truy xuất": mỗi lần hỏi lại đi tìm và ráp các mẩu tài liệu từ đầu),
wiki này **tích lũy** kiến thức: mỗi nguồn mới được đọc, trích xuất, rồi **tích hợp**
vào các trang đã có. Tri thức được biên dịch **một lần** rồi giữ cho luôn cập nhật,
không tái tạo lại mỗi lần hỏi.

Wiki là một **tài sản bền vững, cộng dồn** (mỗi nguồn mới làm nó dày thêm chứ không
thay thế). Đó là bộ não (gọi tắt là **Brain**) cung cấp chất liệu thật cho nhiệm vụ
chính bên dưới.

---

## 0. Hai luật nền — luôn áp dụng, không ngoại lệ

### Luật ngôn ngữ: chỉ tiếng Việt
- **Mọi hoạt động** — đọc, thảo luận, viết trang wiki, tạo sản phẩm phễu, đặt tên,
  ghi log — đều **bằng tiếng Việt**.
- Khi buộc phải dùng thuật ngữ nước ngoài, **luôn kèm giải thích tiếng Việt** ngay
  sau đó. Ví dụ: "lead magnet (mồi thu hút — quà tặng miễn phí để lấy thông tin liên
  hệ)", "CTA (lời kêu gọi hành động)", "SEO (tối ưu hóa cho công cụ tìm kiếm)".
- Tên file vẫn dùng chữ không dấu kiểu `kebab-case` (các-từ-nối-bằng-gạch-ngang) cho
  dễ tham chiếu; nhưng **tiêu đề và nội dung** thì tiếng Việt có dấu đầy đủ.

### Luật nhiệm vụ: dự án này dùng để tạo MỘT PHỄU SẢN PHẨM THÔNG TIN
Mục tiêu của vault này không phải "biết để biết", mà là **xây một phễu sản phẩm
thông tin** (information product funnel — chuỗi nội dung dẫn dắt người lạ thành người
mua). Tài sản phễu nằm trong thư mục `production/` (xem [[production/README]]), gồm
7 lớp:

| Lớp | Thư mục | Vai trò |
|----|---------|---------|
| 0 | `0-bai-pr` | Bài PR (quan hệ công chúng — giới thiệu, tạo uy tín ban đầu) |
| 1 | `1-mang-xa-hoi` | Nội dung mạng xã hội (thu hút, kéo lưu lượng) |
| 2 | `2-blog` | Blog (xây chuyên môn, nuôi dưỡng niềm tin) |
| 3 | `3-leadpage` | Trang thu khách + mồi thu hút + chuỗi email (lấy & nuôi liên hệ) |
| 4 | `4-seo` | SEO (tối ưu hóa cho công cụ tìm kiếm — kéo lưu lượng tự nhiên) |
| 5 | `5-ads` | Quảng cáo (kéo lưu lượng trả phí) |
| 6 | `6-salepage` | Trang bán hàng + sản phẩm thông tin chính |

Mọi tài sản phễu phải đi qua **hai cổng kiểm soát** dưới đây.

#### Cổng EEAT — chất liệu phải THẬT
EEAT (bốn yếu tố Google dùng đánh giá chất lượng: **Experience** — trải nghiệm thật,
**Expertise** — chuyên môn, **Authoritativeness** — thẩm quyền/uy tín, **Trust** —
độ tin cậy). Trước khi làm bất kỳ sản phẩm nào, **phải đọc `wiki/` (Brain)** để rút
ra trải nghiệm và chuyên môn thật của chủ nhân. **Không bịa** kinh nghiệm, con số,
hay thành tích.

#### Cổng YMYL — không gây hại
YMYL (*Your Money or Your Life* — "tiền bạc hoặc cuộc sống của bạn": nhóm chủ đề ảnh
hưởng trực tiếp tới tài chính, sức khỏe, an toàn của người đọc). Mọi sản phẩm phải:
không hứa hẹn sai về tiền bạc/sức khỏe, không khuyên thiếu căn cứ, luôn trung thực,
nêu rõ rủi ro khi cần.

---

## 1. Ba lớp của hệ thống

1. **`raw/`** — Nguồn gốc, là **chân lý gốc** (source of truth). Bài viết, tài liệu,
   ảnh, dữ liệu, ghi chú.
   - **BẤT BIẾN**: Claude chỉ ĐỌC, **không bao giờ sửa** lớp này.
   - Ảnh tải về `raw/assets/`.
2. **`wiki/`** — Tri thức do Claude tạo (định dạng markdown). Claude **sở hữu hoàn
   toàn** lớp này: tạo trang, cập nhật khi có nguồn mới, duy trì liên kết chéo, giữ
   nhất quán. Bạn đọc; Claude viết.
3. **`CLAUDE.md`** (chính file này) — **Schema** (bản quy ước): cấu trúc + quy trình.
   Bạn và Claude **cùng tiến hóa** file này theo thời gian khi tìm ra cách làm tốt hơn.

Ngoài ra `production/` là **đầu ra** (sản phẩm phễu), được nuôi bằng chất liệu từ
`wiki/`.

---

## 2. Cấu trúc thư mục wiki

```
wiki/
  index.md          # Mục lục toàn bộ trang (theo nội dung) — đọc đầu tiên khi truy vấn
  log.md            # Nhật ký theo thời gian (chỉ thêm vào cuối, không sửa cũ)
  overview.md       # Tổng quan toàn wiki (tạo khi đã đủ nội dung)
  synthesis.md      # Tổng hợp/kết nối xuyên nhiều nguồn (tạo khi đã đủ nội dung)
  entities/         # Trang thực thể (người, tổ chức, sản phẩm, địa điểm...)
  concepts/         # Trang khái niệm/chủ đề
  sources/          # Mỗi nguồn đã nạp có một trang tóm tắt
  comparisons/      # Bảng/trang so sánh
  analyses/         # Kết quả truy vấn đáng giữ (phân tích không phải dạng so sánh)
```

---

## 3. Quy ước trang

- Tên file: `kebab-case.md` không dấu (ví dụ `nguyen-van-a.md`,
  `tiep-thi-lien-ket.md`).
- **Chống trùng tên thực thể**: hai người/vật khác nhau cùng tên phải tách riêng bằng
  hậu tố ngành/đặc điểm — `kebab-case`: `anh-khanh-gom.md` vs `anh-khanh-o-to.md`.
  Không bao giờ gộp hai thực thể trùng tên vào một trang.
- Mỗi trang mở đầu bằng khối **frontmatter** (siêu dữ liệu ở đầu file, viết bằng
  YAML — một định dạng khai báo dữ liệu dạng `khóa: giá trị`):
  ```yaml
  ---
  title: Tên trang (tiếng Việt có dấu)
  type: entity | concept | source | comparison | overview | synthesis
  created: NĂM-THÁNG-NGÀY
  updated: NĂM-THÁNG-NGÀY
  sources: [ten-nguon-1, ten-nguon-2]   # các nguồn liên quan
  tags: [the-1, the-2]
  ---
  ```
- Liên kết chéo dùng cú pháp wikilink kiểu Obsidian: `[[ten-trang]]`. Liên kết
  rộng tay — nó là thứ làm wiki "sống".
- Khi một khẳng định **mâu thuẫn** với nguồn cũ, **ghi rõ mâu thuẫn** kèm trích dẫn
  cả hai phía, đừng âm thầm ghi đè.
- Mọi khẳng định quan trọng phải **trích nguồn**: `(nguồn: [[sources/ten-nguon]])`.

---

## 4. Ba quy trình vận hành

### 4.1 NẠP NGUỒN (Ingest)
Khi bạn thả file vào `raw/` và yêu cầu xử lý, Claude sẽ:
1. Đọc nguồn (đọc phần chữ trước; nếu có ảnh, xem ảnh riêng để bổ sung ngữ cảnh — vì
   mô hình không đọc được ảnh nhúng trong markdown chỉ bằng một lượt).
   - **Tài liệu dài** (>50 trang hoặc >10.000 dòng — vd transcript Zoom, SOP): KHÔNG tin
     một lần đọc. Đọc theo từng đoạn (~1.300 dòng), liệt kê phân đoạn kèm số dòng, rồi
     xác minh lại nhiều lượt cho đủ độ phủ (một lần nén thường bỏ sót ~25% chi tiết).
2. **Thảo luận ý chính (key takeaways) với bạn** trước khi ghi.
   - **Xác minh số liệu lớn (cổng EEAT)**: con số lớn, thành tích, khẳng định mạnh phải
     hỏi/xác nhận với bạn trước khi vào wiki; phân biệt rõ **mục tiêu** (tầm nhìn tương
     lai) với **thực tế** (hiện tại) — không ghi mục tiêu như thể là sự thật đã có.
3. Viết trang tóm tắt vào `wiki/sources/<ten-nguon>.md`.
4. Cập nhật `index.md` (thêm mục mới).
5. Cập nhật các trang `entities/` và `concepts/` liên quan (tạo mới nếu chưa có).
   Một nguồn có thể chạm tới 10–15 trang.
6. Ghi lại mâu thuẫn nếu nguồn mới phản bác nguồn cũ.
7. Thêm một dòng vào `log.md`.

> Mặc định nạp **từng nguồn một** và giữ bạn tham gia (đọc tóm tắt, duyệt cập nhật).
> Có thể nạp hàng loạt nhiều nguồn nếu bạn yêu cầu giám sát ít hơn.

### 4.2 TRUY VẤN (Query)
Khi bạn đặt câu hỏi:
1. Đọc `index.md` trước để tìm trang liên quan.
2. Đọc các trang đó, tổng hợp câu trả lời **kèm trích dẫn**.
3. Định dạng tùy câu hỏi: trang markdown, bảng so sánh, slide (dùng Marp — công cụ
   tạo slide từ markdown), biểu đồ (dùng matplotlib — thư viện vẽ biểu đồ của Python),
   hoặc canvas.
4. **Câu trả lời tốt nên được lưu lại** thành trang wiki mới (`comparisons/` nếu là bảng
   so sánh; `analyses/` nếu là phân tích khác; hoặc `concepts/`) — đừng để phân tích
   biến mất vào lịch sử trò chuyện. Hỏi bạn trước khi lưu.

### 4.3 RÀ SOÁT SỨC KHỎE (Lint)
Khi được yêu cầu, rà soát toàn wiki để tìm:
- Mâu thuẫn giữa các trang.
- Khẳng định cũ đã bị nguồn mới vượt qua (đã lỗi thời).
- Trang mồ côi (orphan — không có liên kết nào trỏ tới).
- Khái niệm quan trọng được nhắc nhưng thiếu trang riêng.
- Thiếu liên kết chéo.
- Lỗ hổng dữ liệu có thể lấp bằng tìm kiếm trên web.

Đề xuất câu hỏi mới cần điều tra và nguồn mới cần tìm.

---

## 5. `index.md` so với `log.md`

- **`index.md`** — *theo nội dung*. Là mục lục mọi trang: liên kết + tóm tắt một
  dòng + siêu dữ liệu (ngày, số nguồn). Tổ chức theo nhóm. Cập nhật mỗi lần nạp nguồn.
  **Đọc đầu tiên** khi truy vấn.
- **`log.md`** — *theo thời gian*. Chỉ thêm vào cuối (append-only — không sửa mục cũ).
  Mỗi mục bắt đầu bằng tiền tố nhất quán để máy đọc được:
  `## [NĂM-THÁNG-NGÀY] ingest | Tên nguồn`. Nhờ vậy có thể lọc bằng lệnh dòng:
  `grep "^## \[" log.md | tail -5` (lấy 5 mục gần nhất).

---

## 6. Các kỹ năng (skills) có sẵn

- **`xac-dinh-de-tai`** (`.claude/skills/xac-dinh-de-tai/`): Tìm "đề tài đáng tiền
  nhất" = giao thoa giữa thế giới bên trong (hồ sơ trong `wiki/`) và bên ngoài (10
  thị trường mãi xanh — nhóm nhu cầu luôn có người mua). Gọi 3 tác tử (agent — chương
  trình con tự chạy) tạo ra các đề tài → cho tranh luận → chốt 1 đề tài kèm sản
  phẩm/dịch vụ. Gọi qua `/xac-dinh-de-tai`.
- **`kich-ban-noi-khac-nghiet`** (`.claude/skills/kich-ban-noi-khac-nghiet/`): Viết
  **kịch bản video tài liệu faceless "nơi khắc nghiệt"** (Siberia, Oymyakon, Danakil,
  La Rinconada, đảo hẻo lánh...) cho kênh view ngoại — song ngữ Việt–Anh **kèm link
  footage Envato/Storyblocks đặt sẵn trước từng đoạn lời**. Ra 3 file: kịch bản dựng ·
  lời dẫn EN sạch · bảng kiểm. Khuôn **mô-đun 2 phút**, bắt buộc có **sợi chỉ xuyên
  suốt**, **12 đòn giọng văn** đo được, cổng **EEAT/YMYL 12 mục**. Có chế độ RÀ SOÁT
  kịch bản có sẵn (cân thời lượng theo số từ, bắt lệch giọng, bắt sai số liệu).
  Nền: [[wiki/analyses/phong-cach-kich-ban-noi-khac-nghiet]]. Gọi qua
  `/kich-ban-noi-khac-nghiet`.
- **`anh-facebook`** (`.claude/skills/anh-facebook/`): Tạo **ảnh đăng Facebook**
  (Instagram/Threads) bằng máy sinh Pillow — không qua Canva, không dùng ảnh bản quyền.
  Hai khuôn: **A "phiếu giấy sạch"** 1080×1080 cho việc *trao tài nguyên + gọi hành động*
  (comment nhận quà, mồi thu hút, thông báo) và **B "đen mờ"** 1080×1350 cho *trích dẫn ·
  bài học · tâm tình*. Kèm luật viết chữ, cổng EEAT/YMYL và caption Facebook. Công cụ ở
  `tools/anh-facebook/`, phong cách ở
  [[wiki/analyses/phong-cach-the-tai-nguyen-phieu-sach]]. Gọi qua `/anh-facebook`.
- **`nhan-ban-tay`** (`.claude/skills/nhan-ban-tay/`): **Nhân bản video** đã dựng xong sang
  ngôn ngữ khác (mặc định Anh → Tây Ban Nha) bằng **lồng tiếng đồng bộ theo timestamp từng câu**:
  giữ nguyên hình (`-c:v copy`) và **giữ nguyên nhạc nền** (tách stem bằng demucs, chồng giọng mới
  lên), kèm xuất kịch bản `.docx` tiếng đích. Sáu bước, chỉ **khâu dịch** cần đầu óc; 3 phép thử
  bắt buộc trước khi giao. Thông số đóng băng ở `config.json` + `THONG-SO.md`. Gọi qua
  `/nhan-ban-tay`. Nền: [[wiki/concepts/nhan-ban-video-da-ngon-ngu]] · [[wiki/sources/skill-nhan-ban-tay]].
  ⚠️ Cần cài `faster-whisper edge-tts demucs torch python-docx numpy` + ffmpeg.
- **`viet-bai-blog`** (`.claude/skills/viet-bai-blog/`): Skill blog HỢP NHẤT — MỘT
  skill, HAI chế độ (đã gộp `blog-da-tac-tu` vào đây, 2026-07-08). **Ngắn** (~1000 từ):
  bài cá nhân/tâm sự, một tác tử viết nhanh, hạn chế hỏi. **Dài** (2000–2500 từ) chuẩn
  SEO/EEAT/YMYL: quy trình ĐA TÁC TỬ 5 bước (gom tư liệu → 3 dàn bài → tranh biện có thư
  ký → đồng viết + bình duyệt chéo → tổng biên tập chống "văn AI"). Kèm 2 năng lực tuỳ
  chọn: **tạo ảnh minh hoạ gốc** từ số liệu thật (Pillow, không đụng ảnh bản quyền) và
  **đăng lên WordPress phuc.vn** (REST API, draft/publish, tự tải ảnh + ảnh đại diện,
  link trụ–cụm). Hồ sơ thương hiệu (giọng/EEAT) ở `references/_private/`. Gọi qua
  `/viet-bai-blog`.
- **Bộ 3 profile KÊNH 5 — truyện thiên nhiên dựng bằng AI, dê núi** (2026-09-21). Một chuỗi liên kết,
  cùng dùng **"phiếu tập"** (`production/kenh-5-de-nui/tap-NN-*/00-PHIEU-TAP.md`) làm thẻ nối, đều theo **công thức
  của Phúc BANI** (tiêu đề: [[wiki/analyses/cong-thuc-tieu-de-kenh-5-de-nui]]):
  `/kich-ban` → `/viet-tieu-de` → `/mo-ta-video`.
  - **`kich-ban`** (`.claude/skills/kich-ban/`): viết kịch bản — khuôn 7 thành phần A→C→B (kể chuyện của Phúc), tập
    8 phút ~685 từ EN, tách THẬT/HƯ, chống lặp, tập ghép "FULL EPISODE"; ra `01-KICH-BAN-DUNG` · `02-LOI-DAN-EN` ·
    `03-KIEM-TRA`. Có `scripts/can_tu.py` (cân từ + mốc chương).
  - **`viet-tieu-de`** (`.claude/skills/viet-tieu-de/`): `[Từ khoá video]: [Cảm xúc]+[Hành động]+[Bối cảnh] | [Từ khoá
    chủ đề]`, 3 tuyến 2:1:1, kiểm luật + chấm VidIQ; ra `04-TIEU-DE`. Có `scripts/kiem_tieu_de.py`; nhật ký
    `production/kenh-5-de-nui/NHAT-KY-TIEU-DE.md`.
  - **`mo-ta-video`** (`.claude/skills/mo-ta-video/`): mô tả 100–150 từ, tag theo thứ tự Phúc, hashtag, bình luận ghim,
    khối miễn trừ + khai báo AI, cho video mục phóng sự/truyện động vật; đọc phiếu tập + kịch bản + tiêu đề; ra `05-MO-TA`.
    Có `scripts/kiem_mo_ta.py`.
  ⚠️ Cả ba **không** hứa "cảnh thật" (cổng EEAT/YMYL); khai báo AI đặt ở mô tả + Studio (quyết định chủ nhân 21/09/2026).

---

## 7. Công cụ tùy chọn (khi wiki lớn dần)

- **Tìm kiếm trên markdown**: ví dụ `qmd` — công cụ tìm kiếm chạy ngay trên máy
  (on-device), kết hợp BM25 (xếp hạng theo từ khóa) và vector (xếp hạng theo ngữ
  nghĩa), có cả dòng lệnh (CLI) lẫn máy chủ MCP để Claude gọi như công cụ gốc. Ở quy
  mô nhỏ, chỉ cần `index.md` là đủ; khi lớn lên mới cần công cụ tìm kiếm riêng.
- **Marp**: tạo slide từ markdown (có sẵn tiện ích bổ trợ cho Obsidian).
- **Dataview**: tiện ích Obsidian truy vấn theo frontmatter — sinh bảng/danh sách
  động từ siêu dữ liệu các trang.
- **Graph view** (chế độ xem đồ thị của Obsidian): thấy hình dạng wiki — trang nào là
  đầu mối, trang nào mồ côi.
- **Obsidian Web Clipper**: tiện ích trình duyệt biến bài web thành markdown, kèm tải
  ảnh về `raw/assets/` — cách nhanh để đưa nguồn vào `raw/`.

---

## 8. Nguyên tắc cốt lõi

Wiki là **tài sản bền vững, cộng dồn**. Không tái tạo tri thức mỗi lần hỏi — biên
dịch một lần, giữ cập nhật. `raw/` bất biến; `wiki/` do Claude duy trì kỷ luật;
schema (`CLAUDE.md`) cùng bạn tiến hóa. Mọi đầu ra phục vụ **một mục tiêu duy nhất**:
xây phễu sản phẩm thông tin **bằng tiếng Việt**, dựa trên chất liệu **thật** (EEAT) và
**trung thực, không gây hại** (YMYL).
