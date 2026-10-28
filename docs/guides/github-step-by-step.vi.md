# Hướng dẫn GitHub từng bước cho owner — Orchestrator-Room

Hướng dẫn này chỉ để đọc và kiểm tra, không hướng dẫn
merge. Không có bước nào ở đây yêu cầu merge để “hoàn
tất” — merge là quyết định riêng của owner, chưa được
yêu cầu và chưa được duyệt. Tài liệu này cũng không dùng
screenshot giả: các nút được mô tả bằng tên hiển thị
trên GitHub.

Điều kiện trước: bạn cần quyền truy cập repository private
`Nohfinl99/Orchestrator-Room` bằng tài khoản GitHub đã
được cấp quyền. Nếu một link dưới đây hiện 404 trong khi
bạn chưa đăng nhập hoặc dùng tài khoản khác, đó thường
là vấn đề quyền truy cập, không phải file đã biến mất.

## Bước 1 — Mở đúng repository private

- Thao tác: mở link repository:
  https://github.com/Nohfinl99/Orchestrator-Room
- Kết quả cần nhìn thấy: trang repository hiện tên
  `Nohfinl99 / Orchestrator-Room` và ghi là Private.
  Nếu hiện 404, kiểm tra lại tài khoản đang đăng nhập và
  quyền truy cập repo trước khi kết luận file thiếu.

## Bước 2 — Chọn đúng nhánh Muse; hiểu vì sao main có thể chưa chứa kết quả mới

- Thao tác: mở link nhánh Muse:
  https://github.com/Nohfinl99/Orchestrator-Room/tree/muse/local-control-room
  (hoặc trên trang repo, bấm nút chọn nhánh — thường hiển
  thị `main` lúc đầu — rồi gõ `muse/local-control-room`).
- Kết quả cần nhìn thấy: tên nhánh hiển thị là
  `muse/local-control-room`, và trong danh sách file có
  `START_HERE.md`.
- Vì sao main có thể chưa chứa kết quả mới: mọi công việc
  C5/C5R1/supplement/trial đều nộp lên nhánh Muse này
  theo thiết kế, và không có merge nào được thực hiện.
  Nhánh `main` vẫn giữ bản frozen cũ
  (`8bd7d8a9fcdff34ef6ed1626050c2371661ab279`) nên việc
  bạn không thấy file mới ở `main` là bình thường, không
  phải lỗi. Đừng chuyển sang `main` để tìm kết quả mới,
  và đừng bấm Merge để “đồng bộ” khi chưa có quyết định
  merge riêng.

## Bước 3 — Mở START_HERE.md

- Thao tác: mở link:
  https://github.com/Nohfinl99/Orchestrator-Room/blob/muse/local-control-room/START_HERE.md
- Kết quả cần nhìn thấy: mục tiêu, khả năng thực tế và
  giới hạn, trạng thái tổng NOT_VERIFIED, pins hiện hành
  C6R1/E6R1 và pins lịch sử C5R1/E5R1/supplement, đường
  đọc nhanh sang các tài liệu IA, và link tới guide
  current-use contextual + runbook Windows contextual.
  Đây là điểm bắt đầu, không phải bằng chứng kỹ thuật.

## Bước 4 — Xem current state, gate và next action

- Thao tác: mở link:
  https://github.com/Nohfinl99/Orchestrator-Room/blob/muse/local-control-room/docs/ia/current-state.md
- Kết quả cần nhìn thấy: bảng pins hiện hành C6R1/E6R1
  và lịch sử C5R1; bảng gate đã qua theo scope (C6R1
  completed checks đạt nhưng full-scope NOT_RUN; DOC01
  CLOSED_SCOPED; DOC02/DOC03 đang chờ docs review);
  bảng gate pending (docs review, feedback, product
  acceptance, merge); và một việc nguyên tử tiếp theo
  cùng người thực hiện (Codex review docs DOC02/DOC03,
  sau đó Muse chuẩn bị trial contextual có giám sát).
  Lưu ý: evidence-review gate của attempt-01 đã có
  receipt PASS_SCOPED theo audit (phạm vi hẹp, overall
  NOT_VERIFIED) — việc tải bundle attempt-01 KHÔNG còn
  là việc tiếp theo, đừng tải lại hay yêu cầu relay.
