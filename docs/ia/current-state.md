# Trạng thái hiện hành — Orchestrator-Room (lớp IA, không phải verdict)

Tài liệu này là ảnh trạng thái tại thời điểm lớp IA được
viết, dựa trên pins và manifest đã kiểm chứng trước đó.
Nó không tự tạo verdict mới. Khi có kết quả mới, cập nhật
bảng gate ở đây bằng pin mới, không sửa lịch sử cũ.

## Phạm vi repository

Đây là snapshot nguồn tới rev24 được sao lưu tại Orchestrator_Room_01.
Lượt 29/10/2026 chỉ sửa điều hướng, chưa đọc kênh nguồn live hoặc tạo
review/verdict/owner decision mới. Các pin trong bảng thuộc repo gốc.

## Pins (nguồn trạng thái, không phải tên file “latest”)

| Mốc | Pin |
|---|---|
| Code hiện hành C6R1 (nhánh `muse/local-control-room`) | `c7a837e3538aa6902c24ec4fd3fd8fd1cd047255` |
| Evidence hiện hành E6R1 (riêng, sau C6R1) | `ea9c9464b14eb93bf4efe6b00bf6ce73e59218e7` |
| Code C6 / evidence E6 (trước C6R1) | `385f503b003479d4ae957d97cf3657e3900e1a37` / `da2d318cdad0ea268e8fc709f59fc1462321f4c9` |
| Reviewer R1 verdict | `APPROVED_SCOPED` (artifact `17da045bb042fa1927cbd6f96028f3fb73537878`, nhánh `codex/ctx-001-r1-review`, report `reviews/ctx-001/r1/REPORT.md`) |
| Docs current-use (sửa DOC01) | `docs/ia/contextual-intake-current-use.md`, docs commit `1cfcb871b60c5871bf7b4d98208f7cc10586aa9f` |
| Docs review DOC02/DOC03 | DOC02 CLOSED_SCOPED tại DOCS-R1 (rev14); DOC03 CLOSED_SCOPED tại DOCS-R2 APPROVED_SCOPED (rev17), docs `dfedb46e…`; xem bảng gate và cập nhật rev24 bên dưới |
| Code frozen C5R1 — lịch sử (nhánh `muse/local-control-room`) | `fd3430c9f1b0e98d1f6c9c62067b935f20054498` |
| Evidence E5R1 — lịch sử (riêng, sau C5R1) | `dde7b605b0ef9c97e3ae91156303638f3ba843fd` |
| Windows supplement C5R1 — lịch sử (docs/evidence only) | `cc6591cbfbe7faf9315c3171dff69c7062ddb2c2` |
| Reviewer branch / commit — lịch sử C5R1 | `codex/c5r1-owner-pilot` / `6a48b3f07bd67110b8c8b95768db712994e76499` |
| Reviewer verdict — lịch sử C5R1 | READY_FOR_BOUNDED_OWNER_TRIAL |
| Nhánh `main` của repo gốc Orchestrator-Room (frozen tại snapshot) | `8bd7d8a9fcdff34ef6ed1626050c2371661ab279` |
| Code C5 / evidence E5 (lịch sử) | `0a3d5a4d6606f3427b10162671a99adc3ef5b39b` / `18d74aa157fa9130f70f93be770e88c9e345f496` |
| Checker F21 / evidence E21 (lịch sử) | `bef96ccf3dabda9088491a615eec23cbc8dfe32c` / `1e5907658fbe6dd188ef1b8552fa48c053d040a3` |
| Packet REV2.1 (lịch sử) | `0441decffd456ab1582375b353fd51d5b25b05c0` |
| Fixtures intake-rev2 (F21 manifest, SHA-256) | `fd1716cb77b93adbe739663a630beb3eb80232dbc463f04cdad631d0c265a39c` (39 files) |

## Gate — đã qua, theo scope (không gộp thành toàn hệ PASS)

