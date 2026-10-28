# Archive — Orchestrator-Room

Thư mục này dành cho các snapshot lưu trữ MỚI được tạo ra
có chủ đích (ví dụ: bản sao frozen của một tài liệu tại
một mốc), KHÔNG phải nơi để “dọn” repo bằng cách dời file
cũ vào đây.

Quy tắc bắt buộc:

1. **Không di chuyển file hiện có vào đây.** Các submission
   và review trên kênh đang trỏ tới đúng path gốc; dời file
   là vỡ locator. Khi một tài liệu bị thay thế, nó ở nguyên
   chỗ cũ và được ghi `SUPERSEDED-BY` trong
   [../ia/status-register.md](../ia/status-register.md).
2. **Không xóa lịch sử.** Không có file nào bị xóa khỏi repo
   để “dọn sạch” — lịch sử là bằng chứng, không phải rác.
3. **Snapshot mới vào đây phải ghi rõ:** nguồn, pin, ngày,
   lý do lưu trữ, và quan hệ với file hiện hành (nếu có).
4. Tại thời điểm bản IA này, thư mục archive chưa chứa
   snapshot nào — và đó là trạng thái đúng, không phải
   thiếu sót.
