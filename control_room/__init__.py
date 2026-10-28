"""Local control-room slice for Orchestrator-Room, revisions 5 and 5.1.

Stdlib only. No network, no provider, no background work.
This package is a control-plane prototype, not live agent orchestration.
Role arguments are simulation only, not authentication.

Revision 5 (C5, packet REV2.1 + checker fix F21) adds a thin local
intake slice: bounded file/stdin intake, immutable intake records
with dedupe and correction, a fixed-template proposal with a
computed dependency view, and a local operator gate decision with
required expected bindings. See control_room/C5_BUILD_NOTE.md.

Revision 5.1 (C5R1, bounded fixes C5-F01..F07 after independent
C5/E5 review) fixes reason verbatim handling, the T04 review-gate
next action, legacy Judge scope labelling, and acceptance-runner
evidence truth, portability, and reproducibility. See
control_room/C5R1_NOTE.md. C5 and E5 commits are preserved
unchanged; C5R1 is a separate code revision, not a new product
feature.
"""
__version__ = "0.5.1"
