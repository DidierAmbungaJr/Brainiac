# Brainiac POC Runtime Baseline

This repository contains a synchronous Python/Strands/Gemini proof of concept
(POC). The commands and test results below are baseline evidence for the POC;
they do not deliver, validate, or claim the FastAPI/MCP Core IA MVP.

## Supported Python and setup

Use Python 3.12 on Windows, macOS, or Linux. Create a clean virtual
environment from the repository root, then install the locked POC runtime and
test inputs. The lock uses standard platform markers for Windows-only
dependencies.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
```

Copy the non-secret configuration sample before launching the POC:

```powershell
Copy-Item .env.example .env
```

Set either `GOOGLE_API_KEY` (preferred when both are set) or `GEMINI_API_KEY`
in `.env`. A valid Gemini credential and reachable Gemini service are required
only for interactive model requests; baseline unit tests do not use either.

The remaining non-secret settings are:

- `GEMINI_MODEL`: default Gemini model identifier.
- `GEMINI_SUPERVISOR_MODEL`, `GEMINI_RESEARCHER_MODEL`, and
  `GEMINI_REPORTER_MODEL`: optional role-specific model overrides. An empty
  override falls back to `GEMINI_MODEL`.
- `GEMINI_TEMPERATURE` and `GEMINI_MAX_OUTPUT_TOKENS`: Gemini generation
  parameters used by this POC.
- `AGENT_SESSION_ID` and `AGENT_SESSIONS_DIR`: local file-session values for
  the CLI POC.
- `BRAINIAC_AGENT_MODE`: use `simple` for the single agent; any other value
  uses the hierarchical POC team.
- `DJANGO_REPORT_URL`: optional Streamlit-owned report endpoint. Leave it
  empty for baseline checks and tests; no baseline command sends a request to
  it.

## POC commands and diagnostics

Run the existing CLI POC:

```powershell
.\.venv\Scripts\python -m src.main
```

With no Gemini credential, the CLI prints the existing French configuration
error before constructing an agent. Copy `.env.example` to `.env` and set a
credential to correct it. With a credential, the command reaches the existing
interactive prompt; a subsequent model request still requires Gemini access.

Run the existing Streamlit POC:

```powershell
.\.venv\Scripts\streamlit run streamlit_app.py
```

With no credential, Streamlit shows its existing configuration preflight.
With a credential, it opens the POC UI, whose live interactions require Gemini
access. The optional Django integration is only attempted from its explicit
UI action when `DJANGO_REPORT_URL` is configured; it is outside the baseline
test suite.

If a package is absent, rerun the pinned installation command and keep the
native installer error as evidence that the POC did not start. If Gemini is
unavailable after configuration, keep the surfaced provider error as POC
baseline evidence; do not represent it as an MVP result.

If the optional Django URL is configured but its service is unavailable, the
Streamlit action reports that it could not reach Django and asks you to verify
`DJANGO_REPORT_URL` and the service. The report remains available locally; this
is POC baseline evidence, not an MVP result.

## Fake-only baseline tests

Run the isolated suite with:

```powershell
.\.venv\Scripts\python -m pytest
```

The tests inject a local fake report agent and replace Gemini construction.
They do not import `streamlit_app.py`, create a live Gemini request, access the
network, or contact `DJANGO_REPORT_URL`. A passing result validates only the
documented POC runtime and report-path baseline.

## Verification record

On 2026-08-23, this baseline was installed and checked on Windows with Python
3.12.1. `pip check` reported no broken requirements, the fake-only suite
reported 24 passing tests, the CLI displayed its missing-credential diagnostic,
and Streamlit reported version 1.62.0. This is POC baseline evidence only.
