# Chạy contextual trên Windows với C6R1 frozen — runbook cho owner

Runbook này chỉ chạy code đã frozen, không sửa code,
không merge, không đổi `main` hay `Orchestrator_Reverse`.
Nó là đường contextual HIỆN HÀNH. Guide C5R1 legacy
([windows-local-run.vi.md](windows-local-run.vi.md)) mô
tả propose/decide theo template cố định và KHÔNG enforce
contextual rewrite approval — đừng dùng guide đó cho
đường này.

Luật cốt lõi: draft brief do operator cung cấp từ request
gốc; review ràng buộc đúng rewrite digest đã đọc; chỉ
sau quyết định thật của owner mới được propose. Mọi nhãn
operator/role chỉ là tham số mô phỏng; decision là
`OPERATOR_ASSERTED`, không phải product acceptance và
không phải xác thực owner thật.

Nếu bất kỳ điểm kiểm tra nào dưới đây không khớp, dừng
lại và báo — đừng sửa lệnh để ép ra kết quả PASS.

## Prerequisites

- Windows 11, Git đã cài, PowerShell.
- Python 3.14 (reviewer đã dùng Python 3.14.4 cho lần chạy
  Windows C5R1; nếu bạn dùng phiên bản khác, ghi rõ phiên
  bản thật trong log attempt — khác phiên bản không tự
  thành cùng một bằng chứng).
- Không cần network, provider, tài khoản ngoài hay
  credential nào. Repo và fixtures không chứa credential
  hay dữ liệu thật.
- Quyền tạo symlink KHÔNG bắt buộc. Nếu thiếu quyền, các
  subcase symlink sẽ là NOT_RUN (WinError 1314) — đó là
  kết quả đúng, không phải lỗi cần vượt qua bằng cách ép
  chạy với quyền khác để lấy PASS.

## Checkout đúng C6R1, giữ nguyên newline

Thay `<thư-mục-làm-việc>` bằng thư mục trống của bạn.
Mọi đường dẫn đều có quote; đừng bỏ quote khi đường dẫn
có khoảng trắng. `core.autocrlf=false` là bắt buộc để
checkout giữ nguyên byte gốc (fixture/input không bị đổi
LF thành CRLF, hash mới khớp). Lưu ý: override `-c` ở
lệnh clone KHÔNG tồn tại sang lệnh checkout sau đó, nên
checkout cũng phải mang `-c core.autocrlf=false`. Cách
khác tương đương: chạy `git config --local
core.autocrlf false` trong repo trước khi checkout (chỉ
config repo-local, KHÔNG đổi config global của máy).

```powershell
Set-Location -LiteralPath '<thư-mục-làm-việc>'
git -c core.autocrlf=false clone 'https://github.com/Nohfinl99/Orchestrator-Room.git'
Set-Location -LiteralPath '.\Orchestrator-Room'
git -c core.autocrlf=false checkout 'c7a837e3538aa6902c24ec4fd3fd8fd1cd047255'
git rev-parse HEAD
# Kết quả cần nhìn thấy: c7a837e3538aa6902c24ec4fd3fd8fd1cd047255
# Nếu khác, DỪNG LẠI. Đừng chạy tiếp với một revision khác.
git status --porcelain
# Kết quả cần nhìn thấy: trống (không có file đã sửa).
# Nhưng git status clean KHÔNG đủ: đổi LF thành CRLF vẫn
# cho status clean. Bắt buộc đối chiếu SHA-256 của một
# file đã commit, ví dụ:
Get-FileHash -LiteralPath 'control_room\backend.py' -Algorithm SHA256
# Kết quả cần nhìn thấy: 651eb641af11f5597f363821284d92a35e20c495a516aab3f17cdb3fef1d9b00
# (SHA-256 của control_room/backend.py tại C6R1).
# Nếu khác, DỪNG LẠI. Đừng chạy tiếp với checkout đã đổi byte.
```

## Source và output tách biệt

Source root là thư mục checkout vừa tạo. Trial/output
phải là một thư mục MỚI, NGOÀI source, cho mỗi attempt.
Không bao giờ dùng lại thư mục output của attempt cũ và
không ghi đè file của attempt trước.

