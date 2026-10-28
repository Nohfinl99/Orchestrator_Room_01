# Bản đồ nguồn — Orchestrator-Room

Mỗi nguồn có revision, locator, phạm vi claim và tình trạng
truy cập. “Hiện hành” nghĩa là dùng để đọc trạng thái hiện
tại; “lịch sử” nghĩa là chỉ dùng để hiểu quá khứ, không
dùng làm trạng thái hiện tại. Ngày sửa file và tên “latest”
không phải nguồn trạng thái.

## A. Lớp đọc hiện hành (revision docs này, docs-only)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| `START_HERE.md` | Revision docs này, nhánh `muse/local-control-room` | Điều hướng + trạng thái tổng, không phải verdict kỹ thuật | Trong nhánh Muse (collaborator của repo private) |
| `docs/ia/current-state.md` | Revision docs này | Pins, bảng gate, việc tiếp theo | Trong nhánh Muse |
| `docs/ia/source-map.md` (tài liệu này) | Revision docs này | Bản đồ nguồn, không tự tạo bằng chứng | Trong nhánh Muse |
| `docs/ia/roles-and-gates.md` | Revision docs này (không đổi nội dung luật) | Phân biệt vai trò/gate, không thay đổi luật | Trong nhánh Muse |
| `docs/ia/issues-and-next.md` | Revision docs này | Findings theo scope, backlog, một việc tiếp theo | Trong nhánh Muse |
| `docs/ia/contextual-intake-current-use.md` | Docs commit `1cfcb871…` (sửa DOC01), nhánh Muse | Luật current-use contextual, pins, giới hạn, handoff trial có giám sát | Trong nhánh Muse |
| `docs/guides/github-step-by-step.vi.md` | Revision docs này | Hướng dẫn đọc repo trên GitHub, không hướng merge | Trong nhánh Muse |
| `docs/guides/windows-contextual-c6r1.vi.md` | Revision docs này | Runbook Windows contextual C6R1 hiện hành | Trong nhánh Muse |
| `docs/guides/windows-local-run.vi.md` | Revision docs này (chỉ thêm banner lịch sử) | Hướng dẫn chạy local Windows với C5R1 frozen — LỊCH SỬ, không dùng cho đường contextual | Trong nhánh Muse |

## B. Code (frozen, không sửa trong lớp IA)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| `control_room/` (backend `ctx_*`, cli `ctx-*`, `C6R1_NOTE.md`) | C6R1 `c7a837e3…` — HIỆN HÀNH | Code contextual hiện hành; C6R1_NOTE ghi rõ fix F01–F03 và giới hạn (keyword heuristic, locator-only) | Trong nhánh Muse |
| `control_room/C6_NOTE.md` | C6 `385f503b…` | Ghi chú C6 gốc, trước C6R1 | Trong nhánh Muse |
| `tests/test_intake_c6r1.py` + `tests/test_intake_c6.py` (đã sửa ở C6R1) | C6R1 `c7a837e3…` | Tests contextual hiện hành (suite 83/83 Linux) | Trong nhánh Muse |
| `acceptance/run_acceptance_c6.py` (đã sửa ở C6R1) | C6R1 `c7a837e3…` | Runner acceptance contextual (24/24 completed + 2 NOT_RUN, exit 2) | Trong nhánh Muse |
| `control_room/` (backend, cli, `__init__` 0.5.1, README, `C5R1_NOTE.md`) | C5R1 `fd3430c9…` — LỊCH SỬ | Snapshot C5R1 trước contextual; C5R1_NOTE ghi rõ lệch checklist và giới hạn. Không phải code hiện hành cho đường contextual | Trong nhánh Muse |
| `control_room/C5_BUILD_NOTE.md` | C5 `0a3d5a4d…` (không đổi ở C5R1) | Thiết kế/lệch checklist của C5, lịch sử | Trong nhánh Muse |
| `tests/test_control_room.py` (C4 tests) | Không đổi ở C5R1 | Tests C4, lịch sử + hiện hành cho suite 36 | Trong nhánh Muse |
| `tests/test_intake_c5.py` (21 tests C5) | C5R1 `fd3430c9…` | Tests C5/C5R1 | Trong nhánh Muse |
| `acceptance/run_acceptance_c5.py` | C5R1 `fd3430c9…` | Runner acceptance, roots tách biệt, verdict NOT_RUN | Trong nhánh Muse |
| `fixtures/intake-rev2/` (39 files, MANIFEST SHA-256 `fd1716cb…`) | F21 `bef96ccf…` | Fixtures/schema/checker, subset validator (không phải JSON Schema đầy đủ) | Trong nhánh Muse |

