# Orchestrator_Room_01 — bắt đầu từ đây (bản sao lưu đã sắp xếp lại)

Repo này là bản sao lưu + sắp xếp lại theo IA từ
`Nohfinl99/Orchestrator-Room`, nhánh `muse/local-control-room`,
commit `992b1d09d9fa1fe3bbaff289fbf8824728b07c4f` (2026-10-27).
Nội dung file được giữ nguyên byte, trừ các tài liệu sống đã
cập nhật link/path theo layout mới (xem `docs/README.md`).
Các pin commit/blob trong tài liệu trỏ về repo gốc, không
phải commit của repo này; lịch sử git đầy đủ vẫn ở repo
gốc. Repo này không merge ngược về repo gốc và không thay
thế nó.

## Phạm vi bản sao và đường đọc mới

Các gate bên dưới là snapshot kế thừa tới kênh rev24 ở repo gốc;
không xác nhận trạng thái live ngày 29/10/2026. Nhánh `main` của
repo này khác `main` frozen của repo gốc.
Xem [docs index](docs/README.md), [hướng dẫn đọc GitHub](docs/guides/github-step-by-step.vi.md)
và [cách đọc ma trận](docs/guides/conceptual-and-acceptance-matrix.vi.md).

## Mục tiêu

Xây một lát cắt control-room chạy local: nhận một yêu cầu
bằng file hoặc stdin, lưu thành intake bất biến, tạo một
proposal theo template cố định 4 task (legacy — đường
template cố định cũ, không phải đường contextual hiện
hành; xem phần Khả năng thực tế bên dưới), rồi dừng ở cổng
operator để người vận hành đọc snapshot và tự quyết định.
Mọi dữ liệu là local và synthetic/redacted; không có provider,
network, background agent hay ghi ngoài theo mặc định.

## Khả năng thực tế (và giới hạn)

Có thật, đã chạy local bằng CLI Python stdlib-only:

- Intake có giới hạn (byte cap 20.000 trước decode, strict
  UTF-8, BOM bị từ chối, không trim nội dung đã chấp nhận),
  record bất biến, dedupe và correction bằng record mới
  (`--supersedes`, record cũ không sửa).
- Proposal theo template cố định 4 task, view tính toán lúc
  đọc, digest ràng buộc proposal với intake.
- Contextual intake (hiện hành, xem
  [current-use](docs/ia/contextual-intake-current-use.md)):
  assess bằng keyword heuristic → nguồn locator-only →
  hỏi 2–3 câu khi thiếu → đáp án nguyên văn → draft
  brief có cấu trúc → owner review đúng rewrite digest →
  proposal contextual ràng buộc raw + digest + answers.
  Draft do operator cung cấp, review là `OPERATOR_ASSERTED`,
  không phải hiểu ngữ nghĩa hay xác thực owner thật.
- Cổng decide với required `--expected-*` bindings lấy từ
  snapshot operator đã review; sai/lệch thì reject
  (stale → `REJECTED_STALE`, chỉ ghi event, không tạo
  decision), không tự lấy digest hiện tại, không
  default-approve.
- Audit: lock/CAS, history chain, `verify-history`,
  `overview` với `judge_scope` ghi rõ chỉ C4.

Chưa có, đừng suy ra từ tên gọi:

- Không có live worker, chat listener, scheduler, provider,
  runtime knowledge retrieval, hay điều phối agent thông
  minh. Proposal contextual có 3 task cố định theo luật (legacy có 4), không phải
  phân công agent theo ngữ nghĩa.
- Không có xác thực người dùng thật trong CLI: nhãn
  operator/role chỉ là tham số mô phỏng, provenance của
  decision là `OPERATOR_ASSERTED`, không phải
  `AUTHENTICATED_OWNER`.

## Trạng thái tổng

- **Toàn hệ: NOT_VERIFIED.**
- Hiện hành (current): code C6R1
  `c7a837e3538aa6902c24ec4fd3fd8fd1cd047255`, evidence
  E6R1 `ea9c9464b14eb93bf4efe6b00bf6ce73e59218e7`,
  reviewer verdict R1 `APPROVED_SCOPED` (artifact
  `17da045bb042fa1927cbd6f96028f3fb73537878`, nhánh
  `codex/ctx-001-r1-review`, report
  `reviews/ctx-001/r1/REPORT.md`); docs DOC01 đã đóng
  (guide current-use, commit docs
  `1cfcb871b60c5871bf7b4d98208f7cc10586aa9f`); docs
  DOC02 đã đóng (review DOCS-R1, kênh rev14) và DOC03
  đã đóng (review DOCS-R2 APPROVED_SCOPED, docs commit
  `dfedb46e64d0a8af6777cf4b43acb8630251db27`, kênh
  rev17); packet trial attempt-02 đã nộp và được duyệt
  (submission `SUB-CTX-001-PACKET02-R0`, review
  `REV-CTX-001-PACKET02-R0` APPROVED_SCOPED, readiness
  `READY_FOR_BOUNDED_OWNER_REWRITE_TRIAL`, kênh rev24);
  cổng quyết định thật của owner trên digest rewrite
  `74cd5f5b72e0e01cbe96d08742a0335320dc2dbd1247134691a592b4e8919e97`
  vẫn đang chờ (version 1).
