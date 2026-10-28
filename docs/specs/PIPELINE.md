# Pipeline điều phối cho Muse

## Nguyên tắc

Room là control plane: hiển thị và điều phối stage, task, evidence, role và quyết định. Hub/backend là nguồn trạng thái duy nhất. Agent đề xuất, Builder thực hiện trong phạm vi, Judge đánh giá trên snapshot cố định, owner đóng gate. Không role nào được tự cấp quyền cho bước tiếp theo.

## Pipeline và gate

| Bước | Vai trò | Artifact | Điều kiện qua gate |
|---|---|---|---|
| 0. Intake | Intake Steward | Scope, owner, mục tiêu, nguồn, loại dữ liệu, unknowns | Thiếu scope/authority thì BLOCKED |
| 1. Evidence | Evidence Curator | Observation facts, locator/hash, repetition và baseline hoặc unknown | Không có quan sát thật thì không xác nhận pain; synthetic chỉ dùng demo |
| 2. Discovery | Product Analyst | Tách facts/inferences, hypothesis draft, unknowns và alternative explanations | Backend giữ NEEDS_EVIDENCE nếu thiếu fact hoặc source bắt buộc |
| 3. Product review | Owner + Product Architect | Brief revision, thin slice, tiêu chí đo và ranh giới dữ liệu/runtime | Owner duyệt đúng revision trước khi build |
| 4. Build | Local Builder | Diff, runbook, synthetic fixtures, test outputs | Repo private, capability tối thiểu; không provider/network mặc định |
| 5. Independent Judge | AI Judge (read-only) | Per-case PASS/FAIL/NOT RUN/INCONCLUSIVE kèm evidence locator | Judge không sửa source/evidence/status; thiếu bằng chứng không PASS |
| 6. Owner decision | Owner | Accept, revise, reject hoặc defer kèm lý do | Chỉ owner đóng quyết định sản phẩm |

## Luồng điều phối

1. Owner gửi task vào project room; backend gắn task với project, role, scope, dữ liệu và dependency.
2. Room hiển thị task owner, trạng thái, dependency, revision, blocked reason và next action.
3. Agent nhận đúng phần việc theo capability; không có quyền chung chỉ vì ở cùng room.
4. Mọi artifact được version/hash trước khi dùng làm đầu vào cho bước tiếp theo.
5. Gate evaluator kiểm tra điều kiện bằng schema/rule ở backend. Chỉ chuyển state khi invariant hợp lệ.
6. Judge chỉ nhận snapshot đóng băng gồm criteria revision, source/evidence, changed paths và raw run outputs. Judge trả kết quả riêng; không sửa state.
7. Owner nhận summary và đưa ra quyết định có lưu event. Lỗi hoặc thiếu evidence giữ gate mở/blocked.

## Bài học chọn lọc từ Bear Agent Manager

Áp dụng độc lập ý tưởng hub giữ state chung, UI là control room, task dependency nhìn thấy được, routing rõ vai và giới hạn vòng lặp. Không lấy code do upstream README không cấp license. Không bê default quyền rộng, worker gửi dữ liệu ra provider, quyền tool bypass, background auto-run hoặc coi task DONE là test PASS. Fail-open chỉ có thể dùng cho telemetry không quan trọng; approval và evidence gate phải fail closed.

## Trạng thái phải tách riêng

- Task: TODO / DOING / BLOCKED / DONE. DONE chỉ nói người làm báo đã xong.
- Painpoint: OWNER_STATED_GOAL_NOT_VALIDATED_PAIN / NEEDS_EVIDENCE / OBSERVED / HYPOTHESIS_DRAFT / OWNER_REVIEWED.
- Implementation: NOT_STARTED / IN_PROGRESS / BUILT_PENDING_CHECKS.
- Verification: NOT_RUN / INCONCLUSIVE / FAIL / PASS. PASS cần đủ bằng chứng theo VERIFICATION_POLICY.md.
- Owner outcome: ACCEPTED / REJECTED / DEFERRED, không thay thế trạng thái verification.

## Tình trạng hiện tại

- Repo private Orchestrator-Room ban đầu rỗng trên main.
- Owner chọn pilot tự dùng cho product discovery.
- Chưa có workflow thực tế, tần suất, manual baseline hay acceptance threshold.
- Intake local #2: PREPARED_NOT_DISPATCHED; 0 model call, 0 tool dispatch.
- Bước tiếp theo: Muse đọc gói này, xây control-plane slice với synthetic data trong private repo, chạy checks cục bộ và gửi commit cùng raw evidence. Sau đó mới tiến hành review/test độc lập.
- Không thay đổi sáu identity, REA–IDA, phase/gate hoặc lịch sử FAIL của Orchestrator_Reverse.