## C. Evidence (không di chuyển, không đổi tên, không repin)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| `docs/reports/RUN_REPORT_C6R1.md` + `evidence/c6r1/` (5 files + MANIFEST) | E6R1 `ea9c9464…` — HIỆN HÀNH | Builder evidence Linux cho C6R1 + independent re-run; không phải reviewer verdict | Trong nhánh Muse |
| `docs/reports/RUN_REPORT_C6.md` + `evidence/c6/` | E6 `da2d318c…` | Builder evidence Linux cho C6 gốc, trước C6R1 | Trong nhánh Muse |
| `docs/reports/RUN_REPORT_C5R1.md` + `evidence/c5r1/` (11 files, MANIFEST riêng) | E5R1 `dde7b605…` — LỊCH SỬ | Builder evidence Linux cho C5R1; không phải reviewer verdict | Trong nhánh Muse |
| `docs/guides/windows/WINDOWS_SUPPLEMENT_C5R1.md` + `evidence/windows-c5r1/` (14 files copy reviewer + MANIFEST riêng) | Supplement `cc6591cb…` | Reviewer-run Windows evidence cho C5R1; Muse không chạy Windows | Trong nhánh Muse |
| `docs/reports/RUN_REPORT_C5.md` + `evidence/c5/` | E5 `18d74aa1…` | Builder evidence Linux cho C5; lịch sử, giữ FAIL Windows cũ | Trong nhánh Muse |
| `evidence/rev2-1/` và `evidence/rev2-1-f21/` | REV2.1 `0441decf…` / E21 `1e590765…` | Logs checker REV2.1/F21; Linux, không chứng minh Windows | Trong nhánh Muse |
| `evidence/windows-c4-t3/` + `docs/guides/windows/WINDOWS_SUPPLEMENT_C4_T3.md` | Packet REV2 `db1de0f6…` | Reviewer-run Windows C4/T3; lịch sử | Trong nhánh Muse |

## D. Tài liệu hợp đồng (PROPOSED, không phải APPROVED)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| `docs/briefs/PRODUCT_INTAKE_BRIEF_REV2.md` | Packet REV2, SHA-256 `cbdd8e84…` | Brief PROPOSED_NOT_APPROVED; identity domain cho C5/C5R1 | Trong nhánh Muse |
| `docs/briefs/PRODUCT_INTAKE_BRIEF_REV2_ADDENDUM_REV2_1.md` | REV2.1, SHA-256 `3a354836…` | Addendum PROPOSED_NOT_APPROVED (R2-01/02/03) | Trong nhánh Muse |
| `docs/notes/C5_IMPLEMENTATION_CHECKLIST.md` | REV2.1, SHA-256 `58bec316…` | Spec build C5, A01–A33 lúc viết là PROPOSED/NOT_RUN | Trong nhánh Muse |
| `docs/briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md` | Packet REV2, SHA-256 `f08e5668…` | Ma trận acceptance, runtime cases PROPOSED/NOT_RUN lúc viết | Trong nhánh Muse |
| `docs/notes/REV2_CHANGELOG.md` | Packet REV2, SHA-256 `fccc0436…` | Map BRI01–BRI05 → quyết định → file/case | Trong nhánh Muse |

## E. Tài liệu lịch sử (đọc để hiểu quá khứ, không lấy làm trạng thái)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| `docs/notes/ROADMAP_STATUS.md` | Cập nhật lần cuối ở packet REV2 (blob `11affbcc…` lúc kiểm F21) | Trạng thái roadmap tới REV2; đã được lớp IA này thay thế cho trạng thái hiện tại | Trong nhánh Muse |
| `control_room/README.md` (các mục trước C5R1) | C5R1 `fd3430c9…` (chỉ thêm đoạn trỏ C5R1_NOTE) | Tài liệu code; phần C5 là lịch sử, phần C5R1 trỏ sang C5R1_NOTE | Trong nhánh Muse |
| `docs/reports/RUN_REPORT_C5.md`, `docs/reports/RUN_REPORT_REV4.md` và các report cũ | Các commit E5/E4 tương ứng | Báo cáo builder từng lượt; không sửa sau khi nộp | Trong nhánh Muse |

