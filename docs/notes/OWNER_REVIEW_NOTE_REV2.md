# Ghi chú review cho owner — nhánh chưa hoàn thành (Rev2)

> Trạng thái: NHÁNH CHƯA HOÀN THÀNH, HỆ THỐNG VẪN NOT_VERIFIED.
> File này chỉ là hướng dẫn review, không phải code, không thay đổi
> code đã nộp. Đừng merge nhánh này cho tới khi owner ra quyết định
> bằng văn bản trong chat Muse trực tiếp.

## 1. Đang review cái gì, ở đâu

- Repo: `Nohfinl99/Orchestrator-Room`, nhánh `muse/local-control-room`
- Gốc: main `8bd7d8a9fcdff34ef6ed1626050c2371661ab279` (không đổi)
- Bản đầu: `1bba80368b5a7dfc75d3b66881ccada6a5252a48` — review độc lập
  trước đó verdict REVISE_REQUIRED (xem nhánh `codex/review-muse-1bba803`,
  chỉ đọc, không merge).
- **Commit code cần review (C): `d409eca531a202879c2d5bcddc3f9e90794335d3`**
  - 6 file: `control_room/__init__.py`, `control_room/backend.py`,
    `control_room/cli.py`, `control_room/README.md`,
    `tests/test_control_room.py`,
    `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md`
  - Code này sửa F01–F06, ưu tiên chặn false PASS và sửa oracle T10.
- **Commit evidence cần review (E): `25f9f034d9493d447242ab16f674e27617b5605c`**
  - Chỉ chứa: `RUN_REPORT_REV2.md`,
    `evidence/rev2/clean-checkout-test-run-2026-10-25.log`,
    `evidence/rev2/clean-checkout-source-digests.json`
  - E không đổi code. Nếu nhánh đã có thêm commit hướng dẫn này (D),
    hãy review đúng C cho code và E cho evidence, không lấy head làm
    chuẩn code.
- Báo cáo cũ `RUN_REPORT.md` và log cũ `evidence/local-test-run-2026-10-25.log`
  được giữ nguyên làm bằng chứng lịch sử cho 1bba803, không sửa.
- Không thay đổi gì trong `Nohfinl99/Orchestrator_Reverse`.

## 2. Cách xem nhanh trên GitHub (không cần clone)

1. Mở repo `Nohfinl99/Orchestrator-Room`, chọn nhánh
   `muse/local-control-room`.
2. Vào tab Commits, mở commit C `d409eca5…` để xem 6 file đổi.
   Mở commit E `25f9f034…` để xem báo cáo và evidence.
3. Đọc theo thứ tự:
   - `RUN_REPORT_REV2.md` (ma trận từng subcriterion, mục NOT_RUN)
   - `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` (những claim cũ bị bác và
     đã sửa ra sao; 10 pin knowledge gốc không đổi)
   - `control_room/README.md` (luật Rev2, giới hạn simulation)
   - `tests/test_control_room.py` (đặc biệt test_10, test_10b,
     test_17, test_18, test_19, test_21)
4. Đối chiếu hash trong `RUN_REPORT_REV2.md` với file trong E:
   - Log test: SHA-256 `2d6f3225b3f56683a38d7bb97c753bcf11f4943e6800d3c83cf929fd2a8b65e3`
   - Manifest: SHA-256 `55c80113190584259ccd77a61798d8fc5651740aa033ad150ac8ccdc3ae7ef81`
   - Backend C: SHA-256 `a7df0f57e16c9ddc0bff50bfe1a089d65b40b0e1451aa00713e3eab87ef63eb5`
   - CLI C: SHA-256 `61d816f4da248513cf65c6ee0537fb50a7d74129afa82d3277b4995858295aad`
   - Tests C: SHA-256 `89f9194ccb860a4c1e35c8d09197137d7cade6a34fefb02754018d20973e58d5`

## 3. Cách chạy lại nếu muốn kiểm chứng (tùy chọn, dữ liệu synthetic)