- Lịch sử (C5R1, giữ frozen, không phải current): code
  `fd3430c9f1b0e98d1f6c9c62067b935f20054498`, evidence
  E5R1 `dde7b605b0ef9c97e3ae91156303638f3ba843fd`,
  Windows supplement C5R1 (docs/evidence only,
  reviewer-run) `cc6591cbfbe7faf9315c3171dff69c7062ddb2c2`,
  reviewer verdict READY_FOR_BOUNDED_OWNER_TRIAL (chỉ là
  readiness cho trial local có giám sát, không phải full
  PASS, VERIFIED, product acceptance hay merge approval).
- Trial OWNER_TRIAL_01 attempt-01: local decision gate đã
  thực thi (`DEC-6e42be7ab458849f`); evidence-review gate
  đã có receipt `PASS_SCOPED` theo audit (chỉ kiểm
  consistency/manifest/binding/history, KHÔNG xác thực
  actor hay quan sát độc lập quá trình chạy gốc); owner
  feedback PENDING; product acceptance PENDING.
- Trial OWNER_TRIAL_01 attempt-02 (contextual, ngoài checkout
  frozen): intake `INTAKE-0d0bcbe75d4fbee1`, clarification
  `CTXQ-4723da2edd3488b0` (đáp án tái dùng từ source, nhãn
  `REUSED_PRIOR_OWNER_STATEMENT`), draft `RW-74cd5f5b72e0e01c`,
  digest `74cd5f5b72e0e01cbe96d08742a0335320dc2dbd1247134691a592b4e8919e97`,
  review_status `DRAFT_NOT_REVIEWED`, KHÔNG proposal; packet
  kiểm chứng được tại `packets/ctx-001-packet-02/` (commit
  `4f683e7e4a8910cd731d8f78c2ad387455252ce6`), đã được duyệt
  scoped ở kênh rev24; quyết định thật của owner vẫn chờ.
- Lớp IA này không đóng gate kỹ thuật nào và không nghiệm
  thu sản phẩm. Nó chỉ tổ chức đường đọc và ghi rõ trạng
  thái.

## Đường đọc nhanh

0. [Contextual intake — current use](docs/ia/contextual-intake-current-use.md)
   — luật hiện hành (kể cả sửa DOC01), pins, giới hạn,
   và quy trình handoff trial có giám sát. Đọc tài liệu
   này trước khi chạy đường contextual.
1. [Trạng thái hiện hành](docs/ia/current-state.md) — pins,
   gate nào đã qua, gate nào pending, việc nguyên tử tiếp
   theo và người thực hiện.
2. [Bản đồ nguồn](docs/ia/source-map.md) — tài liệu nào là
   hiện hành, tài liệu nào là lịch sử, source/evidence/trial
   ở đâu, claim nào thuộc phạm vi nào, truy cập ra sao.
3. [Vai trò và gate](docs/ia/roles-and-gates.md) — phân biệt
   vai trò thiết kế, vai trò mô phỏng và người/agent thật
   sự thực hiện; tách task DONE, test PASS, operator
   decision và product acceptance.
4. [Issues và bước tiếp theo](docs/ia/issues-and-next.md) —
   findings đã đóng theo scope, minor backlog, một việc
   nguyên tử tiếp theo.
5. [IA index](docs/ia/README.md) — bản đồ toàn bộ lớp IA: trạng thái
   từng file root, glossary, log quyết định, index review /
   requirement / packet / evidence.
6. [Hướng dẫn GitHub cho owner](docs/guides/github-step-by-step.vi.md),
   [chạy contextual trên Windows (hiện hành)](docs/guides/windows-contextual-c6r1.vi.md)
   và [chạy local C5R1 trên Windows (lịch sử)](docs/guides/windows-local-run.vi.md).
   Đừng dùng guide C5R1 legacy cho đường contextual: nó
   không enforce contextual rewrite approval.
7. [Docs index](docs/README.md) — bản đồ toàn bộ cây `docs/`
   và bảng map đường cũ → đường mới.

Quy tắc đọc: không dùng ngày sửa file hay tên “latest” làm
nguồn trạng thái. Trạng thái chỉ lấy từ pins, manifest và
các bảng gate trong lớp IA này. Tài liệu README/ROADMAP cũ
được ghi rõ là nguồn lịch sử trong bản đồ nguồn.