- Lưu ý: đọc gate luôn kèm scope. Một dòng PASS ở scope
  hẹp không có nghĩa toàn hệ PASS.

## Bước 5 — Tìm đúng code commit, evidence commit và reviewer verdict

- Thao tác: mở từng link commit sau (mỗi link là một
  commit duy nhất, không phải nhánh):
  - Code hiện hành C6R1:
    https://github.com/Nohfinl99/Orchestrator-Room/commit/c7a837e3538aa6902c24ec4fd3fd8fd1cd047255
  - Evidence hiện hành E6R1:
    https://github.com/Nohfinl99/Orchestrator-Room/commit/ea9c9464b14eb93bf4efe6b00bf6ce73e59218e7
  - Code C6 (trước C6R1):
    https://github.com/Nohfinl99/Orchestrator-Room/commit/385f503b003479d4ae957d97cf3657e3900e1a37
  - Evidence E6 (trước C6R1):
    https://github.com/Nohfinl99/Orchestrator-Room/commit/da2d318cdad0ea268e8fc709f59fc1462321f4c9
  - Docs sửa DOC01:
    https://github.com/Nohfinl99/Orchestrator-Room/commit/1cfcb871b60c5871bf7b4d98208f7cc10586aa9f
  - Code C5R1 (lịch sử):
    https://github.com/Nohfinl99/Orchestrator-Room/commit/fd3430c9f1b0e98d1f6c9c62067b935f20054498
  - Evidence E5R1 (lịch sử):
    https://github.com/Nohfinl99/Orchestrator-Room/commit/dde7b605b0ef9c97e3ae91156303638f3ba843fd
  - Windows supplement C5R1 (lịch sử):
    https://github.com/Nohfinl99/Orchestrator-Room/commit/cc6591cbfbe7faf9315c3171dff69c7062ddb2c2
  - Reviewer commit C5R1 (lịch sử, nhánh reviewer, không phải nhánh Muse):
    https://github.com/Nohfinl99/Orchestrator-Room/commit/6a48b3f07bd67110b8c8b95768db712994e76499
- Kết quả cần nhìn thấy ở mỗi commit: message commit,
  danh sách file thay đổi, và không có thay đổi nào sang
  `main` hay `Orchestrator_Reverse`. Commit C6R1 chỉ đổi
  5 file code/tests/tooling; commit E6R1 chỉ đổi report +
  evidence; commit docs DOC01 chỉ đổi 1 file docs mới.
- Reviewer verdict hiện hành (R1): mở báo cáo review trên
  nhánh reviewer:
  https://github.com/Nohfinl99/Orchestrator-Room/blob/codex/ctx-001-r1-review/reviews/ctx-001/r1/REPORT.md
  và tìm verdict `APPROVED_SCOPED` (F01–F03
  CLOSED_SCOPED, DOC01 OPEN_NONBLOCKING_DOCS lúc đó).
  Review docs DOC01 (kênh rev11, `CHANGES_REQUESTED_DOCS_ONLY`)
  nằm trong file kênh:
  https://github.com/Nohfinl99/Orchestrator-Room/blob/codex/orchestrator-channel/ORCHESTRATOR_CHANNEL.md
  — tìm `REV-CTX-001-DOC01`.
- Reviewer verdict C5R1 (lịch sử): mở báo cáo review trên
  nhánh reviewer:
  https://github.com/Nohfinl99/Orchestrator-Room/blob/codex/c5r1-owner-pilot/reviews/2026-10-26-c5r1/REPORT.md
  và tìm verdict `READY_FOR_BOUNDED_OWNER_TRIAL`.
  Verdict này chỉ là readiness cho trial có giám sát —
  không phải full PASS, VERIFIED, product acceptance hay
  merge approval. Nếu bạn chỉ thấy link nhánh reviewer mà
  không thấy file, kiểm tra lại tên nhánh ở nút chọn
  nhánh.

## Bước 6 — Đọc trial input → proposal → decision → history → feedback