```sh
git clone --branch muse/local-control-room https://github.com/Nohfinl99/Orchestrator-Room.git
cd Orchestrator-Room
git checkout d409eca531a202879c2d5bcddc3f9e90794335d3
python3 -m unittest discover -s tests -v
```

Kết quả builder-run đã báo: 25/25 PASS, exit 0, Python 3.12.3, Linux.
Đây là kiểm tra của builder, không phải verdict độc lập. Một verify
PASS trong test chỉ là kiểm tra cơ chế, không chứng minh review độc
lập và không validate product/pain.

Thử nhanh các negative control (đều phải KHÔNG ra PASS):
- Evidence giả (file không tồn tại, hash bịa, thiếu command/env,
  thiếu receipt) → verify phải INCONCLUSIVE, không PASS.
- Evidence exit code 9 → verify phải FAIL, không PASS.
- Thêm observation sau khi judge report đã tạo, rồi quyết định
  OWNER_ACCEPTED với report cũ → phải bị reject, ghi event
  `decision_rejected`, stage vẫn JUDGE_REVIEW.
- Hai writer cùng load một revision, writer thứ hai lưu sau →
  phải bị reject stale, update của writer đầu còn nguyên.

## 4. Những gì CHƯA xong — đừng coi là pass

- Independent Judge review của C: NOT_RUN
- Full pentest của C: NOT_RUN
- Owner decision trên slice Rev2: NOT_RUN (chính là bước này)
- Windows run: NOT_RUN (lần trước lỗi symlink WinError 1314)
- Packet-level no-egress: NOT_RUN (test T13 chỉ kiểm tra chuỗi tĩnh)
- Browser/auth: NOT_RUN, scoped exclusion (slice không có HTTP server)
- Approval timeout, giới hạn fan-out/concurrency, recovery lỗi đĩa thật: NOT_RUN
- Product/pain validation: NEEDS_EVIDENCE, chưa validate

## 5. Checklist review cho owner (đánh dấu từng mục)

- [ ] F01: false PASS đã chặn thật chưa, hay chỉ đổi tên test?
- [ ] F02: gate rỗng/cũ có còn lọt OWNER_ACCEPTED không?
- [ ] F03: nhãn simulation có rõ ràng không, có claim xác thực giả không?
- [ ] F04: stale writer và failed save có giữ đúng store cũ không?
- [ ] F05: write vượt giới hạn có bị reject trước khi ghi không?
- [ ] F06: event có timestamp/digest/chain không, giới hạn chống
      owner đã ghi rõ chưa?
- [ ] Hash trong RUN_REPORT_REV2 có khớp file trong E không?
- [ ] Có file nào ngoài 6 file code + 3 file evidence bị đổi lén không?
- [ ] Có merge/PR/đổi gì ở main hoặc Orchestrator_Reverse không?
      (Đáp án đúng: không.)

## 6. Báo lại cho Muse như thế nào

Báo trực tiếp trong chat Muse (không qua Telegram, vì duyệt chỉ có
hiệu lực ở chat Muse trực tiếp). Dán theo mẫu:

```
Verdict: [ACCEPT_REV2 / REVISE_AGAIN / STOP]
F01: [PASS/FAIL/OPEN] — bằng chứng:
F02: [PASS/FAIL/OPEN] — bằng chứng:
F03: [PASS/FAIL/OPEN] — bằng chứng:
F04: [PASS/FAIL/OPEN] — bằng chứng:
F05: [PASS/FAIL/OPEN] — bằng chứng:
F06: [PASS/FAIL/OPEN] — bằng chứng:
Finding mới (nếu có): [mô tả + bước tái hiện chính xác]
Quyết định: [merge / sửa tiếp / dừng] — chỉ quyết định này mới có hiệu lực
```

Không tự merge, không tự đổi verdict REVISE_REQUIRED thành PASS
chỉ vì test builder chạy xanh. Nếu anh thấy một finding mới, ghi rõ
bước tái hiện để Muse sửa đúng chỗ đó trong lượt tiếp theo.
