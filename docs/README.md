# Docs index — Orchestrator_Room_01

Bản đồ toàn bộ cây `docs/` của repo này (bản sao lưu đã sắp xếp
lại từ `Nohfinl99/Orchestrator-Room`, commit `992b1d09…`, 2026-10-27).
Root repo chỉ giữ `START_HERE.md` và `README.md`; mọi tài liệu
khác nằm dưới `docs/`, chia theo chủ đề, theo mẫu tổ chức của
repo Reading_Companion.

## Cây docs

- `docs/reports/` — báo cáo chạy từng đời.
- `docs/briefs/` — brief và ma trận acceptance intake.
- `docs/notes/` — handoff, instruction, receipt, changelog, nghiên cứu.
- `docs/specs/` — đặc tả và policy.
- `docs/guides/` — runbook hiện hành + `windows/` cho supplement Windows cũ.
- `docs/data/` — manifest và template dữ liệu.
- `docs/ia/` — lớp Information Architecture (xem [ia/README.md](ia/README.md)).
- `docs/reviews/` — index trỏ tới các nhánh review (report không nằm ở repo này).
- `docs/requirements/` — index trỏ tới pin requirement (không nằm ở repo này).
- `docs/archive/` — chỉ luật lưu trữ, chưa có snapshot nào.

## Bảng map đường cũ → đường mới (repo gốc → repo này)

Đường cũ là vị trí file ở repo gốc trước khi sắp xếp lại. Nội dung
file không đổi (giữ nguyên byte), chỉ đổi path — trừ các tài liệu
sống đã cập nhật link/path (START_HERE, docs/ia, docs/guides).

| Đường cũ (repo gốc) | Đường mới (repo này) |
|---|---|
| `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1.md` | `docs/briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1.md` |
| `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md` | `docs/briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md` |
| `PRODUCT_INTAKE_BRIEF_REV1.md` | `docs/briefs/PRODUCT_INTAKE_BRIEF_REV1.md` |
| `PRODUCT_INTAKE_BRIEF_REV2.md` | `docs/briefs/PRODUCT_INTAKE_BRIEF_REV2.md` |
| `PRODUCT_INTAKE_BRIEF_REV2_ADDENDUM_REV2_1.md` | `docs/briefs/PRODUCT_INTAKE_BRIEF_REV2_ADDENDUM_REV2_1.md` |
| `handoff-manifest.json` | `docs/data/handoff-manifest.json` |
| `painpoint-observation-template.json` | `docs/data/painpoint-observation-template.json` |
| `WINDOWS_RUN_GUIDE.md` | `docs/guides/windows/WINDOWS_RUN_GUIDE.md` |
| `WINDOWS_SUPPLEMENT_C3.md` | `docs/guides/windows/WINDOWS_SUPPLEMENT_C3.md` |
| `WINDOWS_SUPPLEMENT_C4_T3.md` | `docs/guides/windows/WINDOWS_SUPPLEMENT_C4_T3.md` |
| `WINDOWS_SUPPLEMENT_C5R1.md` | `docs/guides/windows/WINDOWS_SUPPLEMENT_C5R1.md` |
| `C5_IMPLEMENTATION_CHECKLIST.md` | `docs/notes/C5_IMPLEMENTATION_CHECKLIST.md` |
| `MUSE_HANDOFF.md` | `docs/notes/MUSE_HANDOFF.md` |
| `MUSE_KNOWLEDGE_RECEIPT.md` | `docs/notes/MUSE_KNOWLEDGE_RECEIPT.md` |
| `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` | `docs/notes/MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` |
| `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md` | `docs/notes/MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md` |
| `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md` | `docs/notes/MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md` |
| `MUSE_RUN_INSTRUCTIONS.md` | `docs/notes/MUSE_RUN_INSTRUCTIONS.md` |
| `OWNER_INPUT_NEEDED.md` | `docs/notes/OWNER_INPUT_NEEDED.md` |
| `OWNER_REVIEW_NOTE_REV2.md` | `docs/notes/OWNER_REVIEW_NOTE_REV2.md` |
| `PATCH_NOTE_F21.md` | `docs/notes/PATCH_NOTE_F21.md` |
| `README.md` | `docs/notes/README-LEGACY.md` |
| `REFERENCE_STUDY.md` | `docs/notes/REFERENCE_STUDY.md` |
| `REV2_CHANGELOG.md` | `docs/notes/REV2_CHANGELOG.md` |
| `ROADMAP_STATUS.md` | `docs/notes/ROADMAP_STATUS.md` |
| `RUN_REPORT.md` | `docs/reports/RUN_REPORT.md` |
| `RUN_REPORT_C5.md` | `docs/reports/RUN_REPORT_C5.md` |
| `RUN_REPORT_C5R1.md` | `docs/reports/RUN_REPORT_C5R1.md` |
| `RUN_REPORT_C6.md` | `docs/reports/RUN_REPORT_C6.md` |
| `RUN_REPORT_C6R1.md` | `docs/reports/RUN_REPORT_C6R1.md` |
| `RUN_REPORT_REV2.md` | `docs/reports/RUN_REPORT_REV2.md` |
| `RUN_REPORT_REV3.md` | `docs/reports/RUN_REPORT_REV3.md` |
| `RUN_REPORT_REV4.md` | `docs/reports/RUN_REPORT_REV4.md` |
| `ACCEPTANCE.md` | `docs/specs/ACCEPTANCE.md` |
| `ARCHITECTURE.md` | `docs/specs/ARCHITECTURE.md` |
| `PENTEST_PLAN.md` | `docs/specs/PENTEST_PLAN.md` |
| `PILOT_RUNBOOK.md` | `docs/specs/PILOT_RUNBOOK.md` |
| `PIPELINE.md` | `docs/specs/PIPELINE.md` |
| `THREAT_MODEL.md` | `docs/specs/THREAT_MODEL.md` |
| `VERIFICATION_POLICY.md` | `docs/specs/VERIFICATION_POLICY.md` |

Không đổi path: `START_HERE.md` (đã cập nhật provenance),
`control_room/`, `tests/`, `acceptance/`, `fixtures/`, `scripts/`,
`evidence/`, `packets/`, `docs/ia/`, `docs/guides/*.vi.md`,
`docs/reviews/index.md`, `docs/requirements/index.md`,
`docs/archive/README.md`.

Một hiệu đính so với bảng mapping lúc đề xuất: `ROADMAP_STATUS.md`
bị sót trong bảng lúc đầu, đã cho vào `docs/notes/` cùng nhóm notes.
