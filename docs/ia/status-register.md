# Status register — file docs trong repo mới

Bảng này ghi trạng thái điều hướng của từng file docs trong repo
`Orchestrator_Room_01` (bản sao lưu đã sắp xếp lại từ repo gốc
`Nohfinl99/Orchestrator-Room`, commit `992b1d09…`, 2026-10-27).
Nó là công cụ điều hướng, KHÔNG phải verdict kỹ thuật. Cột
“Đường cũ” ghi vị trí file ở repo gốc trước khi sắp xếp lại,
để ai theo link/path cũ cũng tìm được file mới.

- **CURRENT:** dùng làm trạng thái / đường chạy hiện tại.
- **HISTORICAL:** chỉ dùng để hiểu quá khứ, không dùng làm
  trạng thái hiện tại.
- **SUPERSEDED-BY:** đã bị file khác thay thế (ghi rõ file thay thế).
- **CHƯA PHÂN LOẠI:** chưa có bằng chứng để phân loại; cần
  owner/reviewer xác nhận trước khi trích dẫn làm trạng thái.

## File docs (sau sắp xếp lại)

| File | Trạng thái | Ghi chú | Đường cũ ở repo gốc |
|---|---|---|---|
| `START_HERE.md` | CURRENT | Điểm vào repo, đã cập nhật provenance cho repo mới | `` |
| `README.md` | CURRENT (mới) | README mới của repo này (xem dưới); README cũ chuyển xuống docs/notes/ | `` |
| `docs/reports/RUN_REPORT_C6R1.md` | CURRENT | Report cho code hiện hành C6R1 | `RUN_REPORT_C6R1.md` |
| `docs/briefs/PRODUCT_INTAKE_BRIEF_REV2.md` | CURRENT | Brief template đang dùng | `PRODUCT_INTAKE_BRIEF_REV2.md` |
| `docs/briefs/PRODUCT_INTAKE_BRIEF_REV2_ADDENDUM_REV2_1.md` | CURRENT | Addendum gắn với brief REV2 | `PRODUCT_INTAKE_BRIEF_REV2_ADDENDUM_REV2_1.md` |
| `docs/briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md` | CURRENT | Matrix đi cặp với brief REV2 | `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md` |
| `docs/notes/README-LEGACY.md` | HISTORICAL | README cũ của repo gốc, giữ nguyên làm lịch sử | `README.md` |
| `docs/notes/ROADMAP_STATUS.md` | HISTORICAL | Nguồn lịch sử trong source-map | `ROADMAP_STATUS.md` |
| `docs/reports/RUN_REPORT_C5.md` | HISTORICAL | Report cho code C5, đã qua | `RUN_REPORT_C5.md` |
| `docs/reports/RUN_REPORT_C5R1.md` | HISTORICAL | Report cho code C5R1, đã qua | `RUN_REPORT_C5R1.md` |
| `docs/reports/RUN_REPORT_C6.md` | HISTORICAL | Report cho code C6, đã qua | `RUN_REPORT_C6.md` |
| `docs/reports/RUN_REPORT.md` | HISTORICAL | Report cũ, superseded-by RUN_REPORT_C6R1.md | `RUN_REPORT.md` |
| `docs/reports/RUN_REPORT_REV2.md` | HISTORICAL | Report đời REV2, đã qua | `RUN_REPORT_REV2.md` |
| `docs/reports/RUN_REPORT_REV3.md` | HISTORICAL | Report đời REV3, đã qua | `RUN_REPORT_REV3.md` |
| `docs/reports/RUN_REPORT_REV4.md` | HISTORICAL | Report đời REV4, đã qua | `RUN_REPORT_REV4.md` |
| `docs/briefs/PRODUCT_INTAKE_BRIEF_REV1.md` | SUPERSEDED-BY docs/briefs/PRODUCT_INTAKE_BRIEF_REV2.md | Brief đời REV1 | `PRODUCT_INTAKE_BRIEF_REV1.md` |
| `docs/briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1.md` | SUPERSEDED-BY docs/briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md | Matrix đời REV1 | `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1.md` |
| `docs/notes/MUSE_KNOWLEDGE_RECEIPT.md` | HISTORICAL | Receipt đọc repo, không phải trạng thái | `MUSE_KNOWLEDGE_RECEIPT.md` |
| `docs/notes/MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` | HISTORICAL | Receipt bổ sung | `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` |
| `docs/notes/MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md` | HISTORICAL | Receipt bổ sung REV3 | `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md` |
| `docs/notes/MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md` | HISTORICAL | Receipt bổ sung REV4 | `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md` |
| `docs/notes/C5_IMPLEMENTATION_CHECKLIST.md` | HISTORICAL | Checklist đời C5 | `C5_IMPLEMENTATION_CHECKLIST.md` |
| `docs/notes/PATCH_NOTE_F21.md` | HISTORICAL | Note đời F21 | `PATCH_NOTE_F21.md` |
| `docs/guides/windows/WINDOWS_SUPPLEMENT_C3.md` | HISTORICAL | Supplement đời C3 | `WINDOWS_SUPPLEMENT_C3.md` |
| `docs/guides/windows/WINDOWS_SUPPLEMENT_C4_T3.md` | HISTORICAL | Supplement đời C4/T3 | `WINDOWS_SUPPLEMENT_C4_T3.md` |
| `docs/guides/windows/WINDOWS_SUPPLEMENT_C5R1.md` | HISTORICAL | Supplement C5R1, đã ghi là lịch sử trong current-state | `WINDOWS_SUPPLEMENT_C5R1.md` |
| `docs/guides/windows/WINDOWS_RUN_GUIDE.md` | HISTORICAL | Guide đời C3; đường Windows hiện hành nằm ở docs/guides/ | `WINDOWS_RUN_GUIDE.md` |
| `docs/specs/PENTEST_PLAN.md` | KẾ HOẠCH (CHƯA CHẠY) | Plan pentest tồn tại; bản thân pentest vẫn NOT_RUN | `PENTEST_PLAN.md` |
| `docs/specs/ACCEPTANCE.md` | CHƯA PHÂN LOẠI | Chưa có bằng chứng để phân loại | `ACCEPTANCE.md` |
| `docs/specs/ARCHITECTURE.md` | CHƯA PHÂN LOẠI | Chưa có bằng chứng để phân loại | `ARCHITECTURE.md` |
| `docs/notes/MUSE_HANDOFF.md` | CHƯA PHÂN LOẠI | Từng là instruction cho task trước; chưa xác minh còn hiệu lực | `MUSE_HANDOFF.md` |
| `docs/notes/MUSE_RUN_INSTRUCTIONS.md` | CHƯA PHÂN LOẠI | Từng là instruction cho task trước; chưa xác minh còn hiệu lực | `MUSE_RUN_INSTRUCTIONS.md` |
| `docs/notes/OWNER_INPUT_NEEDED.md` | CHƯA PHÂN LOẠI | Chưa xác minh input còn cần hay đã xong | `OWNER_INPUT_NEEDED.md` |
| `docs/notes/OWNER_REVIEW_NOTE_REV2.md` | CHƯA PHÂN LOẠI | Chưa xác minh còn hiệu lực | `OWNER_REVIEW_NOTE_REV2.md` |
| `docs/specs/PILOT_RUNBOOK.md` | CHƯA PHÂN LOẠI | Runbook pilot; chưa xác minh còn là đường chạy hiện hành | `PILOT_RUNBOOK.md` |
| `docs/specs/PIPELINE.md` | CHƯA PHÂN LOẠI | Chưa có bằng chứng để phân loại | `PIPELINE.md` |
| `docs/notes/REFERENCE_STUDY.md` | CHƯA PHÂN LOẠI | Chưa có bằng chứng để phân loại | `REFERENCE_STUDY.md` |
| `docs/notes/REV2_CHANGELOG.md` | CHƯA PHÂN LOẠI | Chưa có bằng chứng để phân loại | `REV2_CHANGELOG.md` |
| `docs/specs/THREAT_MODEL.md` | CHƯA PHÂN LOẠI | Tài liệu policy; chưa xác minh trạng thái hiện hành | `THREAT_MODEL.md` |
| `docs/specs/VERIFICATION_POLICY.md` | CHƯA PHÂN LOẠI | Tài liệu policy; chưa xác minh trạng thái hiện hành | `VERIFICATION_POLICY.md` |
| `docs/data/handoff-manifest.json` | CHƯA PHÂN LOẠI | File dữ liệu, trạng thái theo từng lần dùng | `handoff-manifest.json` |
| `docs/data/painpoint-observation-template.json` | CHƯA PHÂN LOẠI | File template, trạng thái theo từng lần dùng | `painpoint-observation-template.json` |

