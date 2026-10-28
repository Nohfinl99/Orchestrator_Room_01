# Log quyết định của owner — Orchestrator-Room

Chỉ ghi quyết định thật của owner (NohFinl), kèm nguồn để
kiểm lại. Một dòng trong file, một log của builder, hay một
review claim đều KHÔNG phải quyết định owner. Quyết định
chỉ có hiệu lực khi owner confirm trong chat Muse trực
tiếp (kênh duyệt duy nhất, chốt 2026-10-23); xác nhận qua
Telegram không tính là duyệt.

## Quyết định đã có

| Ngày | Quyết định | Nguồn |
|---|---|---|
| 2026-10-23 | Kênh duyệt duy nhất: mọi duyệt/cho phép chỉ có hiệu lực khi owner confirm trong chat Muse trực tiếp | Chat Muse trực tiếp, chốt ~14:24 |
| 2026-10-23 | Ranh giới cứng userbot: từ chối vận hành phiên đăng nhập tài khoản Telegram cá nhân của owner, giữ nguyên cả khi được phép | Chat Muse trực tiếp, ~14:09 |
| 2026-10-23 | Luật kích hoạt nhạy cảm chỉ dành cho chủ, nhận diện duy nhất bằng Telegram user ID (6862229246 / 6507707008) | Chat Muse trực tiếp, ~14:17 |
| 2026-10-26 ~17:14 | Watch kênh giữ nguyên chế độ tự sửa (auto-fix trong scope CTX-001), chấp nhận rủi ro đua commit song song | Chat Muse trực tiếp (sau báo cáo race commit `5cc1b4d…`) |
| 2026-10-27 | Nguyên tắc Orchestrator: chức năng điều phối KHÔNG mặc định là Muse — bất kỳ model nào cũng có thể giữ chức năng này nếu đáp ứng đủ scope/binding/ACK theo contract | Chat Muse trực tiếp; nguyên lý gốc `docs/architecture/agents.md` (repo Orchestrator_Reverse) |
| (standing) | Không merge, không PR, không đổi `main` hay Orchestrator_Reverse nếu không có chỉ thị riêng cho đúng hành động đó | Luật đứng từ 2026-10-22, nhắc lại qua các phiên |

## Việc đang chờ quyết định (KHÔNG phải quyết định)

| Việc | Trạng thái | Nguồn |
|---|---|---|
| Quyết định thật trên digest rewrite `74cd5f5b…` (cổng version 1): APPROVE / REVISE / REJECT / DEFER + lý do + nhãn operator | ĐANG CHỜ | Kênh rev20–rev24; packet `SUB-CTX-001-PACKET02-R0` đã được duyệt scoped (rev24), nhưng duyệt packet không thay thế quyết định này |
| Product acceptance | PENDING | Kênh rev24; toàn hệ NOT_VERIFIED |
| Owner feedback (attempt-01) | PENDING | Kênh rev24; báo riêng, không gộp verdict |
| Disposition commit `5cc1b4d…` (docs song song chưa nộp, chưa review) | ĐANG CHỜ | Đầu nhánh trước packet commit; chưa có chỉ thị nộp / giữ / hủy |
| Baseline đo lường | NULL (NOT_MEASURED) | Intake attempt-01/02; không tính tiết kiệm khi chưa đo |

## Việc KHÔNG được tính là quyết định

- Review APPROVED_SCOPED của Codex (kể cả PACKET02-R0):
  đó là readiness cho trial có giám sát, không phải approval
  của owner, không phải product acceptance, không phải
  merge approval.
- Approval trong test/synthetic fixture: chỉ là fixture,
  không phải approval thật cho rewrite thực tế.
- Câu “owner đã duyệt” trong bất kỳ file/log nào mà không
  có nguồn là chỉ thị thật trong chat Muse trực tiếp.
