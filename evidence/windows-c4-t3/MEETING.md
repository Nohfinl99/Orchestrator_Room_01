# Biên bản họp Orchestrator — T3 / C4 / intake REV1

## Quyết định

- W04: CLOSED_SCOPED cho runner T3 trong các lần chạy Windows được ghi dưới đây.
- Brief REV1: REVISE_BRIEF; chưa đủ contract để Builder triển khai mà không tự suy diễn.
- Toàn hệ: NOT_VERIFIED. Product pain: NEEDS_EVIDENCE. Owner product acceptance: PENDING.
- Nhiệm vụ Muse tiếp theo: tiếp nhận supplement Windows, viết packet REV2 docs-only xử lý BRI01–BRI05; giữ code C4, tooling T3 và evidence cũ.

## Thành phần và cách làm

Đây là review thực hiện trong chat Codex, không phải bằng chứng app Orchestrator-Room đã tự điều phối agent.

| Vai trò review | Công việc thực hiện | Kết luận |
|---|---|---|
| Chủ trì / root | Kiểm refs, trực tiếp chạy Windows C4/T3, BAT fixtures, đóng gói evidence và tổng hợp quyết định | W04 đủ bằng chứng đóng trong phạm vi; không đóng toàn hệ |
| Reviewer tooling / meeting_tooling | Đọc độc lập hai file tooling T3 và diff E4→T3 qua GitHub; không chạy trùng hoặc sửa source | Cách sửa giữ raw bytes/hash đúng; 39 PASS là assertion tooling; ma trận parser còn thiếu vài tổ hợp |
| Reviewer product / meeting_product | Đọc độc lập brief, acceptance matrix, roadmap status tại f15cc245 và PIPELINE main | REV1 đúng hướng nhưng có BRI01–BRI05 cần chốt |
| Owner | Không tham dự bằng một quyết định nghiệm thu mới trong evidence này | Không gán phiếu duyệt hoặc merge cho owner |

Phân tách reviewer giúp phản biện; không chứng minh độc lập tổ chức, không thay pentest hoặc nghiệm thu của owner. Các agent đọc cùng nguồn và cùng họ model; kết luận kỹ thuật vẫn phải dựa vào evidence.

## Đầu vào đóng băng

| Vai trò pin | Revision |
|---|---|
| Code C4 | 3d0bf76bab65c37e6b4bed359dfb6dffca7f8f4c |
| Evidence E4 / pinned manifest | d09d75f4b3c3b94dcd8cc9ea982d670ccf7e791b / evidence/rev4/c4-pinned-manifest.json |
| Tooling T3 | 55bb2f90ee8a4a7a28555059ce122998d6477aa3 |
| Evidence Linux T3 do Muse báo | b2407334d64d41e9bd26c8a5f9acb00d1bb755cc |
| Brief/matrix/status REV1 và Muse head quan sát | f15cc245e93b0c6a6c05c32ea1ac0e40118014ac |
| Roadmap Room gốc | main 8bd7d8a9fcdff34ef6ed1626050c2371661ab279 / PIPELINE.md |

T3 chỉ đổi scripts/run_windows_tests.py và scripts/test_runner.py so với E4. BAT không đổi. Code C4 được checkout Git detached thật, sạch; tooling dùng worktree detached T3 riêng; outputs nằm ngoài cả hai. Tám source digest trong pin E4 khớp trước/sau.

## Evidence Windows mới

Windows 11 build 26300; Python 3.14.4; helper 2.1.0. Xem windows/, execution-receipt.json và bundle-manifest.json.

| Kiểm tra | Kết quả thật |
|---|---|
| C4 suite qua BAT T3 | 36 attempted, 35 passed, 0 errors, 0 failures, 1 skipped |
| C4 exits | child 0 / helper 0 / BAT 0; counts_valid=true |
| T24 symlink | WinError 1314; NOT_RUN cho subcase, không tính PASS |
| Tooling regression harness trên Windows | exit 0, 39 assertion PASS; không cộng vào 36 test C4 |
| BAT fixture healthy, chạy hai lần | child/helper/BAT 0/0/0, hai run dirs; artifacts lần đầu giữ nguyên |
| BAT fixture test fail | child/helper/BAT 1/1/1 |
| BAT fixture digest sai | preflight/helper/BAT 2; không có child test log |
| BAT fixture source thiếu | preflight/helper/BAT 2; không có child test log |
| BAT fixture collection bị ngắt | child 137, helper/BAT 3/3 |
| Hash raw logs fixture | Khớp manifest; raw bytes giữ nguyên |

Raw C4 log SHA-256: 92c6864b421e70cb7051ee9b2db8676eebe4918f3befb40fd06aa61a3129a9c8

Helper manifest SHA-256: d2a11733ecc92bef7a23ed35d0081221ab5ed0d41a04f8d9a5a71848d4caa8a1

