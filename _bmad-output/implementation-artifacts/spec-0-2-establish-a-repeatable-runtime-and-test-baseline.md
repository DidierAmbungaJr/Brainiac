---
title: 'Establish a Repeatable Runtime and Test Baseline'
type: 'chore'
created: '2026-08-23'
baseline_commit: '49abb955ee8a6268bbd417bdb0a68541e0a43b9d'
status: 'done'
review_loop_iteration: 0
context:
  - 'AGENTS.md'
  - 'project-context.md'
  - '_bmad-output/implementation-artifacts/epic-0-context.md'
  - '_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The existing Brainiac POC has no documented, repeatable setup or automated test suite. A developer cannot reliably separate a missing local package, missing non-secret configuration, unavailable Gemini access, and a report-path regression before migration work begins.

**Approach:** Establish a POC-only runtime baseline with pinned install inputs, non-secret launch and diagnostic instructions, and isolated report-generation tests that inject a fake agent rather than calling Gemini. Record failures as explicit baseline evidence and never treat a successful POC launch or test run as delivery of the FastAPI/MCP MVP.

## Boundaries & Constraints

**Always:** Preserve the approved Epic-0 classifications: retain the POC only as migration evidence; keep production I/O synchronous only inside its existing POC boundary; use documented non-secret `.env` variables; run tests without a live LLM, credentials, network, Streamlit UI, or Django backend; and keep all newly written repository prose in English.

**Ask First:** Replacing or removing a classified POC module, changing the approved evidence SHA, introducing target FastAPI/MCP architecture, or changing the POC's external behavior beyond diagnostic/documentation/test-baseline support requires human approval.

**Never:** Add a FastAPI service, MCP server, RAG, durable memory, provider failover, Docker/Compose stack, CI claim, Streamlit redesign, live-Gemini test, or production-MVP claim. Do not import `streamlit_app.py` in unit tests, place Streamlit or synchronous provider dependencies in a target domain core, or send data to `DJANGO_REPORT_URL` during baseline checks.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| POC launch | Installed pinned POC dependencies and a `.env` copied from the example with a valid Gemini key | The documented CLI (`python -m src.main`) or Streamlit command reaches the existing POC entry point. | State that an interactive prompt or model request requires reachable Gemini; this is POC behavior only. |
| Missing model credential | Dependencies installed but neither `GOOGLE_API_KEY` nor `GEMINI_API_KEY` set | CLI construction or Streamlit preflight identifies the missing credential before an agent call. | Preserve an actionable French error; baseline documentation gives the corrective non-secret setup step. |
| Unavailable dependency | A required package is not installed, or an optional Django URL points to an unavailable service | The documented baseline check/launch procedure identifies the failed dependency and its remediation without pretending the POC ran. | Return or surface the native actionable failure; optional Django is never contacted unless explicitly configured. |
| Isolated report generation | Message list or raw transcript plus injected fake callable agent returning `ConversationReport` | Formatting, validation/model dumping, UTC `generated_at`, and JSON serialization are covered without a Gemini request. | Empty transcript and absent/non-Pydantic structured output fail explicitly; no live fallback is attempted. |

</frozen-after-approval>

## Code Map

- `.env.example:1-10` -- complete non-secret POC configuration sample; document all variables and add any supported reporter-role override needed for a truthful baseline.
- `requirements.txt:1-6` -- current unpinned runtime manifest; turn it into a verified, repeatable POC dependency input and keep test tooling separate from runtime dependencies.
- `src/config.py:6-30` -- dotenv loading, Gemini credential precedence, role override selection, and explicit missing-key `RuntimeError`; do not make a provider call in tests.
- `src/main.py:8-41` -- CLI's documented module entry point, mode selection, construction-time configuration error, and blocking interactive loop.
- `streamlit_app.py:17-38,53-70,72-127` -- POC UI entry point and key preflight; report generation is synchronous and Django posting is optional, UI-owned, and excluded from automation.
- `src/conversation_report.py:13-26` -- POC `ConversationReport` validation boundary; categorical strings remain unconstrained migration input, not an MVP contract.
- `src/conversation_report.py:54-62` -- deterministic transcript role mapping, trimming, omission, and ordering to test.
- `src/conversation_report.py:65-93` -- fake-agent injection seam; valid Pydantic output is JSON-dumped with UTC timestamp and serialized without a live model.
- `src/conversation_report.py:96-123` -- Markdown review rendering used by Streamlit; test only as POC presentation behavior if retained in the baseline suite.
- `src/multi_agent.py:88-113` -- real report orchestrator builds provider-backed agents; document it but keep it out of isolated unit tests.
- `_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md:34,61-86,99-101` -- approved provisional classifications and explicit statement that Story 0.2 owns launch/test-baseline work.

## Tasks & Acceptance

**Execution:**

