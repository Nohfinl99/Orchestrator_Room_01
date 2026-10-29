# Đọc Orchestrator_Room_01 trên GitHub

## 1. Mở đúng bản sao

Mở [Orchestrator_Room_01/main](https://github.com/Nohfinl99/Orchestrator_Room_01/tree/main),
rồi [START_HERE](../../START_HERE.md). Đây là bản sao đã tổ chức lại;
`main` frozen `8bd7d8a9…` trong hồ sơ là của repo gốc Orchestrator-Room.

## 2. Chọn tài liệu theo nhu cầu

- [Trạng thái](../ia/current-state.md): pins và gate snapshot rev24.
- [Issues](../ia/issues-and-next.md): việc chờ owner trong snapshot.
- [Luật contextual](../ia/contextual-intake-current-use.md) và
  [runbook Windows C6R1](windows-contextual-c6r1.vi.md): đường contextual.
- [Cách đọc ma trận](conceptual-and-acceptance-matrix.vi.md): phân biệt thiết kế,
  acceptance case và kết quả thực thi.
- [Reports](../reports/README.md), [evidence](../../evidence/README.md),
  [packet-02](../../packets/ctx-001-packet-02/PACKET_README.md): hồ sơ có sẵn.

## 3. Đọc trạng thái kèm phạm vi

Snapshot rev24 ghi DOC01/DOC02/DOC03 đã đóng scoped; packet-02 được
review APPROVED_SCOPED, nhưng rewrite `74cd5f5b…` vẫn DRAFT_NOT_REVIEWED.
Owner feedback và product acceptance vẫn PENDING. Không dùng hướng dẫn
đời trước để yêu cầu review DOC02/DOC03 lại như chưa có kết quả.

## 4. Khi cần nguồn lịch sử

Code, evidence và reviewer pins nằm trong
[source map](../ia/source-map.md), [review index](../reviews/index.md)
và [requirement index](../requirements/index.md).
Các link sang Orchestrator-Room cần quyền truy cập nguồn; chưa truy cập
được thì ghi chưa kiểm, không suy rằng review đã mất.

Tại GitHub, chọn commit SHA để đọc revision cố định; chọn nhánh để đọc
view của nhánh. Mở file xem nội dung; dùng Raw nếu cần bytes và kiểm
hash theo manifest. Ngày sửa file không thay pin.

## 5. Trial và giới hạn

Attempt-01 raw bundle ở ngoài repo; receipt audit ở pin requirement.
Link tải cũ đã hết hạn ngày 28/10/2026. Packet-02 trong repo là dạng
redacted/tham chiếu. Không tải lại hoặc yêu cầu owner gửi lại bundle
chỉ để đọc tài liệu; audit receipt không xác thực actor hoặc nghiệm thu.

Đọc repo không cần chạy CLI hay tạo approval. Các quyết định trial,
runtime và product acceptance cần scope riêng; chỉnh lý IA không mở gate.