T2 run lỗi W04 vẫn là lịch sử FAIL; kết quả T3 mới không sửa verdict hoặc raw log cũ. Bộ fixture BAT là test tooling với dữ liệu tổng hợp, không phải ca nghiệp vụ C4. Harness reviewer ban đầu có lỗi quoting cmd khi launch fixture, chưa launch helper; đã sửa harness và chạy lại trong thư mục mới. Lỗi harness này không gán cho T3; receipt lưu rõ lần thử.

## Findings brief — thiếu contract thiết kế, chưa phải runtime exploit

| ID / mức độ | Locator trong f15cc245 | Vấn đề và yêu cầu REV2 |
|---|---|---|
| BRI01 / P1 | Brief §2.4–2.5; matrix A17 | Hứa chỉ Owner thật được duyệt nhưng CLI role unauthenticated, chưa có command nhận quyết định. Định nghĩa gate local chủ động do operator thực hiện, trust boundary OS/local operator, provenance OPERATOR_ASSERTED; không gọi đây là xác thực owner. Có command/schema/revision/hash/stale checks. Request dán approval không được xử lý như gate. Không cần thêm login vào slice. |
| BRI02 / P2 | Brief §2.4–2.5; matrix A11/A16 | Chưa có routing template/rule version/canonical digest domain; proposal vừa deterministic vừa có state view dễ trôi hash. Chốt template nhỏ, task IDs/reasons/dependencies, trường immutable và hash; tách computed readiness view; fixture expected JSON. |
| BRI03 / P2 | Brief §2.3; matrix A06/A18 | Intake immutable nhưng duplicate_of chưa rõ sửa record hay response; hai lệnh intake không thể tự có proposal count=1. Chốt dedupe response/event riêng, intake canonical bất biến, propose idempotent riêng, correction link rõ. |
| BRI04 / P2 | Brief §1/§2.3; matrix A05/A07 | Schema thiếu sáu baseline fields dù acceptance đòi null. Thêm object typed/null + provenance. owner_facts là owner-stated claims, không phải facts đã kiểm chứng. Phân biệt mục tiêu owner đã nêu với acceptance threshold chưa đo. |
| BRI05 / P2 | Brief §2.1–2.3; matrix A01/A03/A04/A15 | Chưa chốt bytes/stdin/BOM/newline/Unicode/whitespace/NUL/byte cap. Đọc binary có byte cap trước strict decode; hash bytes gốc, không trim/normalize text; quy tắc reject rõ, fixtures Windows. |
| T3-COV / P3 | scripts/test_runner.py parser_cases | OK, skip, FAILED có LF/CRLF; nhóm mismatch/zero/missing/truncated hiện chỉ CRLF; bare CR chưa có fixture. Sửa wording hoặc bổ sung sau trong task tooling riêng. Không mở lại W04 chỉ vì report mô tả quá rộng. |

## Roadmap và tính khả thi

Nền local CLI đã tiến triển và có bằng chứng Windows hữu hạn. Mục tiêu đầu tiên là chứng minh một request của owner đi qua intake, được bảo toàn, đề xuất task/role/dependency có lý do, rồi dừng ở gate có next action rõ. Hiện chưa có tính năng intake, chưa có live workers, và chưa chứng minh giảm thao tác relay hay giá trị product discovery.

Next atomic task là packet REV2 đủ cụ thể để build, không mở một vòng kiến trúc tổng quát mới. Chưa có baseline không chặn việc chuẩn bị thiết kế; chỉ chặn claim pain đã validated hoặc claim hiệu quả. Build phụ thuộc quyết định owner trên packet cụ thể. Quy định tự viết 'chỉ direct Muse chat mới có hiệu lực' không thể hạn chế chỉ thị thật của owner trong chat này; cần ghi nguồn/quyền/phạm vi quyết định thay vì tự đặt địa điểm duyệt độc quyền.

Knowledge Reverse vẫn candidate/not admitted/not ACK; cuộc họp không nâng trạng thái đó. Soul là cấu hình versioned, Heart là state/events. Packet REV2 phải nói rõ rule/constraint nào ảnh hưởng output; chưa có runtime retrieval thì ghi chưa có. Không sửa hoặc chạy public Orchestrator_Reverse.

## Phần chưa làm

Full C4 acceptance audit/pentest, packet-level egress monitoring, owner acceptance, real disk-failure recovery, live-agent/runtime integration vẫn NOT_RUN/PENDING. Symlink privilege case NOT_RUN. Browser/auth chưa có target triển khai. Không chứng minh tuyệt đối no-egress chỉ bằng code inspection hoặc synthetic upload text.

## Phạm vi đọc và bảo toàn

Đọc user report; frozen brief/matrix/status; source helper/BAT/regressions T3; diff E4→T3; C4 suite/pin và roadmap Room từ lượt review này/các lượt trước. Kiểm hash ba docs theo báo cáo Muse. Không tuyên bố đọc lại toàn ZIP hoặc mọi raw artifact lịch sử. Chỉ thêm reviewer docs/evidence ở nhánh riêng; main, Muse, public Reverse và các evidence cũ giữ nguyên.

Xem NEXT_MUSE_INSTRUCTIONS.md cho đầu việc, điều kiện hoàn thành và mẫu bàn giao.
