# Chạy local trên Windows với C5R1 frozen — hướng dẫn cho owner

> LƯU Ý LỊCH SỬ: guide này mô tả đường C5R1 legacy
> (propose/decide theo template cố định, KHÔNG enforce
> contextual rewrite approval). Đường contextual hiện
> hành là
> [windows-contextual-c6r1.vi.md](windows-contextual-c6r1.vi.md).
> Đừng dùng guide này cho đường contextual.

Hướng dẫn này chỉ chạy code đã frozen, không sửa code,
không merge, không đổi `main` hay `Orchestrator_Reverse`.
Nếu bất kỳ điểm kiểm tra nào dưới đây không khớp, dừng
lại và báo — đừng sửa lệnh để ép ra kết quả PASS.

## Prerequisites

- Windows 11, Git đã cài, PowerShell.
- Python 3.14 (reviewer đã dùng Python 3.14.4 cho lần chạy
  Windows C5R1). Không cần network, provider, tài khoản
  ngoài hay credential nào. Repo và fixtures không chứa
  credential hay dữ liệu thật.
- Quyền tạo symlink KHÔNG bắt buộc. Nếu thiếu quyền, các
  subcase symlink sẽ là NOT_RUN (WinError 1314) — đó là
  kết quả đúng, không phải lỗi cần vượt qua bằng cách ép
  chạy với quyền khác để lấy PASS.

## Checkout đúng C5R1

Thay `<thư-mục-làm-việc>` bằng thư mục trống của bạn.
Mọi đường dẫn đều có quote; đừng bỏ quote khi đường dẫn
có khoảng trắng.

```powershell
Set-Location -LiteralPath '<thư-mục-làm-việc>'
git clone 'https://github.com/Nohfinl99/Orchestrator-Room.git'
Set-Location -LiteralPath '.\Orchestrator-Room'
git checkout 'fd3430c9f1b0e98d1f6c9c62067b935f20054498'
git rev-parse HEAD
# Kết quả cần nhìn thấy: fd3430c9f1b0e98d1f6c9c62067b935f20054498
# Nếu khác, DỪNG LẠI. Đừng chạy tiếp với một revision khác.
```

## Source và output tách biệt

Source root là thư mục checkout vừa tạo. Trial/output
phải là một thư mục MỚI, NGOÀI source, cho mỗi attempt.
Không bao giờ dùng lại thư mục output của attempt cũ và
không ghi đè file của attempt trước.

```powershell
$sourceRoot = '<đường-dẫn-checkout-C5R1-vừa-tạo>'
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
lệnh trước đó. Placeholder không phải dữ liệu chạy được.

```powershell
py -3.14 -X utf8 -m control_room init --store room.json
$LASTEXITCODE
py -3.14 -X utf8 -m control_room intake --store room.json --input request.txt
$LASTEXITCODE
py -3.14 -X utf8 -m control_room overview --store room.json
$LASTEXITCODE
# Copy intake_id thật từ output của intake, rồi:
py -3.14 -X utf8 -m control_room propose --store room.json --intake-id '<actual-intake-id>'
$LASTEXITCODE
py -3.14 -X utf8 -m control_room proposal-view --store room.json --proposal-id '<actual-proposal-id>'
$LASTEXITCODE
```

## Điểm dừng bắt buộc cho operator quyết định

DỪNG LẠI sau `proposal-view`. Không có lệnh nào ở trên
tạo decision. Trước khi decide, đọc kỹ:

- Intake thật: original text, statements, unknowns, hash.
- Proposal: 4 task cố định, role, dependency.
- Binding digest của proposal.

Chỉ sau khi operator chọn rõ một quyết định
(APPROVE/REVISE/REJECT/DEFER) kèm lý do nguyên văn và
nhãn operator, mới chạy decide với bindings ĐÃ REVIEW
(không thay bằng digest hiện tại trong store):

```powershell
py -3.14 -X utf8 -m control_room decide --store room.json --proposal-id '<reviewed-proposal-id>' --expected-proposal-digest '<reviewed-64-hex-digest>' --expected-brief-revision 'PRODUCT_INTAKE_BRIEF_REV2' --expected-intake-id '<reviewed-intake-id>' --decision '<APPROVE|REVISE|REJECT|DEFER>' --reason '<actual-operator-reason>' --operator '<operator-label>' --source 'local-cli'
$LASTEXITCODE
py -3.14 -X utf8 -m control_room verify-history --store room.json
$LASTEXITCODE
py -3.14 -X utf8 -m control_room overview --store room.json
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
- Task DONE chỉ là trạng thái; decision local là
  `OPERATOR_ASSERTED`, không phải product acceptance và
  không đổi stage C4. Nếu decide trả stale (`REJECTED_STALE`),
  giữ gate chưa hoàn thành và báo nguyên nhân — đừng đổi
  bindings rồi chạy lại để ép PASS.

## Lần chạy này chứng minh và không chứng minh gì

- Chứng minh (trong phạm vi lần chạy đó): CLI local với
  template cố định chạy intake → proposal → view → gate
  trên input đã cho, với history kiểm được.
- Không chứng minh: điều phối agent thông minh, live
  worker/chat listener, runtime knowledge retrieval, giá
  trị sản phẩm, hay tiết kiệm thời gian (cần baseline đo
  thật với cùng boundary, hiện đang null).