## F. Nhánh reviewer (chỉ tham khảo, không nằm trong nhánh Muse)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| `reviews/ctx-001/r1/REPORT.md` | Nhánh `codex/ctx-001-r1-review`, artifact `17da045b…` | Báo cáo review R1: F01–F03 CLOSED_SCOPED, DOC01 OPEN_NONBLOCKING_DOCS lúc đó, verdict APPROVED_SCOPED | Nhánh reviewer (read-only reference) |
| `reviews/ctx-001/r0/REPORT.md` | Nhánh `codex/ctx-001-r0-review`, artifact `ec6c0b64…` | Báo cáo review R0: CHANGES_REQUESTED (F01–F03) | Nhánh reviewer (read-only reference) |
| `MUSE_AFTER_C5R1_REVIEW.md` | Nhánh `codex/c5r1-owner-pilot`, commit `6a48b3f0…` — LỊCH SỬ | Chỉ thị review C5R1, verdict READY_FOR_BOUNDED_OWNER_TRIAL | Nhánh reviewer (read-only reference) |
| `reviews/2026-10-26-c5r1/REPORT.md` | Cùng commit reviewer trên — LỊCH SỬ | Báo cáo review độc lập C5R1/E5R1 + Windows | Nhánh reviewer |
| `OWNER_PILOT_PROTOCOL.md` | Cùng commit reviewer trên — LỊCH SỬ | Protocol OWNER_TRIAL_01, lệnh Windows có quote | Nhánh reviewer |

## G. Trial ngoài repo (không nằm trong nhánh Muse)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| Bundle OWNER_TRIAL_01 (`PREPARATION`, `INPUT_PROVENANCE`, `BASELINE`, `RUNBOOK`, `FEEDBACK`, `OUTCOME`, `BACKLOG`, `attempts/README`) | Workspace của Muse, ngoài checkout | Chuẩn bị trial, không phải bằng chứng chạy | Chỉ trên máy Muse của owner, không reviewer-accessible trực tiếp |
| Attempt-01 (`attempts/attempt-01/`: request, provenance, `room.json`, logs, `OUTCOME.md`, `FEEDBACK.md` trống) | Workspace của Muse, ngoài checkout | Trial thật đã chạy tới decision; feedback trống | Chỉ trên máy Muse của owner |
| Evidence bundle attempt-01 (zip, 13 files + `MANIFEST.json` tự loại trừ) | Muse storage link (hết hạn 2026-10-28 01:54:41 +07), SHA-256 `e428fa8a01c5d3289bb62343253e9dca3722a9cd0205985210340967369b9909` | Raw evidence attempt-01 ĐÃ ĐƯỢC KIỂM theo audit dưới; KHÔNG tải lại | Audit là receipt; link hết hạn không làm mất receipt |
| `docs/reviews/2026-10-26-ia-context/trial-bundle-audit.json` | Pin `0a9729772b4598c771a5b7b49b62e46c8ae47a38` (nhánh `codex/ia-context-audit`) | Receipt kiểm bundle: evidence_review_gate `PASS_SCOPED` (13 entries, history chain_valid, raw stdout khớp store), scope hẹp, overall NOT_VERIFIED; owner_feedback PENDING; product_acceptance PENDING | Trong repo (nhánh IA context) |
| Template files (`trial/trial-request-redacted.txt`, `trial/trial-worksheet.md`) | Workspace của Muse, SHA-256 `85745787…` / `a8801b40…` | TEMPLATE/SYNTHETIC_PREPARATION do Muse viết; KHÔNG phải owner evidence | Chỉ trên máy Muse của owner |

## H. Nhánh main và repo tham khảo (frozen, không đổi)

| Nguồn | Revision / locator | Phạm vi claim | Truy cập |
|---|---|---|---|
| Nhánh `main` của Orchestrator-Room | `8bd7d8a9fcdff34ef6ed1626050c2371661ab279` | Main frozen; không chứa công việc nhánh Muse (chưa merge, không merge nào được duyệt) | Trong repo (collaborator) |
| `Nohfinl99/Orchestrator_Reverse` | HEAD `ede6f66d…` (read-only reference) | Candidate knowledge only, NOT_USED_FOR_DECISION; không sửa, không branch/commit/PR | Read-only reference |
| `Nohfinl99/Muse_knowledge` | Không dùng trong tuyến này | Không phải nguồn cho các packet IA này | Không áp dụng |
