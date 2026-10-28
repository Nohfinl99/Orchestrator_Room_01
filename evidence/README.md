# Evidence index — Orchestrator-Room

Evidence frozen xác định bằng **commit SHA**, không bằng
path trên nhánh. Các thư mục `evidence/` trên nhánh này là
phần tích lũy làm việc, không phải bản frozen — khi trích
dẫn evidence, luôn kèm commit.

## Evidence pins (code + evidence tách commit)

| Mốc | Code commit | Evidence commit | Ghi chú |
|---|---|---|---|
| C6R1 (hiện hành) | `c7a837e3538aa6902c24ec4fd3fd8fd1cd047255` (5 paths) | `ea9c9464b14eb93bf4efe6b00bf6ce73e59218e7` (7 files) | Suite 83/83 Linux; acceptance 24/24 completed + 2 NOT_RUN, exit 2, full-scope NOT_RUN |
| C6 | `385f503b003479d4ae957d97cf3657e3900e1a37` (6 paths) | `da2d318cdad0ea268e8fc709f59fc1462321f4c9` (11 files) | Trước C6R1; suite 73/73 |
| C5R1 | `fd3430c9f1b0e98d1f6c9c62067b935f20054498` | `dde7b605b0ef9c97e3ae91156303638f3ba843fd` | Snapshot trước contextual; giữ frozen |
| C5 | `0a3d5a4d6606f3427b10162671a99adc3ef5b39b` | `18d74aa157fa9130f70f93be770e88c9e345f496` | Đời C5 |
| F21 (checker) | `bef96ccf3dabda9088491a615eec23cbc8dfe32c` | `1e5907658fbe6dd188ef1b8552fa48c053d040a3` | Fixtures intake-rev2: 39 files, manifest SHA-256 `fd1716cb…` |
| Packet-02 | — (không phải code) | Packet commit `4f683e7e4a8910cd731d8f78c2ad387455252ce6` (8 files) | Xem [../packets/README.md](../packets/README.md) |

## Quy tắc evidence (bắt buộc)

1. **Không di chuyển, không đổi tên, không repin evidence.**
   Manifest cũ không được sửa để trỏ sang commit mới.
2. **Code và evidence luôn tách commit.** Một commit code
   không kèm evidence mới và ngược lại.
3. **Không dùng lại log cũ để chứng minh code mới.** Mỗi
   revision nộp bằng chứng chạy lại của chính nó.
4. **NOT_RUN không gộp thành PASS.** Runner tách completed
   (PASS/FAIL) khỏi full-scope (NOT_RUN khi còn ca bắt
   buộc chưa chạy).
5. **Branch head không phải evidence.** Trạng thái chỉ lấy
   từ pin commit và manifest, không lấy từ “file mới nhất
   trên nhánh”.
6. **Evidence của trial thật (attempt-01/02) giữ local,**
   không upload raw khi chưa có ủy quyền; packet repo chỉ
   chứa dạng đã redacted / tham chiếu (xem packets README).
