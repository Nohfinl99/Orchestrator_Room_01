# Issues và bước tiếp theo — Orchestrator-Room

## Findings đã đóng, theo scope (không mở rộng scope khi báo)

| Finding | Đóng trong scope nào | Bằng chứng |
|---|---|---|
| R2-01 (decision bindings) | Contract: decision ingress bắt buộc `--expected-*` từ snapshot operator đã review, so sánh trong cùng CAS/lock transaction, thiếu/sai/mismatch đều reject | Addendum REV2.1 + C5 decide; golden `DEC-e81b5e7deada9801`, stale → `REJECTED_STALE` |
| R2-02 (checker validate instance thật) | Checker stdlib-only theo từng definition, keyword không hỗ trợ thì FAIL rõ | Positive 72 PASS, negatives 11/11 rejected (REV2.1, Linux) |
| R2-03 (newline + correction) | 5 loại line_endings; derived statements tách đúng break; correction no-op/conflict/not-found đều reject | Golden correction `INTAKE-432d09e4f46eaff1` |
| V21-01 (manifest path Windows) | `.as_posix()`, raw bytes không đổi; kết quả Windows gốc 71 PASS/1 FAIL giữ nguyên lịch sử | F21 `bef96ccf…`, checker sau patch khớp candidate SHA |
| V21-02 (recurse selectors + $ref sibling) | Reject $ref kèm sibling constraints; regression lưu trong repo (4 schema probes) | F21, schema probes 4/4 rejected |
| V21-03 (cross_decision dùng chung) | Một `cross_decision` cho cả bundle và per-file; regression 2 identity probes | F21, negatives 13/13 rejected |
| C5-F01 (evidence truth) | Runner verdict PASS/FAIL/NOT_RUN/INCONCLUSIVE, exit 0/1/2, completed vs full-scope tách riêng; A15 symlink NOT_RUN thay vì PASS giả | C5R1 runner + E5R1 |
| C5-F02 (byte fixtures) | Mọi input write_bytes; case LF và CRLF no-trim riêng; app không normalize newline | C5R1 tests + runner |
| C5-F03 (reason verbatim) | Strip chỉ để chặn whitespace-only; record và decision_id dùng reason nguyên văn | Padded `DEC-6a82e87b3bdd26d0` vs stripped `DEC-1e34f4692b242c32` |
| C5-F04 (T04 next action) | Gate READY → decide với expected bindings; DONE không decision vẫn chỉ decide; không thêm prerequisite all-tasks-DONE | C5R1 backend + tests |
| C5-F05 (Judge scope) | `judge_scope` ghi rõ C4-only; `snapshot_digest`/`judge_report` không đổi, không repin | C5R1 backend + tests |
| C5-F06 (coverage split) | A10/A13/A33 tách subcase chạy được (scope hẹp) và NOT_RUN (scope rộng) | C5R1 runner |
| C5-F07 (runner roots) | `--source-root`/`--output-dir`, PYTHONPATH tuyệt đối, reproduce command, manifest output riêng | C5R1 runner |
| W04 (runner CRLF) | CLOSED_SCOPED, chỉ phạm vi Windows C4/T3 | Supplement Windows C4/T3 |
| G01 (genesis repair) | Scoped PASS (8/8 controls trong phạm vi giới hạn) | Review roadmap C4 |
| CTX-R0-F01 (bypass clarification/source sau draft) | CLOSED_SCOPED trong C6R1 | Review R1: guards clarification/source trước duplicate lookup ở `ctx_review_rewrite`; control repeat-APPROVE exit 2 `clarification_open` |
| CTX-R0-F02 (batch câu hỏi gợi ý không dùng được) | CLOSED_SCOPED trong C6R1 | Review R1: assess chỉ gợi ý batch 2–3 câu; batch 4/1 bị chặn |
| CTX-R0-F03 (runner gán FAIL thành NOT_RUN) | CLOSED_SCOPED trong C6R1 | Review R1: aggregation tách completed vs full-scope; controls 6/6 |
| CTX-R1-DOC01 (repeat-review wording sai) | CLOSED_SCOPED, docs-only | Sửa trong `docs/ia/contextual-intake-current-use.md` (docs commit `1cfcb871…`); review DOC01 xác nhận đúng code, không cần sửa code |
| CTX-IA-DOC02 (IA route vẫn C5R1 + việc reviewer cũ) | CLOSED_SCOPED ở review DOCS-R1 (kênh rev14) | Submission `SUB-CTX-001-DOCS-R1`, docs commit `72495968…` |
| CTX-IA-DOC03 (Windows route legacy, thiếu runbook contextual) | CLOSED_SCOPED ở review DOCS-R2 (kênh rev17, APPROVED_SCOPED) | Runbook `docs/guides/windows-contextual-c6r1.vi.md`, docs commit `dfedb46e…`, submission `SUB-CTX-001-DOCS-R2` |
| CTX-GATE-01 (cổng WAITING_OWNER sai: thiếu nhãn keyword bị coi là thiếu fact) | CLOSED_SCOPED qua packet check rev24 | Đối chiếu nguồn + đáp án tái dùng nhãn `REUSED_PRIOR_OWNER_STATEMENT`; review `REV-CTX-001-GATE01` (rev19), packet `SUB-CTX-001-PACKET02-R0` |
| CTX-PACKET02-E01 (snapshot trial local-only, chưa nộp để review độc lập) | CLOSED_SCOPED ở review PACKET02-R0 (kênh rev24, APPROVED_SCOPED) | Packet commit `4f683e7e…`, descriptor dạng tham chiếu, digest tái tính khớp |