## Thư mục (không đổi so với repo gốc)

| Thư mục | Trạng thái | Ghi chú |
|---|---|---|
| `control_room/` | CURRENT (code C6R1) + HISTORICAL (note C5/C5R1 bên trong) | Code hiện hành C6R1; note cũ giữ nguyên làm lịch sử |
| `tests/` | CURRENT | Suite hiện hành (C6R1) + tests C4/C5 giữ nguyên |
| `acceptance/` | CURRENT | Runner acceptance hiện hành (C6) + runner C5 |
| `fixtures/` | HISTORICAL (F21) | Fixtures intake-rev2 đời F21; xem source-map |
| `evidence/` | Xem [../../evidence/README.md](../../evidence/README.md) | Evidence frozen xác định bằng commit repo gốc, không bằng path |
| `packets/` | Xem [../../packets/README.md](../../packets/README.md) | Packet kiểm chứng được, index riêng |
| `docs/` | Xem [README.md](../README.md) | Lớp IA + guides, index toàn bộ docs |
| `scripts/` | CURRENT (tooling) | Runner Windows + test runner |

## Bổ sung điều hướng 29/10/2026

Các README nhóm docs, [guide ma trận](../guides/conceptual-and-acceptance-matrix.vi.md)
và [changes index](../changes/README.md) là NAVIGATION_ONLY, không phải verdict.
Các hợp đồng đề xuất mang nhãn CURRENT phía trên không đồng nghĩa APPROVED.
Các tài liệu chưa phân loại vẫn giữ nguyên trạng thái. Phạm vi nhánh và pin
lịch sử tra [source map](source-map.md).
