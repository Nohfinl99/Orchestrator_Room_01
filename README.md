# Orchestrator_Room_01

Bản sao lưu + sắp xếp lại theo IA của
[`Nohfinl99/Orchestrator-Room`](https://github.com/Nohfinl99/Orchestrator-Room),
nhánh `muse/local-control-room`, commit
`992b1d09d9fa1fe3bbaff289fbf8824728b07c4f` (2026-10-27).

Repo gốc giữ nguyên và vẫn là nơi lưu lịch sử git đầy đủ.
Repo này không merge ngược về repo gốc và không thay thế nó.

## Bắt đầu từ đâu

- [START_HERE.md](START_HERE.md) — điểm vào: mục tiêu, khả năng thật, trạng thái tổng.
- [docs/README.md](docs/README.md) — bản đồ toàn bộ cây `docs/` và bảng map đường cũ → đường mới.
- [docs/ia/README.md](docs/ia/README.md) — index lớp IA theo vai trò (người mới / owner / operator / reviewer).

## Bố cục (theo mẫu Reading_Companion: root chỉ giữ file điểm vào)

- `START_HERE.md`, `README.md` (tài liệu này) ở root.
- `docs/reports/` — báo cáo chạy từng đời (C5, C5R1, C6, C6R1, REV2–REV4).
- `docs/briefs/` — brief và ma trận acceptance intake (REV1/REV2).
- `docs/notes/` — handoff, instruction, receipt, changelog, nghiên cứu (kể cả README cũ của repo gốc).
- `docs/specs/` — đặc tả và policy (acceptance, architecture, pipeline, threat model, verification, pentest plan, pilot runbook).
- `docs/guides/` — runbook (kể cả `windows/` cho các supplement Windows cũ).
- `docs/data/` — manifest và template dữ liệu.
- `docs/ia/` — lớp Information Architecture (trạng thái, bản đồ nguồn, findings, glossary, log quyết định).
- `docs/reviews/`, `docs/requirements/` — index trỏ tới review và requirement pin ở repo/nhánh khác.
- `control_room/`, `tests/`, `acceptance/`, `fixtures/`, `scripts/` — code và test, giữ nguyên path.
- `evidence/`, `packets/` — evidence và packet kiểm chứng được, giữ nguyên path, KHÔNG di chuyển/đổi tên.

## Lưu ý provenance (đọc trước khi trích dẫn)

- Nội dung file được giữ nguyên byte so với repo gốc tại commit nguồn,
  trừ các tài liệu sống đã cập nhật link/path theo layout mới.
- Các pin commit/blob và tên nhánh nêu trong tài liệu (ví dụ C6R1
  `c7a837e3…`, evidence E6R1 `ea9c9464…`, kênh rev24) trỏ về repo
  gốc, không phải commit của repo này.
- Toàn hệ: NOT_VERIFIED. Product acceptance: PENDING. Cổng quyết
  định thật của owner trên digest rewrite `74cd5f5b…` (version 1)
  vẫn đang chờ ở kênh `ORCHESTRATOR_CHANNEL.md` của repo gốc.
