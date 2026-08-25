---
title: 'Establish the Verified Brownfield Baseline'
type: 'chore'
created: '2026-08-23'
baseline_commit: '97ccc70f95dc25fc4c0c8e8cb41fc719ca78d7ec'
evidence_commit: '7c8434106bbd09fadbd410fd22b700f85693ca48'
status: 'done'
review_loop_iteration: 0
context:
  - 'AGENTS.md'
  - 'project-context.md'
  - '_bmad-output/implementation-artifacts/epic-0-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The tracked Brainiac proof of concept contains useful synchronous Strands/Gemini experiments, but no durable, evidence-based decision record establishes what may migrate to the Onbora Core IA target. Similar prototype behavior could otherwise be mistaken for delivery of an MVP functional requirement.

**Approach:** Create one auditable baseline inventory anchored to commit `7c8434106bbd09fadbd410fd22b700f85693ca48`, classify every baseline runtime module and runtime dependency, and explicitly map prototype capabilities to their unmet MVP acceptance gaps. Make the approved inventory discoverable from the existing durable repository-context files used by BMad workflows.

## Boundaries & Constraints

**Always:** Base technical findings on the approved commit, use only `retain`, `adapt`, `replace`, or `retire` classifications with concise rationale, and distinguish current POC evidence from the asynchronous FastAPI/MCP hexagonal target. Record all POC capabilities that resemble an FR as gaps; no resemblance may be called MVP delivery. Keep all artifact prose in English.

**Ask First:** Changing a classification after the inventory is accepted, removing/replacing POC source files, altering the approved baseline revision, or expanding this story into runtime/test-baseline work requires human approval.

**Never:** Implement FastAPI, MCP, RAG, durable memory, provider failover, Streamlit changes, runtime launch instructions, or automated report tests in this story. Do not put Streamlit, synchronous I/O, or direct provider/tool integrations into a target domain core, and do not claim an FR is complete.

</frozen-after-approval>

## Code Map

- `AGENTS.md:1-33` -- managed brownfield context and the outside-managed-block pointer to the approved evidence revision and provisional inventory.
- `project-context.md:1-19` -- durable workflow context that identifies POC behavior as migration input, requires Epic-0 classification before change, and points to provisional classifications.
- `_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md:3-146` -- provisional decision record, reproducible 12-path scope, baseline evidence anchors, runtime/dependency classifications, POC-to-MVP gaps, and audit checks.
- `_bmad-output/implementation-artifacts/epic-0-context.md:1-35` -- authoritative Epic 0 constraints, verified baseline SHA, scope, and cross-story dependency.
- `_bmad-output/planning-artifacts/epics.md` -- Story 0.1 acceptance criteria; it establishes the intent but does not itself inventory source evidence.
- `7c8434106bbd09fadbd410fd22b700f85693ca48:src/config.py:9-30` -- synchronous Gemini-only model creation; evidence for replacement by validated async provider configuration.
- `7c8434106bbd09fadbd410fd22b700f85693ca48:src/multi_agent.py:48-83` and `src/conversation_report.py:13-88` -- POC agent/report behaviors whose limited reuse and MVP gaps must be recorded.
- `7c8434106bbd09fadbd410fd22b700f85693ca48:src/agent.py`, `src/response.py`, `src/main.py`, `src/tools/`, and `streamlit_app.py` -- remaining tracked POC runtime paths to classify without modifying them.
- `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:1-6` and `.env.example:1-10` -- baseline runtime dependency and non-secret configuration evidence.

## Tasks & Acceptance

**Execution:**

- [x] `_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md` -- create the authoritative audit for the exact approved SHA: scope and reproduction commands; a complete decision matrix for tracked runtime Python modules, entry points, runtime configuration, and every runtime dependency; exclusions for non-runtime tracked dotfiles; and a POC-to-FR/Story assessment that names each unmet acceptance gap and states that no FR is delivered.
- [x] `AGENTS.md` -- append (outside the managed `bmad:context` block) a link to the accepted inventory, retaining the generated brownfield rules, exact baseline revision, and target-domain isolation warning.
- [x] `project-context.md` -- add a concise pointer to the authoritative inventory so any BMad workflow loading repository context can find the accepted classifications without treating POC behavior as MVP delivery.
- [x] `_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md` -- validate the audit against `git ls-tree` and `git show` at the approved SHA, then perform the documented reproducibility and coverage checks before handoff.

**Acceptance Criteria:**

