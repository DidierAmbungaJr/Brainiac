---
title: "Sprint Change Proposal — Adopt the Existing POC as the Delivery Baseline"
status: approved
date: 2026-08-23
project: onboracoreai
mode: batch
scope: major
---

# Sprint Change Proposal — Adopt the Existing POC as the Delivery Baseline

## 1. Issue Summary

### Trigger

Planning started after implementation had already begun. The repository contains two commits:

- `34f6f2b` (2026-08-20): initial Gemini/Strands assistant.
- `7c84341` (2026-08-21): multi-agent coordination, structured commercial reporting, and a Streamlit interface.

The current source is therefore a **brownfield proof of concept (POC)**, not a greenfield repository.

### Problem statement

The PRD, architecture spine, and epic breakdown were produced as if no implementation existed. They currently describe the target Core IA correctly, but they do not identify what has already been built, what can be retained, or the gap between the POC and the MVP. Future BMad work could duplicate, overwrite, or incorrectly mark existing work as complete.

### Evidence

| Existing source | Verified capability | MVP status |
|---|---|---|
| `src/agent.py`, `src/main.py` | Gemini/Strands CLI assistant with file-backed session manager | POC only |
| `src/multi_agent.py` | supervisor, researcher delegation, and report orchestration | POC only; no registry contract |
| `src/conversation_report.py` | Pydantic `ConversationReport` and structured output generation | partial precursor to FR-18 |
| `streamlit_app.py` | interactive chat and manually approved report download / Django POST | POC UI; not the FastAPI API required by the PRD |
| `src/config.py` | per-role Gemini model environment override | partial precursor to FR-6; no provider abstraction or failover |

No FastAPI application, API routes, MCP servers, RAG engine, durable memory adapter, automated tests, Docker assets, or sprint status file are present in the tracked source tree.

## 2. Impact Analysis

### Checklist status

| Item | Status | Finding |
|---|---|---|
| 1.1 Trigger | [x] Done | Planning followed an already-started POC rather than preceding it. |
| 1.2 Core problem | [x] Done | Planning artifacts assume a greenfield repository. |
| 1.3 Evidence | [x] Done | Git history and current source establish the POC baseline. |
| 2.1–2.5 Epic impact | [x] Done | Add an explicit reconciliation epic before the existing delivery epics; do not reorder product epics 1–5. |
| 3.1 PRD impact | [x] Done | Product scope is unchanged; the PRD needs a brownfield baseline and explicit completion semantics. |
| 3.2 Architecture impact | [x] Done | The architecture must distinguish transitional POC code from the production structural seed. |
| 3.3 UX impact | [N/A] Skip | Streamlit is a POC operator interface; client Flutter/Web UX remains out of scope. |
| 3.4 Other artifacts | [!] Action-needed | Add repository context and sprint tracking; establish test and run baselines during reconciliation. |
| 4.1 Direct adjustment | Viable | Add a baseline/reconciliation epic and amend the planning artifacts. Effort: Medium; risk: Low. |
| 4.2 Rollback | Not viable | No evidence supports reverting the POC; it contains reusable learning and a partial report contract. Effort: High; risk: High. |
| 4.3 MVP review | Viable but not recommended | The MVP remains valid. A scope reduction is not justified before the POC gap is assessed. |

### Epic impact

The current epics remain relevant. Their completion must be measured against their acceptance criteria, not against the existence of similarly named POC code.

| Epic | Impact |
|---|---|
| Epic 1 — Integrable and Extensible AI Core | Reuse lessons from the existing supervisor and per-role model settings, but implement the required FastAPI service, registry, provider abstraction, validation, and failover. |
| Epic 2 — Trusted Orange Knowledge and Company Intelligence | No shipped equivalent exists; retain scope unchanged. |
| Epic 3 — Real-Time Field Copilot | No shipped equivalent exists; retain scope unchanged. |
| Epic 4 — CRM-Ready Visit Reports | Reconcile `ConversationReport` with the planned public contract and retain it only after tests and API integration validate it. |
| Epic 5 — Inbound Prospect Qualification and Lead Handoff | The Streamlit conversation is not the required SSE API; retain scope unchanged. |

## 3. Recommended Approach

Adopt a **hybrid direct adjustment**:

1. Add a new pre-delivery **Epic 0: Existing POC Reconciliation and Delivery Baseline**.
2. Record a concise, verified repository context so all BMad workflows treat this as a brownfield project.
3. Amend the PRD and architecture to distinguish the current POC from the approved MVP target.
4. Keep Epics 1–5 and the MVP scope unchanged until Epic 0 produces a concrete retain/adapt/replace decision for every POC component.

This approach avoids a destructive rewrite while preventing unverified POC behavior from being counted as delivered product functionality.

**Estimated effort:** Medium (one planning/reconciliation epic before normal delivery).

**Risk:** Medium. The main risk is accidental coupling to the synchronous, Streamlit-centric POC. It is mitigated by treating the POC as an input to be evaluated, not as the production architecture.

**Timeline impact:** one short foundational epic before Epic 1. Subsequent implementation should proceed with fewer false starts.

## 4. Detailed Change Proposals

### A. Repository-wide BMad context

Create `AGENTS.md` with a verified `bmad:context` block and a root `project-context.md` companion.

**New facts to record:**