## Minor backlog (không sửa trong frozen C5R1, không chặn pilot)

| ID | Nội dung | Hướng xử lý sau này |
|---|---|---|
| R1-UX01 (P3) | T04 READY kèm decision sẵn vẫn gợi decide; note “decision xóa next action” chỉ đúng khi T04 DONE | Sửa ở revision riêng + test riêng khi có ích; không hiểu gợi ý lặp là approval mới bắt buộc |
| R1-TOOL01 (P3) | Output dir không enforce ngoài source, ghi đè filename cố định, path không quote / PYTHONPATH kiểu POSIX trong header | Dùng runbook PowerShell có quote + thư mục ngoài mới cho mỗi attempt; fix ở revision riêng nếu cần |
| R1-SCOPE01 | Tiêu đề A32 nói payload-change nhưng probe thực chất reject digest của proposal khác | Giữ scope hẹp đã ghi rõ; không cần brief editor cho pilot |

## Khoảng trống còn mở (OPEN / NOT_RUN)

Full pentest; packet-level egress monitoring; real
changed-brief invalidation; symlink privileged coverage;
real disk-failure recovery; live provider/worker/chat
integration; admitted knowledge retrieval; measured owner
baseline; owner product acceptance; merge. Không mục nào
trong danh sách này được coi là đã xong nhờ lớp IA này.

## Một việc nguyên tử tiếp theo

- Việc: owner quyết thật trên digest rewrite `74cd5f5b…` (cổng version 1): APPROVE / REVISE / REJECT / DEFER kèm lý do nguyên văn và nhãn operator. Việc tải bundle attempt-01 KHÔNG còn là việc tiếp theo: bundle đã được kiểm, receipt là `trial-bundle-audit.json` (PASS_SCOPED, phạm vi hẹp, overall NOT_VERIFIED) — không tải lại, không yêu cầu owner relay lại bundle.
- Người thực hiện: owner (NohFinl) quyết; sau đó Muse chạy review/propose và trial có giám sát theo guide `OWNER_TEST_GUIDE.vi.md` (review PACKET02-R0).
- “Xong” của việc này nghĩa là: có quyết định thật gắn đúng digest, sau đó mới chạy `ctx-review-rewrite` / `ctx-propose`. Cho tới lúc đó, 4 gate (local decision, evidence-review, owner feedback, product acceptance) vẫn báo riêng, không gộp thành một verdict.
- Việc treo riêng (không phải việc nguyên tử này): disposition commit `5cc1b4d…` (docs song song chưa nộp, chưa review) — chờ quyết định owner: nộp / giữ / hủy.
