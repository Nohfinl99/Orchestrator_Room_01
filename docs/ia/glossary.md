# Glossary — thuật ngữ Orchestrator-Room

Định nghĩa ngắn gọn, theo cách repo này dùng. Thuật ngữ nào
cũng có thể bị hiểu sai nếu tách khỏi scope của nó — khi trích
dẫn, kèm theo scope và pin.

- **Control-room:** phòng điều hành local: nơi yêu cầu được
  tiếp nhận, chuẩn bị ngữ cảnh, duyệt và theo dõi — không
  phải agent, không chạy live.
- **Intake:** bản ghi bất biến của một yêu cầu đã tiếp nhận
  (byte/ký tự, SHA-256, brief, baseline, unknowns). Đổi yêu
  cầu = intake mới, không sửa intake cũ.
- **Brief:** bản tóm tắt có cấu trúc của intake (template
  `PRODUCT_INTAKE_BRIEF_REV2` cho đường hiện hành).
- **Digest:** SHA-256 của payload đã chuẩn hóa (canonical
  JSON: sort keys, không khoảng trắng thừa, UTF-8). Đổi một
  trường payload là đổi digest.
- **Rewrite (bản viết lại):** draft có cấu trúc gồm
  goal/context/scope/desired_output/constraints/unknowns/
  labelled inferences/next_action, gắn với intake và
  clarification, có revision và digest riêng.
- **Clarification:** lượt hỏi 2–3 câu khi intake thiếu chiều
  thiết yếu; trạng thái `WAITING_CLARIFICATION` rồi
  `ANSWERED`. Đáp án phải nguyên văn, đủ số lượng bằng số
  câu hỏi.
- **DEC (decision):** quyết định đã ghi trong store, có
  decision_id và reason nguyên văn. Decision của operator
  mang provenance `OPERATOR_ASSERTED`, không phải
  `AUTHENTICATED_OWNER`.
- **CPROP (contextual proposal):** proposal theo ngữ cảnh,
  chỉ được tạo sau APPROVE thật trên đúng digest, và ràng
  buộc với intake + digest + answers đã duyệt.
- **Gate:** điểm dừng bắt buộc trong workflow (ví dụ: owner
  review rewrite, evidence review, product acceptance). Qua
  gate cần bằng chứng hoặc quyết định thật, không tự qua.
- **Verdict:** kết luận review theo từng predicate:
  `APPROVED_SCOPED` (đạt trong scope đã nêu),
  `CHANGES_REQUESTED` (cần sửa trong scope),
  `REVIEW_BLOCKED` (thiếu evidence/truy cập),
  `WAITING_OWNER` (chờ owner). Một hard failure không được
  lấy trung bình che đi.
- **CLOSED_SCOPED:** finding đã đóng trong đúng scope đã
  nêu, không phải đóng cho mọi scope.
- **Packet:** gói bằng chứng kiểm chứng được của một trial
  (descriptor, transcript đã redacted, hash file raw,
  provenance, manifest). Packet tốt cho phép reviewer tính
  lại digest mà không cần raw request.
- **Submission:** một lần nộp lên kênh (mã `SUB-…`) gồm
  code/evidence/docs pins và bảng kiểm; reviewer trả lời
  bằng review (`REV-…`).
- **Review:** lượt review độc lập của Codex trên kênh, có
  verdict, findings và next atomic action riêng.
- **Pin:** commit SHA (hoặc blob SHA) xác định đúng một
  revision. Trạng thái chỉ lấy từ pin, không lấy từ tên
  file hay ngày sửa.
- **Frozen:** commit đã đóng băng, không sửa sau đó. Code
  và evidence luôn nộp thành commit riêng, tách nhau.
- **Locator-only:** nguồn chỉ ghi định danh (locator), không
  nhận là đã đọc hay hiểu nội dung nguồn đó.
- **OPERATOR_ASSERTED:** provenance của decision do operator
  ghi, không phải xác thực owner thật.
- **NOT_RUN:** trường hợp bắt buộc nhưng chưa chạy — không
  được gộp thành PASS. Tương tự: `NOT_VERIFIED` (toàn hệ
  chưa được verify), `NOT_MEASURED` (baseline chưa đo).
- **Stale / REJECTED_STALE:** draft/proposal đã cũ vì context
  đổi sau khi nó được tạo (thêm source, clarification mới,
  draft mới hơn). APPROVE trên draft stale bị reject.
- **Manifest:** danh sách file kèm SHA-256 và độ dài byte;
  manifest tự loại trừ chính nó (không liệt kê bản thân).
- **Evidence:** file/log/report chứng minh một lần chạy;
  evidence frozen xác định bằng commit, không bằng path
  trên nhánh.
- **Source-map:** bản đồ nguồn: nguồn nào hiện hành/lịch
  sử, claim nào thuộc phạm vi nào, truy cập ra sao.
- **HITL (human-in-the-loop):** owner là người phê duyệt /
  executor thật cuối cùng; không có approval nào tự sinh
  từ log, quote hay claim của builder.
- **IA (Information Architecture):** lớp tổ chức đường đọc
  và trạng thái của repo (index, bản đồ nguồn, bảng gate).
  IA không đóng gate kỹ thuật và không nghiệm thu.
- **Legacy:** đường template cố định 4 task đời C4/C5, khác
  đường contextual hiện hành (intake → clarify → draft →
  owner review → propose).
- **Orchestrator (chức năng):** chức năng điều phối, không
  phải identity thứ bảy và không mặc định là một model cụ
  thể; model nào giữ chức năng này cũng cần scope/binding/
  ACK theo contract.
