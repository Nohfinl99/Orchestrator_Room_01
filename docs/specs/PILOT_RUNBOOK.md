# Local pilot runbook — CLI only, no chat listener, no live agents

This runbook is honest about the current entry point. It does not
activate anything beyond the local CLI slice, and it must not be
read as a chat or agent system.

## Supported state

- Local files and synthetic/redacted data only.
- Python standard library only, no network, no provider, no
  background work.
- Live adapters: **BLOCKED**. Simulated role arguments are
  **not authentication** and do not grant real authority.
- A chat message does **not** start live orchestration in this
  slice. There is no chat listener, no natural-language dispatch,
  and no real worker coordination here. Those are separate
  integration work, not silently enabled by this runbook.

## Exact supported commands (run from a checkout root)

```sh
python3 -m control_room --help
python3 -m control_room init --store room.json
python3 -m control_room overview --store room.json
python3 -m control_room add-observation --store room.json --role agent \
  --id OBS-01 --trigger "synthetic trigger" \
  --problem "synthetic problem" \
  --source-locator "synthetic-fixture:obs-01"
python3 -m control_room overview --store room.json
python3 -m control_room history --store room.json
python3 -m control_room verify-history --store room.json
```

## Observable next steps after capture

After `add-observation`, `overview` still shows stage **INTAKE**,
because capture alone does not advance the product stage. The
owner-controlled next step is a transition, for example:

```sh
python3 -m control_room transition --store room.json --role owner \
  --to NEEDS_EVIDENCE --reason "owner moves captured observation forward"
```

Further stages follow the fixed machine only, with content-bound
prerequisites (ready observation, reviewed inference, approved
brief, judge report, owner decision naming that report). See
`control_room/README.md` for the full stage machine and gate rules.
`verify-history` reports the audit chain and its same-owner
full-recompute limit; it does not prove a real review happened.

## If a user-message entry/adapter is required next

That is **one explicit atomic task, not implemented here**:

> Input: a user message in a defined channel
> -> Intake record: create one observation with trigger, problem,
>    and source locator, preserving unknowns as null
> -> Task/role proposal: propose tasks and roles from that record
>    only, with no provider execution
> -> Owner gate: no stage advance, no dispatch, and no external
>    action until an owner explicitly approves at the gate

Do not present that future adapter as already implemented, and do
not enable a provider to satisfy it without a separate explicit
authorization and a concrete trust model.
