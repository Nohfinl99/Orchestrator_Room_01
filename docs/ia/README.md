# IA index — Orchestrator-Room (lớp Information Architecture)

> Lưu ý provenance (repo này): lớp IA này được sao chép nguyên
> từ repo gốc `Nohfinl99/Orchestrator-Room` (commit `992b1d09…`,
> 2026-10-27) trong đợt sắp xếp lại. Các pin commit/blob và
> tên nhánh nêu trong tài liệu trỏ về repo gốc, không phải
> commit của repo này.

Lớp IA này tổ chức đường đọc và ghi rõ trạng thái. Nó KHÔNG đóng
gate kỹ thuật nào, KHÔNG nghiệm thu sản phẩm, KHÔNG tạo verdict
mới. Trạng thái chỉ lấy từ pins, manifest và bảng gate — không
dùng ngày sửa file hay tên “latest” làm nguồn trạng thái.

## Đọc theo vai trò

- **Người mới:** [START_HERE.md](../../START_HERE.md) → tài liệu này →
  [current-state.md](current-state.md) → [source-map.md](source-map.md).
- **Owner:** [decisions.md](decisions.md) (quyết định đã có) →
  [current-state.md](current-state.md) (gate nào pending) →
  [issues-and-next.md](issues-and-next.md) (một việc tiếp theo).
- **Operator:** [contextual-intake-current-use.md](contextual-intake-current-use.md)
  → [../guides/windows-contextual-c6r1.vi.md](../guides/windows-contextual-c6r1.vi.md)
  → [../../packets/README.md](../../packets/README.md) →
  [../../evidence/README.md](../../evidence/README.md).
- **Reviewer:** [../reviews/index.md](../reviews/index.md) →
  [source-map.md](source-map.md) → pins trong
  [current-state.md](current-state.md).

## Bản đồ file IA

| File | Để làm gì |
|---|---|
| [START_HERE.md](../../START_HERE.md) | Điểm vào repo: mục tiêu, khả năng thật, trạng thái tổng, đường đọc nhanh |
| [README.md](README.md) (tài liệu này) | Index lớp IA theo vai trò |
| [current-state.md](current-state.md) | Pins, bảng gate, việc nguyên tử tiếp theo |
| [source-map.md](source-map.md) | Nguồn nào là hiện hành / lịch sử, claim nào thuộc phạm vi nào |
| [issues-and-next.md](issues-and-next.md) | Findings đã đóng theo scope, minor backlog, khoảng trống còn mở |
| [roles-and-gates.md](roles-and-gates.md) | Phân biệt vai trò thiết kế, vai trò mô phỏng và người/agent thật |
| [contextual-intake-current-use.md](contextual-intake-current-use.md) | Luật current-use contextual, pins, giới hạn, handoff trial có giám sát |
| [status-register.md](status-register.md) | Trạng thái từng file root: CURRENT / HISTORICAL / SUPERSEDED-BY / CHƯA PHÂN LOẠI |
| [glossary.md](glossary.md) | Thuật ngữ dùng trong repo, định nghĩa ngắn gọn |
| [decisions.md](decisions.md) | Log quyết định của owner kèm nguồn (số rev kênh / ngày) |
| [../reviews/index.md](../reviews/index.md) | Index trỏ tới các nhánh review và pin (report không nằm ở nhánh này) |
| [../requirements/index.md](../requirements/index.md) | Index trỏ tới pin requirement (không nằm ở nhánh này) |
| [../guides/github-step-by-step.vi.md](../guides/github-step-by-step.vi.md) | Hướng dẫn đọc repo trên GitHub, không hướng merge |
| [../guides/windows-contextual-c6r1.vi.md](../guides/windows-contextual-c6r1.vi.md) | Runbook Windows contextual C6R1 hiện hành |
| [../guides/windows-local-run.vi.md](../guides/windows-local-run.vi.md) | Hướng dẫn chạy local C5R1 trên Windows — LỊCH SỬ |

## Quy tắc của lớp IA (bắt buộc)

1. **Không di chuyển, không đổi tên file hiện có.** Các submission
   và review trên kênh đang trỏ tới đúng path đó; đổi path là
   vỡ locator. Trạng thái thay đổi được ghi trong
   [status-register.md](status-register.md), không bằng cách dời file.
2. **Không sửa lịch sử.** Khi có kết quả mới, cập nhật bảng gate
   bằng pin mới; không sửa claim cũ thành như chưa từng sai.
3. **Không tự nhận đóng.** Một finding chỉ đóng khi có review
   verdict ghi rõ; “fix trong revision này” không phải là đóng.
4. **Không gộp verdict.** Local decision, evidence-review, owner
   feedback và product acceptance báo riêng, không gộp thành
   một verdict chung hay toàn hệ PASS.
5. **Không merge/PR/main.** Nhánh này là nhánh làm việc của Muse;
   `main` giữ frozen, không chứa kết quả mới — đó là thiết kế
   có chủ đích.

## Bản IA này (gốc từ repo Orchestrator-Room, commit 992b1d09) gồm gì

- Mới: tài liệu này, `status-register.md`, `glossary.md`,
  `decisions.md`, `../reviews/index.md`,
  `../requirements/index.md`, `../../packets/README.md`,
  `../../evidence/README.md`, `../archive/README.md`.
- Cập nhật lên rev24: `current-state.md`, `issues-and-next.md`,
  `START_HERE.md` (mục trạng thái tổng + đường đọc nhanh).
- Không đổi: code, evidence, frozen commit, file hiện có nào
  ngoài 3 file cập nhật trên. Trong repo mới này, lớp IA là tài liệu tham chiếu được sao chép nguyên,
  không phải một submission kênh mới.
