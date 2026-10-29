# Chỉnh lý điều hướng — 29/10/2026

## Scope và baseline

Theo yêu cầu owner trong chat Codex: kiểm tra, sắp xếp thư mục Orchestrator
Room trên GitHub và sửa file phù hợp. Repository đích duy nhất là
Orchestrator_Room_01, baseline `0d6cb6ca8b88e9f09345281c5b911ec98488738b` (214 tracked files).
Không cập nhật repo gốc Orchestrator-Room hoặc Orchestrator_Reverse.

## Phát hiện và cách xử lý

| Phát hiện | Cách xử lý |
|---|---|
| Nhóm docs đã chia nhưng thiếu entry từng thư mục | Thêm README cho briefs/specs/reports/notes/data/guides/windows và changes |
| Guide GitHub dẫn về nhánh Muse repo gốc | Guide mới bắt đầu từ bản sao, dẫn nguồn riêng khi cần pin |
| Dòng DOC02/DOC03 pending mâu thuẫn cập nhật rev24 cùng file | Sửa dòng tóm tắt theo gate rev14/rev17 đã ghi; không tạo review mới |
| Main frozen và nhánh Muse bị đọc như thuộc bản sao | Ghi rõ scope hai repository ở README, START_HERE, IA, source map |
| Ma trận đề xuất và kết quả contextual dễ bị gộp | Guide phân biệt A01–A33 với runner B01–B17 và evidence C6R1 |

Không dời/xóa file hiện hữu. Không sửa code, runners, fixtures, evidence,
packet, report đã freeze, manifest hoặc pin lịch sử. Bổ sung index là
cách sắp xếp đường đọc phù hợp với locator đã được pin.

## Phạm vi đã đọc và kiểm kê

Đọc entry, docs index, IA, guide GitHub, phần đầu runbook Windows, evidence
index và packet index; đối chiếu code contextual cùng report/kết quả đã
đọc ở lượt đánh giá trước. Kiểm kê toàn cây theo Git. Không tuyên bố audit
ngữ nghĩa từng raw log, từng fixture hoặc review nằm ở repo gốc.
Không truy vấn kênh nguồn live; trạng thái sản phẩm giữ snapshot rev24.

## Kiểm tra

Kiểm local: 214 file gốc; 8 file điều hướng sửa và 11 file mới.
Đối chiếu SHA-256 bytes của 206 file gốc ngoài allowlist với Git baseline:
0 mismatch; không xóa hoặc đổi tên file.
20 link tương đối cũ trong 2 hồ sơ giữ nguyên; [bảng locator](../ia/legacy-locators.md)
chỉ ra 18 file tương ứng và 2 gap chưa xác định. Không sửa raw để che gap.
Kiểm relative Markdown links theo file tồn tại, bỏ fenced code và URL ngoài;
0 link hỏng trong các file sửa/thêm. Không kiểm HTTP toàn bộ link upstream. Không chạy suite nghiệp vụ, acceptance runner, target, provider
hoặc W4. Tài liệu không phải bằng chứng chạy sản phẩm.

## Bàn giao

Đọc [README](../../README.md) → [docs index](../README.md) hoặc chọn nhóm
theo nhu cầu. Việc owner quyết trên rewrite và nghiệm thu sản phẩm vẫn
là các gate riêng trong snapshot nguồn, không phải đầu ra của lượt IA này.
