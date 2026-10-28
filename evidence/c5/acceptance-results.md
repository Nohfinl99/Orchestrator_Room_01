# C5 acceptance results (builder-run, A01-A33 + variants)

Total subcases: 53; PASS: 53; FAIL: 0.
OS: Linux 7.0.0-39-generic; Python: 3.12.3.

| Case | Subcase | Result |
|---|---|---|
| A01 | golden intake file | PASS |
| A02 | empty input | PASS |
| A03 | byte over cap | PASS |
| A03 | char over cap | PASS |
| A04 | invalid UTF-8 | PASS |
| A05 | baseline six null + provenance | PASS |
| A06 | duplicate | PASS |
| A07 | statements vs interpretations separate | PASS |
| A08 | hostile set PASS inert | PASS |
| A09 | pasted approval inert | PASS |
| A10 | upload/send text inert | PASS |
| A11 | proposal dependency view | PASS |
| A12 | restart/reload coherent | PASS |
| A13 | changed brief invalidates approval | PASS |
| A14 | no auto-PASS | PASS |
| A15 | outside cwd | PASS |
| A15 | symlink | PASS |
| A15 | .git path | PASS |
| A15 | secret-like filename | PASS |
| A15 | binary (invalid UTF-8) | PASS |
| A15 | missing file | PASS |
| A16 | deterministic proposal, two stores | PASS |
| A17 | gate only, OPERATOR_ASSERTED | PASS |
| A18 | immutable intake via correction | PASS |
| A19 | golden template four tasks | PASS |
| A20 | stale decision rejected | PASS |
| A21 | wrong brief | PASS |
| A21 | wrong intake | PASS |
| A22 | knowledge/Soul/Heart honesty | PASS |
| A23 | byte cap 20,000 accepted | PASS |
| A23 | byte cap 20,001 rejected | PASS |
| A24 | whitespace-only rejected | PASS |
| A24 | accepted content never trimmed | PASS |
| A25 | char cap 10,000 accepted | PASS |
| A25 | char cap 10,001 rejected | PASS |
| A26 | request-bom.json | PASS |
| A27 | request-nul.json | PASS |
| A28 | request-crlf.txt | PASS |
| A28 | request-mixed.txt | PASS |
| A28 | request-bare-cr.txt | PASS |
| A28 | request-no-newline.txt | PASS |
| A29 | unicode combining preserved | PASS |
| A30 | propose repeat idempotent | PASS |
| A31 | correction new record, old unchanged | PASS |
| A32 | view change does not change digest | PASS |
| A32 | payload change invalidates bound decision | PASS |
| A33 | owner acceptance recorded, not assumed | PASS |
| V01 | missing expected binding flag | PASS |
| V02 | wrong-format bindings | PASS |
| V03 | correction rejections with events | PASS |
| V04 | concurrent decide, exactly one | PASS |
| V05 | stdin intake | PASS |
| V06 | tampered intake fails history | PASS |