```powershell
$sourceRoot = '<đường-dẫn-checkout-C6R1-vừa-tạo>'
$trialRoot = '<thư-mục-trial-mới-ngoài-source>'
New-Item -ItemType Directory -Path $trialRoot -Force
# Copy request thật đã redacted vào $trialRoot, byte-for-byte,
# rồi đối chiếu hash của bản copy với hash của file gốc trước
# khi chạy intake. Nếu hash khác, DỪNG LẠI.
Set-Location -LiteralPath $trialRoot
$env:PYTHONPATH = $sourceRoot
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
```

## Lệnh chạy (ghi $LASTEXITCODE ngay sau mỗi lệnh)

Thay `<...>` bằng giá trị thật copy từ output của chính
lệnh trước đó. Placeholder không phải dữ liệu chạy được,
không dùng giá trị bịa (không digest giả, không intake-id
giả, không câu trả lời giả của owner).

```powershell
py -3.14 -X utf8 -m control_room init --store room.json
$LASTEXITCODE
py -3.14 -X utf8 -m control_room intake --store room.json --input request.txt
$LASTEXITCODE
# Copy intake_id thật từ output của intake, rồi:
py -3.14 -X utf8 -m control_room ctx-assess --store room.json --intake-id '<actual-intake-id>'
$LASTEXITCODE
```

### Nếu assess nói thiếu context: thêm nguồn, hỏi, trả lời

Nguồn chỉ là locator (không phải nội dung đã nạp): `--trust-class`
chỉ nhận `owner_statement`, `reference` hoặc `external_text`.

```powershell
py -3.14 -X utf8 -m control_room ctx-add-source --store room.json --intake-id '<actual-intake-id>' --source-id '<actual-source-id>' --locator '<actual-locator>' --trust-class '<owner_statement|reference|external_text>'
$LASTEXITCODE
# Hỏi đúng 2–3 câu (batch 1 hoặc 4 câu bị chặn — đó là fix F02):
py -3.14 -X utf8 -m control_room ctx-clarify --store room.json --intake-id '<actual-intake-id>' --questions '<question-1>' '<question-2>' '<question-3>'
$LASTEXITCODE
# Copy clarification_id thật, rồi trả lời nguyên văn.
# Số đáp án phải bằng đúng số câu hỏi trong batch:
# batch 2 câu → 2 đáp án, batch 3 câu → 3 đáp án.
# Ví dụ dưới là batch 3 câu; batch 2 câu thì chỉ ghi 2 đáp án, không thêm đáp án thứ ba:
py -3.14 -X utf8 -m control_room ctx-answer --store room.json --clarification-id '<actual-clarification-id>' --answers '<verbatim-answer-1>' '<verbatim-answer-2>' '<verbatim-answer-3>'
$LASTEXITCODE
```

Nếu assess nói input đã rõ, bỏ qua ba lệnh trên và đi
thẳng tới draft — dùng variant A bên dưới, không bịa
clarification-id — nhưng vẫn phải review trước khi propose.

### Draft, xem lại, rồi DỪNG

Variant A — input đã rõ, không có clarification: BỎ HẲN
cả `--clarification-id` lẫn giá trị của nó. Option này
là tùy chọn theo `ctx-draft --help`; không có clarification
thì không được ghi option này với placeholder hay ID bịa.

```powershell
py -3.14 -X utf8 -m control_room ctx-draft --store room.json --intake-id '<actual-intake-id>' --goal '<actual-goal>' --context '<actual-context>' --scope '<actual-scope>' --desired-output '<actual-desired-output>' --next-action '<actual-next-action>'
$LASTEXITCODE
```

Variant B — đã hỏi và trả lời: mới thêm
`--clarification-id` với ID thật đã trả lời ở trên.

```powershell
py -3.14 -X utf8 -m control_room ctx-draft --store room.json --intake-id '<actual-intake-id>' --goal '<actual-goal>' --context '<actual-context>' --scope '<actual-scope>' --desired-output '<actual-desired-output>' --next-action '<actual-next-action>' --clarification-id '<actual-clarification-id>'
$LASTEXITCODE
# Áp dụng cho cả variant A và B — copy rewrite_id thật, rồi xem toàn bộ rewrite:
py -3.14 -X utf8 -m control_room ctx-rewrite-view --store room.json --rewrite-id '<actual-rewrite-id>'
$LASTEXITCODE
```

