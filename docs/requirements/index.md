# Index requirement — Orchestrator-Room

Requirement và IA review gốc KHÔNG nằm ở nhánh này — chúng
nằm ở pin requirement trên nhánh `codex/ia-context-audit`.
Tài liệu này chỉ trỏ tới đó bằng pin, không sao chép nội
dung requirement.

## Pin requirement (nguồn trạng thái cho CTX-001)

| Mốc | Pin |
|---|---|
| Requirement pin | `0a9729772b4598c771a5b7b49b62e46c8ae47a38` (nhánh `codex/ia-context-audit`) |
| Requirement contextual-intake | `docs/requirements/contextual-intake.md`, blob `ef07d493d1243485830152ef8abb3f6f2d23628d` |
| README hiện hành tại pin | `README_CURRENT.md`, blob `62f011560b54243c73fa8a53df504f978c572c23` |
| IA review REPORT tại pin | `docs/reviews/2026-10-26-ia-context/REPORT.md`, blob `4100098c064d82b1d210feb24ffb554dc124a9e8` |
| Trial bundle audit tại pin | `docs/reviews/2026-10-26-ia-context/trial-bundle-audit.json`, blob `c7b884c4…` (evidence_review_gate PASS_SCOPED, phạm vi hẹp: bundle consistency / manifest custody / binding / history recomputation — KHÔNG xác thực actor hay quan sát độc lập quá trình chạy gốc) |

## Quy tắc

- Requirement pin là nguồn, không phải bản sao ở nhánh này.
  Nếu nội dung requirement đổi thì pin đổi theo; không sửa
  lặng nội dung rồi giữ pin cũ.
- IA review tại pin là nguồn lịch sử cho lớp IA, không phải
  verdict kỹ thuật cho code hiện hành.
- Mọi claim về requirement phải kèm pin; không trích dẫn
  requirement bằng tên file hay ngày sửa.