- [x] `requirements.txt` and `requirements-dev.txt` -- define a verified, pinned POC runtime dependency set plus a separate pinned pytest test input, with an install command that works from a clean virtual environment; do not introduce target-runtime dependencies.
- [x] `README.md` -- create concise POC-baseline instructions covering virtual-environment setup, dependency installation, copying `.env.example`, every non-secret setting and supported role override, CLI/Streamlit commands, fake-only test command, expected missing-dependency/credential behavior, and the optional Django boundary; label every result as POC baseline evidence, not MVP delivery.
- [x] `.env.example` -- align the non-secret example with every supported model-role override documented for the POC without adding secrets or implying provider abstraction.
- [x] `tests/test_conversation_report.py` -- add fake-agent unit tests for schema validation, transcript mapping/trimming/order, valid generation/model serialization with a UTC timestamp, JSON output, and explicit empty/malformed structured-output failures; assert that injected fakes are used instead of `create_report_agent`.
- [x] `tests/test_config.py` -- add no-network configuration coverage for the explicit absent-Gemini-key failure and documented credential precedence/role model selection, using mocks where provider construction would otherwise occur.
- [x] `tests/` test support as needed -- make test discovery deterministic without importing Streamlit or creating a live Gemini/Django call; keep fakes minimal and local to the tests.

**Acceptance Criteria:**

- Given a clean supported Python environment and the documented non-secret setup, when a developer follows the baseline guide, then they can start the existing CLI or Streamlit POC with the documented commands and understand that a valid Gemini credential is required for live interaction.
- Given the report-generation helpers, when the baseline tests run with an injected fake agent/model, then `ConversationReport` validation, transcript formatting, generation serialization, and JSON output are covered without a live LLM request.
- Given an expected package, credential, Gemini service, or optional Django dependency is unavailable, when baseline commands or checks are run, then the failure and remediation are explicit and no POC behavior is represented as FastAPI/MCP MVP delivery.
- Given the POC dependency/test inputs change, when the documented clean-environment install and test command run, then their direct versions and successful baseline result are recorded reproducibly.

## Spec Change Log

## Design Notes

Use the `agent=` parameter of `generate_conversation_report` as the test seam: a tiny callable fake returns a result object whose `structured_output` is a real `ConversationReport`. This avoids `create_report_agent()`, `create_model()`, credentials, and network I/O while preserving the report function's actual formatting and serialization path.

Keep `create_report_orchestrator()` out of these unit tests because it constructs real provider-backed agents. Validate timestamps by parsing their ISO-8601 UTC value instead of comparing wall-clock text.

## Verification

**Commands:**

- `python -m venv .venv` -- expected: isolated local environment is created.
- `.\.venv\Scripts\python -m pip install -r requirements-dev.txt` -- expected: the pinned POC and test dependencies install from the declared inputs.
- `.\.venv\Scripts\python -m pytest` -- expected: all fake-only baseline tests pass without Gemini, Streamlit UI, Django, or network access.
- `.\.venv\Scripts\python -m src.main` -- expected: with no key, prints the documented configuration error; with configured dependencies and valid credential, reaches the existing interactive POC prompt.
- `.\.venv\Scripts\streamlit run streamlit_app.py` -- expected: with no key, shows the documented configuration preflight; with a valid credential, opens the existing POC UI.
- `git diff --check` -- expected: no whitespace errors.

## Suggested Review Order

**Baseline contract**

- Defines the POC-only setup, diagnostics, and evidence boundary.
  [`README.md:1`](../../README.md#L1)

- Locks every resolved runtime and test dependency version.
  [`requirements.lock:1`](../../requirements.lock#L1)

- Keeps direct POC dependency intent readable alongside the lock.
  [`requirements.txt:1`](../../requirements.txt#L1)

**Runtime safeguards**

- Makes copied sample configuration fail clearly until a real key is supplied.
  [`.env.example:1`](../../.env.example#L1)

- Rejects whitespace-only report input before invoking an agent.
  [`conversation_report.py:70`](../../src/conversation_report.py#L70)

**Isolated baseline verification**

- Blocks all network connections during baseline tests.
  [`conftest.py:6`](../../tests/conftest.py#L6)

- Exercises CLI modes, credential errors, role overrides, and hierarchy construction.
  [`test_config.py:15`](../../tests/test_config.py#L15)

- Covers report formatting, fake-agent serialization, errors, and review Markdown.
  [`test_conversation_report.py:44`](../../tests/test_conversation_report.py#L44)

- Guards documented remediation and POC-only boundaries against accidental drift.
  [`test_runtime_baseline_docs.py:4`](../../tests/test_runtime_baseline_docs.py#L4)

**Follow-up boundary**

- Preserves the strict-report-contract gap for Epic 4 work.
  [`deferred-work.md:1`](deferred-work.md#L1)

### Review Findings

- [x] [Review][Patch] Make the locked baseline installable across supported platforms [requirements.lock:72] — decision: support multiple platforms; regenerated with a Windows platform marker.
- [x] [Review][Patch] Keep baseline tests free of real Gemini provider construction [tests/test_config.py:55]
- [x] [Review][Patch] Surface an actionable optional-Django failure and remediation [streamlit_app.py:121]
