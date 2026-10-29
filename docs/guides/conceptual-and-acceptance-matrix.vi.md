# Cách đọc mô hình khái niệm và Acceptance Matrix

Trong các entry, glossary và code contextual đã đối chiếu, chưa xác định
module mang tên chính thức Conceptual Matrix. Bảng dưới là mô hình giải
thích do lượt chỉnh lý này tổng hợp; không phải ma trận runtime mới.

| Lớp | Dữ liệu / trách nhiệm | Giới hạn đã đọc từ code và current-use |
|---|---|---|
| Intake | Raw bytes, SHA-256, owner statements | Không sửa raw để làm brief đẹp hơn |
| Assess | goal / context / scope / desired_output | Keyword substring scan; COMPLETE không chứng minh hiểu ngữ nghĩa |
| Context | Source locator, clarification, đáp án nguyên văn | Locator-only, không retrieval nội dung nguồn |
| Rewrite | Brief do operator soạn, digest và revision | Suy luận có nhãn; chưa có approval thì chưa proposal |
| Review | APPROVE / REVISE / REJECT / DEFER | OPERATOR_ASSERTED, không xác thực actor |
| Proposal | 3 task cố định của đường contextual | Không phân công live agent; legacy có 4 task |
| Audit | Bindings và event history | Hash không tự chứng minh ai đã phê duyệt |

Nguồn: [backend](../../control_room/backend.py),
[luật contextual](../ia/contextual-intake-current-use.md),
[roles/gates](../ia/roles-and-gates.md).

## Acceptance Matrix thực tế

[REV2 A01–A33](../briefs/PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md)
gắn yêu cầu với input, expected behavior và evidence cần thu. Đây là
hợp đồng đề xuất được giữ nguyên tại mốc viết; các chữ PROPOSED/NOT_RUN
trong file không phải bảng kết quả mới nhất của toàn dự án.

Đường contextual có [runner B01–B17](../../acceptance/run_acceptance_c6.py)
và [kết quả C6R1](../../evidence/c6r1/acceptance-results.json) riêng.
Không cộng case A với case B hoặc dùng kết quả B để tự đổi trạng thái A.

Chuỗi kiểm chứng: requirement/brief revision → case và oracle đã chọn →
input/command/environment → raw output/exit/hash → verdict theo scope →
quyết định owner riêng. Ma trận là bảng đối chiếu; runner và validator
thực thi kiểm tra, reviewer đánh giá evidence.

Kết quả đã lưu C6R1: 24 PASS, 2 NOT_RUN trên 26 subcase, full-scope NOT_RUN.
Đây là kết quả lịch sử, không phải chạy mới ngày 29/10/2026.
Negative control PASS nghĩa là đầu vào sai/giả mạo đã bị chặn đúng kỳ vọng.