- This is a brownfield Python POC, not a greenfield repository.
- `src/` and `streamlit_app.py` are the current POC baseline and may not be deleted or claimed production-ready without an explicit reconciliation decision.
- The target remains the FastAPI-based Onbora Core IA described in the approved PRD and architecture spine.
- Existing POC capabilities map only to partial precursors: per-role Gemini selection (FR-6), multi-agent orchestration (FR-7), and `ConversationReport` (FR-18).
- Every future BMad planning, architecture, story, and implementation workflow must inspect the current affected code and this baseline before proposing replacements.

**Rationale:** nearly all installed BMad workflows load `project-context.md`, while `AGENTS.md` gives code-facing agents the authoritative repository constraints.

### B. PRD update

**Section:** insert after `## 0. Document Purpose`.

**OLD:**

```markdown
This document specifies the target Core IA without an implementation baseline.
```

**NEW:**

```markdown
## 0.1 Existing Implementation Baseline

This project is brownfield. As of 2026-08-23, the repository contains a
Python/Strands/Gemini POC with a CLI assistant, Streamlit interface, supervisor,
researcher delegation, structured commercial report generation, and optional
Django report POST. These components are discovery and migration inputs only.
They do not satisfy a functional requirement unless their corresponding epic
acceptance criteria and automated tests are met.

The MVP target remains the FastAPI-based Onbora Core IA defined in this PRD.
Before implementing a target component, the team must classify the related POC
code as retain, adapt, replace, or retire and preserve a traceable rationale.
```

**Rationale:** preserves product intent while making completion and migration semantics unambiguous.

### C. Architecture spine update

**Section:** insert before `## 1. Design Paradigm`.

**OLD:**

```markdown
The structural seed is presented as the repository's current structure.
```

**NEW:**

```markdown
## 0. Brownfield Transition Baseline

The current repository is a synchronous Python/Strands POC organized around
`src/agent.py`, `src/multi_agent.py`, `src/conversation_report.py`, and
`streamlit_app.py`. It provides useful behavior but does not yet implement the
hexagonal, async FastAPI/MCP architecture below.

The source tree in section 5 is the **target structural seed**, not a claim
about files that already exist. During Epic 0, each POC component must receive a
retain/adapt/replace/retire decision. The POC must not leak transport, Streamlit,
or synchronous I/O dependencies into the domain core.
```

**Rationale:** eliminates the false present-tense description of the planned directory structure.

### D. Epic and story update

**Section:** insert before `## Epic 1: Integrable and Extensible AI Core` and add to the epic list.

**NEW EPIC:**

```markdown
## Epic 0: Existing POC Reconciliation and Delivery Baseline

The delivery team can evolve the existing Brainiac POC into the Onbora Core IA
without duplicating, silently discarding, or misrepresenting existing work.

### Story 0.1: Establish the Verified Brownfield Baseline

As a delivery team,
I want an auditable inventory of the existing POC and its relationship to the
MVP requirements,
So that implementation decisions start from verified facts.

Acceptance criteria:

- Given the repository at the approved baseline commit, when the inventory is
  completed, then every tracked runtime module and dependency is classified as
  retain, adapt, replace, or retire with rationale.
- Given a POC capability resembles an FR, when it is assessed, then the
  inventory states the missing acceptance criteria and does not mark the FR done.
- Given the baseline is accepted, when any BMad workflow starts, then it can
  load `AGENTS.md` and `project-context.md` as repository context.

### Story 0.2: Establish a Repeatable Runtime and Test Baseline

As a developer,
I want to run and test the current POC reproducibly before migration,
So that later architecture changes have a known behavioral reference.

Acceptance criteria:

- Given documented non-secret environment variables, when a developer follows
  the baseline instructions, then they can launch the CLI or Streamlit POC.
- Given the report-generation path, when unit tests run with a fake agent/model,
  then schema validation, transcript formatting, and serialization behavior are
  covered without a live LLM call.
- Given the baseline checks run, when an external dependency is unavailable,
  then the failure is explicit and no production-MVP claim is made.
```

**Rationale:** establishes a dependency-safe first epic while retaining the current Epic 1–5 IDs and scope.

### E. Sprint tracking

Create `_bmad-output/implementation-artifacts/sprint-status.yaml` with Epic 0 as `in-progress` only after this proposal is approved; Epics 1–5 remain `backlog`.

**Rationale:** the project needs explicit status tracking, and no current artifact supports reliable progress reporting.

## 5. Implementation Handoff

**Scope classification:** Major — planning and architecture references need coordinated correction, but the product goal does not change.

| Recipient | Responsibility | Success criterion |
|---|---|---|
| Product Manager | Apply the PRD baseline amendment and confirm MVP scope remains unchanged. | PRD explicitly distinguishes POC from MVP. |
| Solution Architect | Apply the architecture transition baseline and validate the retain/adapt/replace/retire decisions. | Target architecture does not misstate current implementation. |
| Developer | Execute Epic 0, document the runtime/test baseline, and create the tracking file. | POC baseline is reproducible and every POC component is classified. |
| BMad workflows | Load the repository context before all future planning and implementation. | No future artifact assumes a greenfield codebase. |

### Approval

Approved by Steve on 2026-08-23. The PRD, architecture, epic, sprint-tracking,
and shared repository-context changes were applied on 2026-08-23.