| Gate | Trạng thái | Phạm vi và bằng chứng |
|---|---|---|
| C6R1 bounded fixes F01–F03 (hiện hành) | Completed checks đạt, full-scope NOT_RUN | Linux (builder, kiểm độc lập lại): suite 83/83, acceptance 24/24 completed, 2 NOT_RUN, exit 2. Windows (reviewer R1): suite 81 PASS + 2 SKIP, acceptance 24/24 completed, 2 NOT_RUN, exit 2. Full-scope NOT_RUN ở cả hai OS. Xem `docs/reports/RUN_REPORT_C6R1.md` và `evidence/c6r1/`. |
| DOC01 (repeat-review wording) | CLOSED_SCOPED | Sửa docs-only trong `docs/ia/contextual-intake-current-use.md`; code không đổi; reviewer R1 xác nhận guards-before-duplicate đúng code và control repeat-APPROVE. |
| DOC02/DOC03 (IA route + Windows runbook) | CLOSED_SCOPED: DOC02 đóng ở review DOCS-R1 (kênh rev14), DOC03 đóng ở review DOCS-R2 APPROVED_SCOPED (docs commit `dfedb46e…`, kênh rev17) | Xem submission `SUB-CTX-001-DOCS-R1` và `SUB-CTX-001-DOCS-R2`. |
| C5R1 bounded fixes F01–F07 | Completed checks đạt, full-scope NOT_RUN | Linux (builder): suite 57/57, acceptance 60/60 completed, 3 NOT_RUN, exit 2. Windows (reviewer): suite 55 PASS + 2 SKIP, acceptance 59/59 completed, 4 NOT_RUN, exit 2. Full-scope NOT_RUN ở cả hai OS. Xem `docs/reports/RUN_REPORT_C5R1.md` và `docs/guides/windows/WINDOWS_SUPPLEMENT_C5R1.md`. |
| W04 (runner CRLF) | CLOSED_SCOPED | Chỉ trong phạm vi Windows C4/T3. Không phải chứng minh cho mọi runner. |
| T24 symlink (Windows) | NOT_RUN | WinError 1314 (thiếu privilege). Trên Linux subcase này chạy được; Linux không chứng minh Windows. |
| Checker F21 (V21-01–03) | Đóng trong stored probes (Linux) | Positive 72 PASS, negatives 13/13 rejected, schema probes 4/4 rejected trên Linux. Windows cho F21 thuộc lịch sử review C5, không được gộp thành bằng chứng C5R1 mới. |
| G01 genesis repair | Scoped PASS | Chỉ trong phạm vi review có giới hạn của nó, không phải toàn hệ. |
| C5/E5 lịch sử (FAIL Windows cũ) | Giữ nguyên lịch sử | Suite C5 trên Windows cũ: 51 PASS, 1 FAIL (test_c5_10 do write_text), 2 SKIP. Không sửa thành PASS. |

## Gate — pending (không giấu thành PASS)

| Gate | Trạng thái | Ghi chú |
|---|---|---|
| Evidence-review gate (attempt-01 bundle) | PASS_SCOPED (receipt, không phải verdict toàn hệ) | Theo audit `docs/reviews/2026-10-26-ia-context/trial-bundle-audit.json` tại pin `0a9729772b4598c771a5b7b49b62e46c8ae47a38`: 13 manifest entries khớp, file set exact, history recomputed chain_valid true (event_count 3), raw stdout khớp store, overall NOT_VERIFIED. Phạm vi audit: bundle consistency, manifest custody, deterministic binding và history recomputation — KHÔNG xác thực actor và KHÔNG quan sát độc lập quá trình chạy gốc. Không cần tải lại bundle đã audit. |
| Owner feedback (attempt-01) | PENDING | `FEEDBACK.md` vẫn trống. Không tự viết feedback thay owner. |
| Product acceptance | PENDING | Cần chỉ thị rõ của owner với source, actor, time, scope cho slice sản phẩm. Chưa có. |
| Merge | PENDING, không yêu cầu | Không merge/PR nào được duyệt hay thực hiện. Merge là quyết định riêng của owner. |
| Full pentest, packet-level egress, real changed-brief, symlink privilege, disk-failure recovery, live integration, knowledge retrieval, measured baseline | NOT_RUN / OPEN | Xem [issues-and-next](issues-and-next.md). |

