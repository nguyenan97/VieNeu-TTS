# Giọng đọc VieNeu: giọng top và giọng tiếng Anh

Tổng hợp từ bảng xếp hạng sử dụng (`computedAt` 2026-10-24, cửa sổ `all`) và danh mục 1,222 giọng của vieneu.io. Cột **Có trên máy** cho biết giọng có sẵn trong model VieNeu-TTS v3 Turbo chạy local hay không; các giọng còn lại (phần lớn engine `v4`) chỉ có trên dịch vụ vieneu.io.

## Gợi ý nhanh (giọng chạy được trên máy)

| Mục đích | Giọng | Ghi chú |
|---|---|---|
| Song ngữ Việt–Anh | `Custom Song Ngữ` | Hải Đăng cho câu Việt, giọng Anh (Kokoro am_michael trộn 80% với Hải Đăng) cho câu tiếng Anh trọn vẹn. Tạo bằng `examples/make_bilingual_voice.py`. |
| Đa dụng, phổ biến nhất | `Hải Đăng` | Model local nhận tên **Minh Quân** (#1) và **Minh Quân Pro** (#5) là Hải Đăng; bản trên vieneu.io chạy engine v4 nên có thể nghe khác. Đọc tiếng Anh khá tốt trong các giọng có sẵn. |
| Kể chuyện, triết lý, sách nói | `Thiện Minh` | Model local nhận tên **Anh Khôi** (#8) là Thiện Minh. Tiếng Anh yếu hơn, nên dùng `Custom Song Ngữ` nếu nhiều tiếng Anh. |
| Đọc kinh, kể chuyện chậm | `Thiền Tâm Đức` | #15 |
| Tin tức, giọng nữ miền Nam | `Thùy Dung` | #38 |
| Tiếng Anh thuần | `Adam` | Giọng nam tiếng Anh duy nhất có sẵn (#23); hoặc clone một clip tiếng Anh bản ngữ. |

## Top 50 giọng được dùng nhiều nhất

| # | Giọng | Tỉ lệ dùng | Có trên máy | Giới · Vùng | Engine | Mô tả |
|---|---|---|---|---|---|---|
| 1 | Minh Quân | 1.00 | ✅ `Hải Đăng` (alias) | Nam · Bắc | v4 | Giọng nam trầm ấm |
| 2 | Adam Tốp Tốp | 0.67 | — | Nam · Nam | v4 | Nam · Nam · Cảm xúc, Không nghiêm túc, Tốp Tốp, Tấu hề |
| 3 | Duyên Hà My | 0.41 | — | Nữ · Nam | v4 | Nữ · Nam · Rõ ràng, TikToker thời trang |
| 4 | Nhật Phong | 0.34 | — | Nam · Bắc | v3 | Nam · Phong cách đọc truyện |
| 5 | Minh Quân Pro | 0.32 | ✅ `Hải Đăng` (alias) | Nam · Bắc | v4 | Nam · Bắc · Code, IT, Chuyên nghiệp |
| 6 | Đăng Quân | 0.22 | — | Nam · Nam | v4 | Nam · Nam · Cảm xúc, Truyền cảm, Review công nghệ, Siêu review |
| 7 | Mai Bé Phương | 0.18 | — | Nữ · Nam | v4 | Nữ · Nam · Vui nhộn, TikTok, Tự nhiên, Văn phòng |
| 8 | Anh Khôi | 0.16 | ✅ `Thiện Minh` (alias) | Nam · Bắc | v4 | Nam · Bắc · Kể chuyện, Cảm xúc, Truyền cảm |
| 9 | Ban Mai | 0.16 | — | Nữ · Bắc | v4 | Nữ · Bắc · Tin tức, Rõ ràng |
| 10 | Nhỏ Ngọt Ngào | 0.14 | — | Nữ · Bắc | v4 | Nữ · Bắc · Nói chuyện vui, Ngọt ngào, Dịu dàng |
| 11 | Tưởng Vy | 0.13 | — | Nữ · Nam | v4 | Nữ · Nam · Ngọt ngào, Truyền cảm, Người bạn |
| 12 | Châu Thảo | 0.13 | — | Nữ · Bắc | v4 | Nữ · Bắc · Tin tức, Hoạt ngôn |
| 13 | Huyền My | 0.11 | — | Nữ · Bắc | v4 | Nữ · Bắc · Hoạt ngôn, Tin tức, Chuẩn giọng |
| 14 | Thái Duy Bình | 0.11 | — | Nam · Bắc | v4 | Nam · Bắc · Tin tức, Hoạt ngôn, Đưa tin, Truyền cảm |
| 15 | Thiền Tâm Đức | 0.10 | ✅ `Thiền Tâm Đức` | Nam · Nam | v4 | Nam · Nam · Phật, Trầm, Đọc kinh, Kể chuyện chậm |
| 16 | My Méo | 0.09 | — | Nữ · Nam | v4 | Nữ · Nam · Méo mó, Vui nhộn |
| 17 | Bình Bon | 0.09 | — | Nam · Nam | v4 | Nam · Miền Nam · Méo mó, vui nhộn |
| 18 | Ngọc Lan | 0.09 | — | Nữ · Nam | v3 | Giọng nữ dịu dàng, ấm áp, miền Nam. |
| 19 | Mạnh Dũng 1 | 0.09 | — | Nam · Bắc | v4 | Nam · Bắc · Tin tức, Chất lượng, Uy tín |
| 20 | Tào Tháo | 0.08 | — | Nam · Nam | v4 | Nam · Miền Nam · Hùng hồn, mạnh mẽ |
| 21 | Adam vui | 0.08 | — | Nam · Nam | v4 | Nam · Vui nhộn, tấu hài |
| 22 | Bích Ngọc | 0.08 | — | Nữ · Bắc | v3 | Nữ · Phong cách đọc truyện |
| 23 | Adam | 0.06 | ✅ `Adam` | Nam · Nam | v3 | Nam · Tiếng Anh · Giọng đọc tự nhiên |
| 24 | Mai Phương | 0.06 | — | Nữ · Bắc | v4 | Nữ · Bắc · Tin tức, Rõ ràng |
| 25 | Nam Nũng Nịu | 0.06 | — | Nam · Bắc | v4 | Nam · Bắc · Méo mó, Vui nhộn, Bựa |
| 26 | Anh Dũng | 0.05 | — | Nam · Nam | v3 | Nam · Phong cách đọc truyện |
| 27 | Kim Chi | 0.05 | — | Nữ · Bắc | v4 | Giọng nữ rõ ràng, trẻ trung |
| 28 | Phú Thắng | 0.05 | — | Nam · Bắc | v4 | Nam |
| 29 | Bảo Long | 0.05 | — | Nam · Bắc | v3 | Nam · Phong cách đọc truyện |
| 30 | Linh Thi | 0.05 | — | Nữ · Bắc | v4 | Nữ Trẻ em |
| 31 | Hoàng Nam | 0.05 | — | Nam · Bắc | v3 | Nam · Phong cách đọc truyện |
| 32 | Anh Thư | 0.04 | — | Nữ · Bắc | v3 | Nữ · Phong cách đọc truyện |
| 33 | Hà My | 0.04 | — | Nữ · Bắc | v3 | Nữ · Phong cách đọc truyện |
| 34 | Thanh Ngọc | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 35 | Thiện Nhân | 0.04 | — | Nam | v3 | Nam · Phong cách đọc truyện |
| 36 | Bạch Tuyết | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 37 | An Nhiên | 0.04 | — | Nữ · Bắc | v3 | Nữ · Phong cách đọc truyện |
| 38 | Thùy Dung | 0.04 | ✅ `Thùy Dung` | Nữ · Nam | v3 | Nữ · Nam · Phong cách tin tức |
| 39 | Bảo Khánh | 0.04 | — | Nam · Bắc | v3 | Nam · Phong cách đọc truyện |
| 40 | Tuấn Huy | 0.04 | — | Nam · Bắc | v4 | Giọng nam trầm ấm, tự nhiên miền Bắc. |
| 41 | An Khang | 0.04 | — | Nam · Nam | v3 | Nam · Phong cách đọc truyện |
| 42 | Hương Giang | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 43 | Trung Dũng | 0.04 | — | Nam · Trung | v4 | Nam · Miền Trung (Bình Định) · Gần gũi |
| 44 | Bảo Ngân | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 45 | Bảo Ngọc | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 46 | Hoàng Long | 0.04 | — | Nam · Bắc | v4 | Giọng nam trẻ, giọng khỏe khoắn |
| 47 | Kiều Linh | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 48 | Ái Chi | 0.04 | — | Nữ · Bắc | v4 | Nữ · Kể chuyện, chậm |
| 49 | Cẩm Hồng | 0.04 | — | Nữ · Nam | v3 | Nữ · Phong cách đọc truyện |
| 50 | Hạ Vy | 0.04 | — | Nữ · Bắc | v3 | Nữ · Phong cách đọc truyện |

## Giọng tiếng Anh (109 giọng trong danh mục)

69 nam, 40 nữ; engine: `v3` 65, `v4` 44. Trên máy chỉ có `Adam`.

Muốn đọc tiếng Anh chuẩn hơn với VieNeu local: clone một clip 5–15 giây của người nói tiếng Anh bản ngữ (`--ref-audio`), hoặc dùng giọng song ngữ (`examples/make_bilingual_voice.py --en-ref clip.wav`).

**Nam** (69):

- Aaron (v4) — Kể chuyện
- Aaron (v3) — Kể chuyện, Tự nhiên, Rõ ràng
- Adam (v3) — Mới, Tự nhiên
- Adrian (v4) — Kể chuyện
- Adrian (v3) — Kể chuyện, Nam tính, Rõ ràng
- Andrew (v4) — Kể chuyện
- Andrew (v3) — Kể chuyện, Tự nhiên, Ấm áp
- Benjamin (v4) — Kể chuyện
- Benjamin (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Caleb (v3) — Kể chuyện, Rõ ràng
- Christopher (v4) — Kể chuyện
- Christopher (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Connor (v4) — Kể chuyện
- Connor (v3) — Kể chuyện, Sâu lắng, Chuyên nghiệp
- Daniel (v4) — Kể chuyện
- David (v4) — Kể chuyện
- David (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Dominic (v3) — Kể chuyện, Rõ ràng
- Dylan (v3) — Kể chuyện, Rõ ràng
- Edward (v4) — Kể chuyện
- Felix (v3) — Kể chuyện, Rõ ràng
- George (v4) — Kể chuyện
- Gregory (v4) — Kể chuyện
- Gregory (v3) — Trầm ấm, Lôi cuốn, Kể chuyện
- Henry (v4) — Kể chuyện
- Henry (v3) — Kể chuyện, Giọng nam, Tự nhiên
- Jack (v4) — Kể chuyện
- Jack (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- James (v4) — Kể chuyện
- James (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Kevin (v4) — Kể chuyện
- Kevin (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- Leo (v3) — Kể chuyện, Rõ ràng
- Logan (v3) — Kể chuyện, Rõ ràng
- Lucas (v4) — Kể chuyện
- Lucas (v3) — Kể chuyện, Tự nhiên, Duyên dáng
- Marcus (v4) — Kể chuyện
- Marcus (v3) — Trầm ấm, Rõ ràng, Kể chuyện
- Marcus 2 (v3) — Kể chuyện, Rõ ràng, Tự tin
- Marcus 3 (v3) — Kể chuyện, Sâu lắng, Tự nhiên
- Marcus Loan (v4) — Kể chuyện
- Marcus Loan (v3) — Kể chuyện, Rõ ràng, Ấm áp
- Michael (v4) — Kể chuyện
- Michael (v3) — Kể chuyện, Rõ ràng, Nam tính
- Nathan (v4) — Kể chuyện
- Nathan (v3) — Kể chuyện, Rõ ràng, Tự nhiên
- Nicholas (v4) — Kể chuyện
- Nicholas (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Oliver (v4) — Kể chuyện
- Oliver (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- Owen (v3) — Kể chuyện, Rõ ràng
- Patrick (v4) — Kể chuyện
- Patrick (v3) — Tự nhiên, Kể chuyện, Nam tính
- Robert (v4) — Kể chuyện
- Robert (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- Robert 2 (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- Russell (v4) — Kể chuyện
- Russell (v3) — Chuyên nghiệp, Kể chuyện, Rõ ràng
- Ryan (v3) — Kể chuyện, Rõ ràng
- Samuel (v4) — Kể chuyện
- Samuel (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- Thomas (v4) — Kể chuyện
- Thomas (v3) — Tường thuật, Rõ ràng, Chuyên nghiệp
- Trevor (v4) — Kể chuyện
- Trevor (v3) — Kể chuyện, Trầm ấm, Chuyên nghiệp
- Vincent (v3) — Kể chuyện, Rõ ràng
- Wesley (v3) — Kể chuyện, Rõ ràng
- William (v4) — Kể chuyện
- William (v3) — Kể chuyện, Dễ nghe, Tự nhiên

**Nữ** (40):

- Amy (v4) — Kể chuyện
- Amy (v3) — Tiểu thuyết, Rõ ràng, Chuyên nghiệp
- Audrey (v3) — Kể chuyện, Rõ ràng
- Charlotte (v4) — Kể chuyện
- Charlotte (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Chloe (v3) — Kể chuyện, Rõ ràng
- Claire (v4) — Kể chuyện
- Claire (v3) — Kể chuyện, Dịu dàng, Chuyên nghiệp
- Eleanor (v3) — Kể chuyện, Rõ ràng
- Emily (v4) — Kể chuyện
- Emma (v4) — Kể chuyện
- Emma (v3) — Kể chuyện, Rõ ràng, Duyên dáng
- Ethan (v3) — Kể chuyện rõ ràng, Tự tin, Chuyên nghiệp
- Grace (v4) — Kể chuyện
- Grace (v3) — Kể chuyện, Mềm mại, Tự nhiên
- Hannah (v3) — Kể chuyện, Rõ ràng
- Iris (v4) — Kể chuyện
- Iris (v3) — Kể chuyện, Tự nhiên, Dễ nghe
- Isabella (v4) — Kể chuyện
- Isabella (v3) — Kể chuyện, Âm điệu ấm áp, Rõ ràng
- Jessica (v4) — Kể chuyện
- Jessica (v3) — Kể chuyện, Chuyên nghiệp, Tự nhiên
- Julia (v4) — Kể chuyện
- Julia (v3) — Kể chuyện, Rõ ràng, Chuyên nghiệp
- Lily (v3) — Kể chuyện, Rõ ràng
- Megan (v3) — Kể chuyện, Rõ ràng
- Naomi (v3) — Kể chuyện, Rõ ràng
- Natalie (v3) — Kể chuyện, Rõ ràng
- Nora (v3) — Kể chuyện, Rõ ràng
- Olivia (v4) — Kể chuyện
- Olivia (v3) — Kể chuyện, Tự nhiên, Dễ nghe
- Rachel (v4) — Kể chuyện
- Rachel (v3) — Kể chuyện, Tự nhiên, Thân thiện
- Sarah (v4) — Kể chuyện
- Sarah (v3) — Kể chuyện, Chuyên nghiệp, Rõ ràng
- Sophia (v4) — Kể chuyện
- Sophia (v3) — Rõ ràng, Tự nhiên, Kể chuyện
- Sophie (v4) — Kể chuyện
- Sophie (v3) — Kể chuyện, Tự nhiên, Hấp dẫn
- Victoria (v3) — Kể chuyện, Rõ ràng

## Cập nhật lại tài liệu này

Danh sách được tạo từ hai file JSON xuất từ vieneu.io (`ranking` và `voices`). Khi bảng xếp hạng thay đổi, xuất lại hai file đó và tạo lại bảng; giọng có trên máy được đối chiếu với `Vieneu()._preset_voices` và `_voice_aliases`.
