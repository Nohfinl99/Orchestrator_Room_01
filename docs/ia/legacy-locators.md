# Locator cũ trong hồ sơ được bảo toàn

Kiểm ngày 29/10/2026 thấy 20 relative Markdown link không resolve ở layout
bản sao: 8 trong README-LEGACY và 12 trong REPORT Windows C3. Các file
nguồn này được giữ nguyên bytes. Dùng bảng sau để mở bản tương ứng;
bảng không sửa manifest, repin hoặc chứng minh tương đương ngữ nghĩa.

| File chứa link cũ | Target nguyên văn | Đường đọc trong bản sao |
|---|---|---|
| docs/notes/README-LEGACY.md | ARCHITECTURE.md | [Mở file](../../docs/specs/ARCHITECTURE.md) |
| docs/notes/README-LEGACY.md | PIPELINE.md | [Mở file](../../docs/specs/PIPELINE.md) |
| docs/notes/README-LEGACY.md | ACCEPTANCE.md | [Mở file](../../docs/specs/ACCEPTANCE.md) |
| docs/notes/README-LEGACY.md | VERIFICATION_POLICY.md | [Mở file](../../docs/specs/VERIFICATION_POLICY.md) |
| docs/notes/README-LEGACY.md | THREAT_MODEL.md | [Mở file](../../docs/specs/THREAT_MODEL.md) |
| docs/notes/README-LEGACY.md | PENTEST_PLAN.md | [Mở file](../../docs/specs/PENTEST_PLAN.md) |
| docs/notes/README-LEGACY.md | painpoint-observation-template.json | [Mở file](../../docs/data/painpoint-observation-template.json) |
| docs/notes/README-LEGACY.md | handoff-manifest.json | [Mở file](../../docs/data/handoff-manifest.json) |
| evidence/windows-c3/REPORT.md | evidence/windows/windows-test-run-2026-10-25.log | [Mở file](../../evidence/windows-c3/windows-test-run-2026-10-25.log) |
| evidence/windows-c3/REPORT.md | evidence/windows/windows-test-manifest.json | [Mở file](../../evidence/windows-c3/windows-test-manifest.json) |
| evidence/windows-c3/REPORT.md | evidence/execution-receipt.json | [Mở file](../../evidence/windows-c3/execution-receipt.json) |
| evidence/windows-c3/REPORT.md | evidence/windows-helper-console.log | [Mở file](../../evidence/windows-c3/windows-helper-console.log) |
| evidence/windows-c3/REPORT.md | evidence/bundle-manifest.json | [Mở file](../../evidence/windows-c3/bundle-manifest.json) |
| evidence/windows-c3/REPORT.md | evidence/tooling-negative/result.json | [Mở file](../../evidence/windows-c3/tooling-negative/result.json) |
| evidence/windows-c3/REPORT.md | evidence/tooling-negative/failing-suite.log | [Mở file](../../evidence/windows-c3/tooling-negative/failing-suite.log) |
| evidence/windows-c3/REPORT.md | evidence/tooling-negative/launcher-console.log | [Mở file](../../evidence/windows-c3/tooling-negative/launcher-console.log) |
| evidence/windows-c3/REPORT.md | evidence/tooling-negative/helper-manifest.json | [Mở file](../../evidence/windows-c3/tooling-negative/helper-manifest.json) |
| evidence/windows-c3/REPORT.md | tooling_checks.py | KHÔNG CÓ trong cây đã kiểm kê; chưa xác định locator nguồn, không tạo file giả |
| evidence/windows-c3/REPORT.md | evidence/smoke-and-controls.json | [Mở file](../../evidence/windows-c3/smoke-and-controls.json) |
| evidence/windows-c3/REPORT.md | ../../MUSE_AFTER_WINDOWS_INSTRUCTIONS.md | KHÔNG CÓ trong cây đã kiểm kê; chưa xác định locator nguồn, không tạo file giả |

Hai target không có trong cây được giữ là gap truy cập. Lượt này không
truy vấn nhánh reviewer nguồn để tìm chúng. Các link ngoài repo chưa được
HTTP-check toàn bộ; link có pin vẫn cần quyền truy cập tương ứng.

[Source map](source-map.md) · [Docs index](../README.md).