- Given commit `7c8434106bbd09fadbd410fd22b700f85693ca48`, when the baseline inventory is reviewed, then every tracked runtime module, entry point, runtime configuration artifact, and dependency has exactly one of `retain`, `adapt`, `replace`, or `retire`, with a concise evidence-based rationale.
- Given an excluded tracked artifact, when the inventory is reviewed, then it is explicitly identified as non-runtime rather than silently omitted from the audit scope.
- Given a POC capability resembling FR-3, FR-4, FR-6, FR-7, FR-15, FR-16, FR-19, or the Epic 2/3/5 capabilities, when it is assessed, then the inventory identifies the relevant unmet MVP behaviors and states that the FR remains undelivered.
- Given the accepted inventory and repository root, when a BMad workflow loads `AGENTS.md` and `project-context.md`, then both files remain readable, identify the brownfield constraints, and point to the same authoritative inventory.
- Given the inventory changes, when structural checks run, then the audit references the exact baseline SHA and produces no whitespace errors.

## Spec Change Log

## Design Notes

The inventory is a migration decision record, not an architecture implementation. It deliberately classifies `conversation_report.py` and Pydantic as adaptable source material, while classifying the synchronous transport, direct provider configuration, demo tools, and Streamlit runtime as replace/retire candidates. This preserves useful vocabulary and formatting logic without allowing prototype coupling to define the target architecture.

`baseline_commit` is the BMad workflow's review-diff base captured at implementation entry. `evidence_commit` is the fixed approved revision used for all POC findings in this story; the two fields deliberately serve different purposes.

The baseline commit predates the BMad planning foundation; it does not contain the two required context files. The current root-level `AGENTS.md` and `project-context.md` are therefore delivery artifacts of this story and must point to the inventory rather than being presented as evidence that they existed at the baseline SHA.

## Verification

**Commands:**

- `git ls-tree -r --name-only 7c8434106bbd09fadbd410fd22b700f85693ca48` -- expected: every in-scope runtime artifact is represented in the inventory or listed under explicit non-runtime exclusions.
- `git show 7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt` -- expected: all six baseline runtime dependencies and their decisions match the audit.
- `rg -n '7c8434106bbd09fadbd410fd22b700f85693ca48|## Runtime Classification|## POC-to-MVP Gap Assessment' _bmad-output/implementation-artifacts/brownfield-baseline-inventory.md` -- expected: baseline identity and the two required assessment sections are present.
- `rg -n 'brownfield-baseline-inventory' AGENTS.md project-context.md` -- expected: both durable context files point to the authoritative audit.
- `git diff --check` -- expected: no whitespace errors.
- `Get-Content -Raw _bmad-output/implementation-artifacts/brownfield-baseline-inventory.md, _bmad-output/implementation-artifacts/spec-0-1-establish-verified-brownfield-baseline.md | Select-String '[ \t]+$'` -- expected: no trailing whitespace in untracked Markdown artifacts.

## Suggested Review Order

**Evidence and migration decisions**

- Starts with the immutable evidence boundary and provisional decision status.
  [`brownfield-baseline-inventory.md:3`](brownfield-baseline-inventory.md#L3)

- Maps every runtime path to one explicit migration decision.
  [`brownfield-baseline-inventory.md:61`](brownfield-baseline-inventory.md#L61)

- Makes every POC-to-MVP similarity explicitly non-delivery.
  [`brownfield-baseline-inventory.md:93`](brownfield-baseline-inventory.md#L93)

**Workflow discoverability**

- Preserves generated safeguards while exposing the inventory outside the managed block.
  [`AGENTS.md:27`](../../AGENTS.md#L27)

- Lets every BMad workflow locate the provisional audit from durable context.
  [`project-context.md:18`](../../project-context.md#L18)

**Audit reproducibility**

- Revalidates manifest coverage, classifications, dependencies, and whitespace mechanically.
  [`brownfield-baseline-inventory.md:111`](brownfield-baseline-inventory.md#L111)

**Untracked Markdown whitespace check:**

```powershell
$markdownArtifacts = @(
  '_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md',
  '_bmad-output/implementation-artifacts/spec-0-1-establish-verified-brownfield-baseline.md'
)
foreach ($artifact in $markdownArtifacts) {
  if ([IO.File]::ReadAllText((Resolve-Path $artifact)) -match '(?m)[ \t]+(?=\r?$)') {
    throw "Trailing whitespace found in $artifact."
  }
}
```

Expected: no output or exception. This check covers the two untracked Markdown artifacts that `git diff --check` does not inspect.