## Điểm dừng bắt buộc cho owner review digest

DỪNG LẠI sau `ctx-rewrite-view`. Không có lệnh nào ở trên
tạo review hay proposal. Trước khi review, đọc kỹ rewrite
thật: goal, context, scope, desired-output, next-action,
unknowns, và digest của nó.

Chỉ sau khi owner chọn rõ một quyết định
(APPROVE/REVISE/REJECT/DEFER) kèm lý do nguyên văn và
nhãn operator, mới chạy review với digest ĐÃ REVIEW
(không thay bằng digest hiện tại trong store):

```powershell
py -3.14 -X utf8 -m control_room ctx-review-rewrite --store room.json --rewrite-id '<reviewed-rewrite-id>' --expected-rewrite-digest '<reviewed-64-hex-digest>' --decision '<APPROVE|REVISE|REJECT|DEFER>' --reason '<actual-operator-reason>' --operator '<operator-label>' --source 'local-cli'
$LASTEXITCODE
```

Guards (đừng coi exit 2 là lỗi cần vượt qua):

- Còn clarification đang mở → exit 2 `clarification_open`,
  không tạo decision. Trả lời clarification rồi draft mới,
  review mới.
- Digest/context/source đã stale → exit 2 `REJECTED_STALE`,
  không tạo decision. Không rebind lặng lẽ sang digest
  mới: draft lại và review lại từ đầu.
- Lặp lại APPROVE y hệt sau khi các guard đã qua → trả
  về review đã có (`already_exists=true`,
  `new_review_created=false`). Đây là readback của
  review đã frozen, không phải bypass an toàn (sửa DOC01).

## Chỉ sau APPROVE mới propose

REVISE/REJECT/DEFER không tạo proposal. Nếu REVISE, quay
lại draft mới rồi review mới. Chỉ khi review đã APPROVE:

```powershell
py -3.14 -X utf8 -m control_room ctx-propose --store room.json --intake-id '<actual-intake-id>' --rewrite-id '<reviewed-rewrite-id>' --expected-rewrite-digest '<reviewed-64-hex-digest>'
$LASTEXITCODE
py -3.14 -X utf8 -m control_room ctx-status --store room.json --intake-id '<actual-intake-id>'
$LASTEXITCODE
py -3.14 -X utf8 -m control_room ctx-proposal-view --store room.json --proposal-id '<actual-proposal-id>'
$LASTEXITCODE
py -3.14 -X utf8 -m control_room verify-history --store room.json
$LASTEXITCODE
Get-FileHash -LiteralPath request.txt -Algorithm SHA256
Get-FileHash -LiteralPath room.json -Algorithm SHA256
```

## Lưu raw outputs đúng cách

- Ghi riêng stdout, stderr và `$LASTEXITCODE` cho mỗi
  lệnh, vào thư mục attempt đó, không ghi đè attempt cũ.
- Lưu ý: PowerShell redirection (`>`) có thể re-encode
  text. Nếu cần log byte-chính xác, capture subprocess
  bytes như script của reviewer, hoặc ghi rõ encoding đã
  dùng khi redirect. Đừng trình bày log đã re-encode như
  raw bytes gốc.
- Review/proposal local là `OPERATOR_ASSERTED`, không
  phải product acceptance. Nếu review trả stale, giữ gate
  chưa hoàn thành và báo nguyên nhân — đừng đổi bindings
  rồi chạy lại để ép PASS.

## Lần chạy này chứng minh và không chứng minh gì

- Chứng minh (trong phạm vi lần chạy đó): CLI local chạy
  assess → nguồn locator-only → hỏi/trả lời (khi cần) →
  draft → owner review đúng digest → propose, với history
  kiểm được, trên input đã cho.
- Không chứng minh: hiểu ngữ nghĩa thật (assess là keyword
  heuristic), điều phối agent thông minh, live worker/chat
  listener, runtime knowledge retrieval, giá trị sản phẩm,
  hay tiết kiệm thời gian (baseline đang null).
