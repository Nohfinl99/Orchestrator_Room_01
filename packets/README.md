# Packet index — Orchestrator-Room

Packet là gói bằng chứng kiểm chứng được của một trial.
Packet tốt cho phép reviewer tính lại digest mà không cần
raw request. Packet KHÔNG phải approval, KHÔNG phải
product acceptance.

## Packet đã có

| Packet | Commit | Nội dung | Submission / Review |
|---|---|---|---|
| `ctx-001-packet-02` (attempt-02) | `4f683e7e4a8910cd731d8f78c2ad387455252ce6` (8 file, manifest tự loại trừ) | Descriptor dạng tham chiếu (`REFERENCE_FORM_NOT_HASH_PAYLOAD`), transcript room đã redacted, hash SHA-256/bytes của file raw giữ local, provenance đáp án tái dùng, metadata lệnh/exit, output verify-history | Submission `SUB-CTX-001-PACKET02-R0` (kênh rev22) → review `REV-CTX-001-PACKET02-R0` APPROVED_SCOPED, readiness `READY_FOR_BOUNDED_OWNER_REWRITE_TRIAL` (kênh rev24) |

Packet-02 ràng buộc: intake `INTAKE-0d0bcbe75d4fbee1`,
clarification `CTXQ-4723da2edd3488b0`, rewrite
`RW-74cd5f5b72e0e01c`, digest
`74cd5f5b72e0e01cbe96d08742a0335320dc2dbd1247134691a592b4e8919e97`,
review_status `DRAFT_NOT_REVIEWED`, KHÔNG proposal. Quyết
định thật của owner trên digest vẫn đang chờ (cổng
version 1); duyệt packet không thay thế quyết định đó.

## Attempt-01: KHÔNG phải packet repo

Trial attempt-01 chỉ tồn tại local (store/DEC cũ không
chạm). Bundle evidence của nó (zip 10773 bytes, SHA-256
`e428fa8a01c5d3289bb62343253e9dca3722a9cd0205985210340967369b9909`)
đã hết hạn link (2026-10-28 01:54:41 +07). Không tải lại
bundle, không yêu cầu owner relay lại bundle. Receipt kiểm
đã có trong `trial-bundle-audit.json` tại pin requirement
(xem [../docs/requirements/index.md](../docs/requirements/index.md)).

## Quy tắc cho packet tương lai

1. Không upload raw request và không upload full raw store
   khi chưa có ủy quyền. Nội dung protected chỉ xuất hiện
   dạng tham chiếu: SHA-256 nguồn + span ký tự 0-based +
   SHA-256 của span, gắn nhãn `REFERENCE_FORM_NOT_HASH_PAYLOAD`.
2. Descriptor phải đủ trường để reviewer tính lại digest
   độc lập (thuật toán + bước tái tạo + packager self-check).
3. Manifest tự loại trừ chính nó; mỗi file kèm SHA-256 và
   độ dài byte.
4. Phân biệt rõ transcript đã redacted với raw bytes. Nếu
   history chain không tái tạo đầy đủ từ tài liệu được
   phép thì ghi PARTIAL/UNVERIFIED, không bịa PASS.
5. Packet không đổi code/evidence/docs pin, không đổi
   digest/rewrite đã nộp. Payload đổi thì khai revision /
   digest mới, không giữ claim cũ.