## Trial OWNER_TRIAL_01 attempt-01 (tóm tắt, chi tiết ở bundle)

- Input: request thật của owner (tin nhắn trực tiếp, owner
  KHÔNG gửi file gốc; Muse tạo file từ tin nhắn theo chỉ
  thị, 504 bytes, SHA-256
  `2bf4740b8e478ecae833171bb3a8acedce3562b089d065416c9c5618b9dd8907`).
- Intake `INTAKE-0d0bcbe75d4fbee1`, proposal
  `PROP-INTAKE-0d0bcbe75d4fbee1`, digest
  `0792c65ac599275a01da7f31d6897e3a88675c1d1dc913d4a3817fea6cec9f2f`.
- Local decision gate: ĐÃ THỰC THI, không chạy lại.
  Decision `DEC-6e42be7ab458849f` (APPROVE, provenance
  `OPERATOR_ASSERTED`, operator `NohFinl`, tạo lúc
  2026-10-25T18:45:37Z). Verify-history chain_valid true,
  event_count 3. Overview cuối 1/1/1, stage INTAKE.
- Evidence bundle: zip 10773 bytes, SHA-256
  `e428fa8a01c5d3289bb62343253e9dca3722a9cd0205985210340967369b9909`
  (link Muse storage, hết hạn 2026-10-28 01:54:41 +07).
  Không tải lại bundle: receipt kiểm đã có trong audit
  `trial-bundle-audit.json` nêu ở bảng gate (PASS_SCOPED,
  phạm vi hẹp, overall NOT_VERIFIED). Link hết hạn không
  làm mất receipt audit, và cũng không tự thành bằng chứng
  còn truy cập được.
- Baseline: null, reason NOT_MEASURED. CLI tổng attempt-01:
  1.377s / 9 lệnh — không phải thời gian tiết kiệm.

## Cập nhật rev24 (2026-10-27, lớp IA này chưa nộp kênh)

- Docs DOC02/DOC03: đã đóng scoped (xem bảng gate trên).
- Packet trial attempt-02: commit `4f683e7e4a8910cd731d8f78c2ad387455252ce6`, submission `SUB-CTX-001-PACKET02-R0`, review `REV-CTX-001-PACKET02-R0` APPROVED_SCOPED, readiness `READY_FOR_BOUNDED_OWNER_REWRITE_TRIAL`, kênh rev24 (commit `d8af62221a4dfb2351225a4b357729f3437a9490`, blob `3c1bf83e0f110104240cbfdc151c9d0571f7ba47`), artifact review `51a42e46da5bdef3eb1bd3acc755abe699a00f3d`, nhánh `codex/ctx-001-packet02-r0-review`, guide `reviews/ctx-001/packet02-r0/OWNER_TEST_GUIDE.vi.md`.
- Rewrite attempt-02: `RW-74cd5f5b72e0e01c`, digest `74cd5f5b72e0e01cbe96d08742a0335320dc2dbd1247134691a592b4e8919e97`, review_status `DRAFT_NOT_REVIEWED`, KHÔNG proposal.
- Commit song song `5cc1b4d…` (docs, chưa nộp, chưa review) vẫn ở đầu nhánh trước packet commit; disposition của nó vẫn chờ quyết định owner, không thuộc bản IA này.

## Việc nguyên tử tiếp theo và người thực hiện

- Việc: owner quyết thật trên digest rewrite `74cd5f5b…` (cổng version 1): chọn APPROVE / REVISE / REJECT / DEFER kèm lý do nguyên văn và nhãn operator. Chỉ APPROVE thật trên đúng digest mới mở bước review rồi propose; packet được duyệt scoped không thay thế quyết định này.
- Người thực hiện: owner (NohFinl) quyết; sau đó Muse chạy review/propose và trial có giám sát theo `docs/ia/contextual-intake-current-use.md` và guide `OWNER_TEST_GUIDE.vi.md`. Các gate (local decision, evidence-review, owner feedback, product acceptance) vẫn báo riêng, không gộp thành một verdict chung.
