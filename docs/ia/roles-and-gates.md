# Vai trò và gate — phân biệt để không gộp verdict

## Vai trò thiết kế, vai trò mô phỏng, người/agent thật sự

| Vai trò | Loại | Ai/cái gì thật sự thực hiện |
|---|---|---|
| Intake Steward | Thiết kế + mô phỏng | Code CLI (`control_room`), không phải người. Nhiệm vụ: capture và preserve request. |
| Product Analyst | Thiết kế + mô phỏng | Code template theo luật, không phải agent suy luận. Nhiệm vụ: tách statements, draft proposal/view. |
| Owner (real operator) | Thiết kế + thật | NohFinl (owner). Người duy nhất ở cổng review có thể APPROVE/REVISE/REJECT/DEFER, và là người duy nhất có thể cho product acceptance (đang PENDING). |
| Orchestrator (Muse) | Thật (agent của owner) | Viết code theo chỉ thị, chạy local, báo cáo ở gate, chuẩn bị trial. Không phải reviewer độc lập, không phải người nghiệm thu. |
| Reviewer (Codex reviewers) | Thật (agent review) | Chạy Windows, kiểm controls độc lập, viết verdict. Giới hạn đã ghi trong report: reviewers cùng nguồn và cùng họ model, không tạo độc lập tổ chức. Reviewer không thay owner nghiệm thu. |
| Operator label trong CLI | Tham số, không phải xác thực | `--operator` chỉ là nhãn chuỗi. Record ghi rõ: role argument là simulation only, không authenticate caller. Provenance decision là `OPERATOR_ASSERTED`, không bao giờ là `AUTHENTICATED_OWNER` trong slice này. |

## Bốn thứ không được gộp

### 1. Task DONE (trạng thái task trong proposal view)

- Nghĩa: một task trong proposal template đã được đánh dấu
  DONE bằng lệnh `complete` (hoặc vẫn PENDING/BLOCKED/READY).
- Không phải approval. T04 DONE mà chưa có decision vẫn
  chỉ sang decide; T04 DONE kèm decision thì next action
  null. Trong attempt-01, các task giữ PENDING vì owner
  decide mà không cần complete task trước — điều này được
  phép và không làm decision yếu đi.
- Đừng đọc “T04 DONE” thành “đã duyệt”.

### 2. Test PASS (kết quả suite/acceptance)

- Nghĩa: một test hoặc subcase acceptance chạy và đạt
  trong phạm vi đã ghi (OS, Python, fixture, runner).
- Luôn đi kèm scope và NOT_RUN: một subcase NOT_RUN
  (ví dụ symlink WinError 1314, packet-egress, real
  changed-brief, owner acceptance) chặn full-scope PASS,
  dù completed checks đạt 100%. Suite exit 0 không xóa
  skip; acceptance exit 2 là kết quả thiếu scope có chủ
  đích, không phải lỗi runtime mới.
- Test PASS của builder không thay reviewer verdict; test
  PASS của reviewer không thay owner acceptance.

### 3. Operator decision (cổng local)

- Nghĩa: một decision record trong store, tạo bằng lệnh
  `decide` với expected bindings từ snapshot đã review,
  provenance `OPERATOR_ASSERTED`.
- Ví dụ attempt-01: `DEC-6e42be7ab458849f` (APPROVE,
  operator `NohFinl`, tạo 2026-10-25T18:45:37Z). Decision
  này không đổi stage C4 (stage vẫn INTAKE), không phải
  product acceptance, không phải merge approval.
- Luật cổng: stale/mismatch → `REJECTED_STALE` (chỉ event,
  không tạo decision); duplicate giống hệt → trả record cũ
  với `already_exists`; reason lưu nguyên văn (chỉ dùng
  strip để chặn reason toàn whitespace); không tự lấy
  digest hiện tại thay snapshot đã review.

### 4. Product acceptance (quyền của owner)

- Nghĩa: chỉ thị rõ của owner với source, actor, time và
  scope cho slice sản phẩm. Hiện tại: PENDING.
- Một cuộc họp, một yêu cầu review, một reviewer verdict,
  một decision `OPERATOR_ASSERTED`, hay một lần chạy
  thành công đều KHÔNG phải product acceptance.
- Merge cũng vậy: merge là quyết định riêng của owner,
  chưa được yêu cầu, chưa được duyệt ở bất kỳ lượt nào.

## Quy tắc đọc gate

- Mỗi verdict phải ghi scope trong cùng câu: PASS ở scope
  hẹp không bao giờ được trình bày như PASS ở scope rộng.
- SKIP = NOT_RUN, không bao giờ = PASS.
- Một hard failure không được lấy trung bình che đi; phần
  trăm chỉ mô tả tiến độ chuẩn bị, không phải verdict.
- Khi scope thay đổi (payload, brief revision, template),
  phải bump revision, regenerate goldens nhất quán và nêu
  lý do — không repin lặng lẽ.