Trial attempt-01 KHÔNG nằm trong repo. **Không tải lại
bundle và không yêu cầu relay:** bundle đã được kiểm,
receipt là file audit:
https://github.com/Nohfinl99/Orchestrator-Room/blob/codex/ia-context-audit/docs/reviews/2026-10-26-ia-context/trial-bundle-audit.json
(pin `0a9729772b4598c771a5b7b49b62e46c8ae47a38`).
Audit kết luận evidence_review_gate `PASS_SCOPED`:
13 manifest entries khớp, file set exact, history
recomputed chain_valid true (event_count 3), raw stdout
khớp store, zip 10773 bytes SHA-256
`e428fa8a01c5d3289bb62343253e9dca3722a9cd0205985210340967369b9909`.
Phạm vi audit chỉ là bundle consistency, manifest
custody, deterministic binding và history recomputation —
KHÔNG xác thực actor và KHÔNG quan sát độc lập quá trình
chạy gốc; overall vẫn NOT_VERIFIED. Các bước dưới đây
là cách audit ĐÃ LÀM, ghi lại để hiểu, không phải việc
cần làm lại:

1. (Đã làm) Tải evidence bundle attempt-01 từ link Muse
   storage (link có hạn, hết hạn 2026-10-28 01:54:41 +07)
   và đối chiếu: file zip 10773 bytes, SHA-256 như trên.
   Nếu hash khác, bundle đó không dùng được làm bằng
   chứng.
2. (Đã làm) Giải nén và mở `MANIFEST.json` trước: manifest
   liệt kê 13 file kèm SHA-256 và byte length, tự loại trừ
   chính nó, và nêu riêng code pin C5R1. Đối chiếu hash
   từng file trong bundle với manifest trước khi đọc nội
   dung.
3. Đọc theo thứ tự: `owner-request.redacted.txt` (input,
   504 bytes, SHA-256 `2bf4740b…`) → `INPUT_PROVENANCE.json`
   (nguồn gốc: owner KHÔNG gửi file gốc; file được tạo từ
   tin nhắn theo chỉ thị, kèm quy tắc serialization) →
   `decision-record.json` (decision `DEC-6e42be7ab458849f`,
   APPROVE, provenance `OPERATOR_ASSERTED`, operator
   `NohFinl`) → `decide.stdout.txt` / `decide.stderr.txt` /
   `decide.meta.json` (raw outputs của decide) →
   `verify-history.stdout.txt` (chain_valid true,
   event_count 3) → `overview-final.stdout.txt`
   (counts 1/1/1, stage INTAKE) → `room.json` cuối
   (SHA-256 `a182794e…`).
4. Feedback: feedback KHÔNG có trong bundle và vẫn đang
   PENDING (file `FEEDBACK.md` trong bundle chuẩn bị vẫn
   trống). Đừng tìm feedback trong zip, và đừng coi
   decision `OPERATOR_ASSERTED` là product acceptance.
5. Báo cáo tổng của attempt (`OUTCOME.md`) nằm trong
   workspace của Muse (ngoài repo, ngoài zip) và đã được
   gửi kèm trong chat; nếu cần đọc lại, hỏi Muse gửi lại
   file đó thay vì tìm trong repo.

## Bước 7 — Phân biệt xem file, tải file và xem lịch sử commit

- Xem file: bấm tên file trong danh sách của nhánh để mở
  trang xem file (blob view). Bạn đọc nội dung ngay trên
  trang, không cần tải về. Đây là cách đọc tài liệu IA và
  report.
- Tải file: trên trang xem file, bấm nút `Raw` (xem nội
  dung thô) rồi lưu lại, hoặc bấm nút `Download` (biểu
  tượng tải xuống) nếu có. Sau khi tải, đối chiếu SHA-256
  với manifest (đối với evidence) trước khi dùng file.
  Tải về máy không tự động tạo bằng chứng mới.
- Tải toàn bộ nhánh: trên trang repo/nhánh, bấm nút
  `Code` rồi chọn `Download ZIP`. Cách này tải snapshot
  của nhánh tại thời điểm đó; muốn biết chính xác commit
  nào, kiểm tra commit ở Bước 5 thay vì tin tên file zip.
- Xem lịch sử commit: trên trang nhánh, bấm `Commits`
  để xem danh sách commit theo thời gian (mới nhất lên
  đầu). Bấm một commit để xem message, file đổi và diff.
  Lịch sử này cho biết cái gì đã đổi, khi nào, ở commit
  nào — nhưng ngày giờ commit không thay thế pin và
  manifest khi xác minh bằng chứng.
- Không bấm Merge, không tạo pull request để “hoàn tất”.
  Việc merge (nếu có) là một quyết định riêng của owner,
  cần chỉ thị rõ, và không nằm trong hướng dẫn này.
