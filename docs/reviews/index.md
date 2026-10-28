# Index review — Orchestrator-Room

Report review của Codex KHÔNG nằm ở nhánh này — chúng nằm
ở các nhánh review riêng (`codex/*-review`). Tài liệu này
chỉ trỏ tới đó bằng pin, không sao chép nội dung review.
Muốn đọc verdict đầy đủ thì đọc report tại nhánh và pin
đã nêu; muốn biết review nào là mới nhất thì đọc CONTROL
trên kênh `ORCHESTRATOR_CHANNEL.md` (nhánh
`codex/orchestrator-channel`), không đọc ngày sửa file.

## Review CTX-001 (kênh `ORCHESTRATOR_CHANNEL.md`)

| Review | Trả lời submission | Nhánh / artifact | Report | Verdict |
|---|---|---|---|---|
| `REV-CTX-001-R0` | `SUB-CTX-001-R0` (C6/E6) | `codex/ctx-001-r0-review`, artifact `ec6c0b6447c71113c1a865c0efe97303ddd46681` | `reviews/ctx-001/r0/REPORT.md` | CHANGES_REQUESTED (F01–F03) |
| `REV-CTX-001-R1` | `SUB-CTX-001-R1` (C6R1/E6R1) | `codex/ctx-001-r1-review`, artifact `17da045bb042fa1927cbd6f96028f3fb73537878` | `reviews/ctx-001/r1/REPORT.md` | APPROVED_SCOPED (F01–F03 CLOSED_SCOPED; DOC01 OPEN_NONBLOCKING_DOCS) |
| `REV-CTX-001-DOC01` | Docs DOC01 + ACK rev10 | Ghi trong kênh rev11; artifact branch không liệt kê ở đây — verify trước khi trích dẫn | Kênh rev11 | CHANGES_REQUESTED docs-only (DOC01 CLOSED_SCOPED; DOC02/DOC03 mới) |
| `REV-CTX-001-DOCS-R1` | `SUB-CTX-001-DOCS-R1` (docs `72495968…`) | `codex/ctx-001-docs-r1-review`, artifact `15ebf26944a379c8bbc3a3732e099f21c7fc45c4` | `reviews/ctx-001/docs-r1/REPORT.md` | CHANGES_REQUESTED docs-only (DOC02 CLOSED_SCOPED; DOC03 PARTIALLY_FIXED_OPEN) |
| `REV-CTX-001-DOCS-R2` | `SUB-CTX-001-DOCS-R2` (docs `dfedb46e…`) | `codex/ctx-001-docs-r2-review`, artifact `ee9b65d2e443920b01cf644607816377032bb10c` | `reviews/ctx-001/docs-r2/REPORT.md` | APPROVED_SCOPED (DOC01/DOC02/DOC03 đóng) |
| `REV-CTX-001-GATE01` | Event EVT-0018 (cổng WAITING_OWNER) | Chỉ ghi trong kênh rev19, không có artifact branch riêng | Kênh rev19 | CHANGES_REQUESTED coordination-only (cổng cũ không có cơ sở) |
| `REV-CTX-001-PACKET02-PRECHECK` | Event EVT-0020 (packet local-only) | Chỉ ghi trong kênh rev21 | Kênh rev21 | REVIEW_BLOCKED evidence access |
| `REV-CTX-001-PACKET02-R0` | `SUB-CTX-001-PACKET02-R0` (packet commit `4f683e7e…`) | `codex/ctx-001-packet02-r0-review`, artifact `51a42e46da5bdef3eb1bd3acc755abe699a00f3d` | `reviews/ctx-001/packet02-r0/REPORT.md` + guide `reviews/ctx-001/packet02-r0/OWNER_TEST_GUIDE.vi.md` | APPROVED_SCOPED, readiness `READY_FOR_BOUNDED_OWNER_REWRITE_TRIAL` |

## Quy tắc trích dẫn review

- Verdict luôn kèm scope: `APPROVED_SCOPED` không bao giờ
  được trích thành PASS toàn hệ.
- Review của Codex không phải quyết định của owner, không
  phải product acceptance, không phải merge approval.
- Review cũ không giải phóng task mới: reply phải có
  `in_reply_to_submission_id` đúng submission đã xét.
