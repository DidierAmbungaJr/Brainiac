---
title: 'Runnable and Observable Core Service'
type: 'feature'
created: '2026-08-24'
status: 'done'
baseline_commit: 'c86135568021ea376dd62a3459a6e9b9b3a647e5'
review_loop_iteration: 0
context:
  - '{project-root}/project-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The repository contains a synchronous CLI POC but no independently runnable Core IA HTTP service. Integrators cannot verify service readiness, inspect an API contract, or receive predictable configuration and error diagnostics.

**Approach:** Establish the FastAPI service foundation with validated Pydantic Settings, a documented health resource, and one global API-error contract. Preserve the legacy POC modules as migration input while decoupling the new service from them.

## Boundaries & Constraints

**Always:** Use Python 3.11+ async FastAPI/Uvicorn and Pydantic v2 with `pydantic-settings`; load settings centrally from `.env`; fail validation before the app is ready; expose `GET /health`, OpenAPI, and the exact `{ "error": { "code", "message", "details" } }` envelope. Keep FastAPI in `src/api`/`src/main.py`, core exceptions framework-independent, and redact secrets/provider internals.

**Ask First:** Adding a versioned `/api/v1/health` alias, changing the required service-level configuration fields, or deleting/moving a POC module beyond the `src/main.py`/`src/config.py` target replacements requires explicit approval.

**Never:** Do not initialize Gemini, Strands, Streamlit, MCP, persistence, RAG, or an agent registry at service import/startup; do not require provider credentials for this foundation; do not introduce blocking production I/O or a client UI; do not expose raw exceptions or secrets.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|---------------|----------------------------|----------------|
| Service ready | Valid documented `.env`; ASGI startup | Async FastAPI app exposes OpenAPI and `GET /health` returns a typed successful JSON health payload | N/A |
| Invalid startup config | Missing required service setting or malformed/unsupported value | Settings validation aborts startup before the service is marked ready | Clear validation error; no partially initialized app |
| Domain failure | A route/dependency raises the core domain exception | JSON response has the standard nested error object and the domain HTTP status/code | Preserve safe message/details only |
| Invalid request / unexpected failure | FastAPI request validation fails or an uncaught exception occurs | Same error envelope with a stable client-safe code/message | Validation details are structured; unexpected errors are redacted |

</frozen-after-approval>

## Code Map

- `src/main.py:1-41` -- blocking POC CLI, classified **retire** in the approved inventory; replace its entry-point role with a FastAPI app factory/ASGI application without importing POC agents.
- `src/config.py:1-31` -- direct dotenv/Gemini construction, classified **replace**; make it service-only strict Settings configuration.
- `src/agent.py`, `src/multi_agent.py`, `src/response.py`, `streamlit_app.py` -- POC migration input; read-only for this story and must not be imported by the service.
- `src/api/router.py`, `src/api/v1/health.py` -- new inbound boundary and central API route registration from the architecture spine.
- `src/core/exceptions.py` -- new framework-independent error types used by global API handlers.
- `src/schemas/health.py`, `src/schemas/errors.py` -- new strict public response contracts.
- `requirements.txt`, `requirements.lock`, `requirements-dev.txt` -- current POC dependency manifests; pin FastAPI/Uvicorn/pydantic-settings and regenerate the lock consistently.
- `.env.example`, `README.md` -- adapt POC environment/start instructions to document the service and non-secret configuration.
- `tests/test_config.py:1-125` -- current tests are coupled to the retired CLI/Gemini config; replace/rehome only the affected assertions with service-foundation tests.
- `tests/conftest.py:1-12` -- autouse socket prohibition; use in-process clients and no live network calls.
- `_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md` -- authoritative provisional POC classifications; do not treat POC behavior as MVP delivery.

## Tasks & Acceptance

**Execution:**
- [x] `requirements.txt`, `requirements.lock`, `requirements-dev.txt` -- add and lock the selected FastAPI/Uvicorn/pydantic-settings runtime and compatible test dependencies so the documented install is reproducible.
- [x] `src/config.py`, `.env.example` -- replace Gemini-specific startup configuration with strict, documented service Settings and an explicit cached/accessor lifecycle that validates before readiness.
- [x] `src/core/__init__.py`, `src/core/exceptions.py`, `src/schemas/__init__.py`, `src/schemas/health.py`, `src/schemas/errors.py` -- introduce transport-independent core errors and strict public health/error schemas.
- [x] `src/api/__init__.py`, `src/api/router.py`, `src/api/v1/__init__.py`, `src/api/v1/health.py`, `src/main.py` -- assemble an async app factory, centralized route inclusion, health endpoint, lifespan validation, and global handlers for domain, request-validation, and unexpected errors.
- [x] `tests/test_config.py`, `tests/test_core_service.py` -- replace CLI-bound checks and add in-process coverage for valid/invalid configuration, startup fail-fast behavior, health/OpenAPI visibility, and every error-envelope path.
- [x] `README.md` -- document installation, required non-secret `.env` values, `uvicorn` launch command, `/health`, and generated OpenAPI documentation; distinguish the legacy POC from the new service.

**Acceptance Criteria:**
- Given a developer installs the pinned dependencies and supplies valid documented service settings, when they start the ASGI application, then it starts asynchronously and exposes usable OpenAPI documentation.
- Given a ready service, when a client sends `GET /health`, then it receives the documented structured successful health JSON response.
- Given a required service setting is absent, malformed, or unsupported, when the application begins startup, then settings validation clearly aborts before readiness or traffic handling.
- Given a domain, request-validation, or unexpected request failure, when the API responds, then its JSON body always follows the standard error envelope and does not expose secrets or raw implementation details.

## Spec Change Log

## Design Notes

Create settings during application lifespan rather than at module import so tests and process startup both exercise the same fail-fast boundary. App construction must remain side-effect free; the health endpoint reports only service status, because providers and agents are introduced by later stories.

## Verification

**Commands:**
- `uv run pytest` -- expected: all retained baseline and new service tests pass without network access.
- `uv run python -c "from fastapi.testclient import TestClient; from src.main import create_app; print(TestClient(create_app()).get('/health').json())"` -- expected: structured successful health JSON using documented valid environment configuration.
- `uv run python -c "from src.main import create_app; print(create_app().openapi()['openapi'])"` -- expected: OpenAPI generation succeeds.
- `git diff --check` -- expected: no whitespace errors.

## Suggested Review Order

**Service boundary and error contract**

- Creates the side-effect-free ASGI service and centralizes all public error translation.
  [`main.py:49`](../../src/main.py#L49)

- Converts domain, validation, HTTP, and unexpected failures into one safe envelope.
  [`main.py:60`](../../src/main.py#L60)

**Validated startup and observability**

- Anchors `.env` discovery to the project and rejects invalid service identity.
  [`config.py:11`](../../src/config.py#L11)

- Validates configuration before serving traffic during ASGI lifespan startup.
  [`main.py:42`](../../src/main.py#L42)

- Provides the typed readiness response without initializing future providers.
  [`health.py:14`](../../src/api/v1/health.py#L14)

**Contracts, reproducibility, and verification**

- Keeps expected domain failures independent of the FastAPI transport layer.
  [`exceptions.py:6`](../../src/core/exceptions.py#L6)

- Pins the runtime service dependencies alongside retained POC migration dependencies.
  [`requirements.txt:1`](../../requirements.txt#L1)

- Exercises startup, documentation, health, and every public error category in-process.
  [`test_core_service.py:22`](../../tests/test_core_service.py#L22)

- Documents the locked installation and service launch for integrators.
  [`README.md:1`](../../README.md#L1)
