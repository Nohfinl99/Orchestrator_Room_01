# Orchestrator_Room_01

Phòng điều hành local cho quy trình tiếp nhận yêu cầu, làm rõ ngữ cảnh,
duyệt brief và chuẩn bị proposal. Lát cắt CLI hiện hành là C6R1;
toàn hệ **NOT_VERIFIED**, product acceptance **PENDING** theo snapshot rev24.

## Chọn đường đọc

| Cần làm gì? | Mở ở đâu? |
|---|---|
| Hiểu dự án và giới hạn | [START_HERE](START_HERE.md) |
| Xem snapshot trạng thái, gate, việc đang chờ | [Trạng thái](docs/ia/current-state.md) · [Issues](docs/ia/issues-and-next.md) |
| Chạy contextual intake theo runbook | [Hướng dẫn](docs/guides/README.md) |
| Hiểu ma trận và cách kiểm chứng | [Cách đọc ma trận](docs/guides/conceptual-and-acceptance-matrix.vi.md) |
| Đọc brief, kiến trúc, thiết kế | [Briefs](docs/briefs/README.md) · [Specs](docs/specs/README.md) |
| Đối chiếu kết quả đã lưu | [Reports](docs/reports/README.md) · [Evidence](evidence/README.md) · [Packets](packets/README.md) |
| Tìm toàn bộ tài liệu | [Docs index](docs/README.md) · [Bản đồ nguồn](docs/ia/source-map.md) |

## Bố cục

- `control_room/`: code CLI; `tests/`: suite; `acceptance/`: runners.
- `fixtures/`: input/golden/schema lịch sử; `scripts/`: tooling.
- `docs/`: IA, hướng dẫn, brief, thiết kế, báo cáo, hồ sơ và dữ liệu.
- `evidence/` và `packets/`: hồ sơ kiểm chứng; giữ nguyên đường dẫn và bytes.

## Repository này và nguồn gốc

Bản sao từ [Orchestrator-Room](https://github.com/Nohfinl99/Orchestrator-Room),
nhánh `muse/local-control-room`, commit nguồn
`992b1d09d9fa1fe3bbaff289fbf8824728b07c4f` (2026-10-27).
Lịch sử đầy đủ và các kênh review nằm ở repo gốc. Repo này có nhánh
`main` riêng để đọc bản đã sắp xếp; nó không thay thế hoặc merge ngược nguồn.

Các pin C6R1/E6R1, reviewer và packet vẫn thuộc repo gốc.
Các gate ở đây phản ánh snapshot đã sao lưu, không phải trạng thái live
của kênh nguồn. Quyết định owner trên rewrite `74cd5f5b…` vẫn chờ
trong snapshot; sửa tài liệu không tạo quyết định đó.

[Bản ghi chỉnh lý 29/10/2026](docs/changes/2026-10-29-navigation-repair.md).
