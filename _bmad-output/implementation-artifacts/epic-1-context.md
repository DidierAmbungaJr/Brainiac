# Epic 1 Context: Integrable and Extensible AI Core

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish the reliable, independently runnable foundation of Onbora Core IA: an asynchronous, documented FastAPI service with fail-fast configuration and predictable API errors, plus extension points for agent registration and role-specific LLM selection. This lets client teams verify that the Core IA is ready to integrate before AI features arrive, while allowing product capabilities to grow without API-Gateway changes.

## Stories

- Story 1.1: Runnable and Observable Core Service
- Story 1.2: Register Specialized Agents Through a Stable Contract
- Story 1.3: Configure Per-Agent Multi-LLM Routing and Failover

## Requirements & Constraints

- Run a documented asynchronous ASGI/FastAPI Core IA service with automatically exposed OpenAPI/Swagger documentation and a structured health check. Client-facing applications remain API consumers; no Flutter or web UI belongs in this repository.
- Load configuration centrally from `.env` through strictly validated Pydantic Settings. Missing, malformed, unsupported, or incomplete required settings must stop startup clearly before a partially initialized service can accept traffic.
- Return all domain and unhandled request failures in one stable envelope: `{ "error": { "code": "...", "message": "...", "details": {} } }`. Do not expose credentials or provider implementation internals in client errors.
- Support per-agent-role LLM selection through a common provider interface. A configured primary provider must be eligible for a configured fallback on availability or quota failure; failover must be observable with the role and provider names.
- Make specialized agents extensible through a stable registration contract, so adding an agent or an MCP server never requires a change in API Gateway code. Duplicate registrations and incomplete agent contracts must fail explicitly rather than overwrite existing agents.
- Keep production I/O asynchronous throughout API, LLM, MCP, persistence, and RAG paths. The Core IA is the backend service only; direct server-side audio transcription, billing, and contract signing are out of scope.
- Pin the selected project dependencies and provide automated tests appropriate to the API, agent, and provider-extension foundation.

## Technical Decisions

- Target runtime is Python 3.11+ using FastAPI/Uvicorn, Pydantic v2, and `pydantic-settings`. FastAPI supplies the ASGI runtime and OpenAPI contract; Pydantic models supply strict, documented request and response contracts.
- Follow hexagonal architecture. API routers are inbound adapters; the domain core must not depend on FastAPI or another transport framework. External LLM and MCP integrations are outbound adapters accessed through ports or interfaces.
- Use the structural seed: `src/main.py` as the FastAPI entry point; `src/config.py` for settings; `src/api/` for inbound routing and dependencies; `src/core/` for orchestration, registry, and agents; `src/adapters/llm/` for provider adapters and factory; `src/schemas/` for Pydantic contracts. Create the associated `data/` and `tests/` roots as the service foundation develops.
- Centralize API v1 route registration. Health and future agent-discovery endpoints belong to the health inbound adapter; API-layer wiring stays separate from registry and provider logic.
- Model domain failures as explicit custom exceptions (including the common core error and agent/provider-specific failures). A global FastAPI exception middleware or handler owns conversion to the standard error envelope.
- The `BaseAgent` contract declares a unique agent ID, system prompt, declared MCP tools, input/output Pydantic schemas, and LLM role policy. `AgentRegistry` owns lifecycle and lookup; `LLMProviderFactory` resolves provider adapters by role behind a single interface.
- Use environment-driven role configuration for model routing. Keep exact provider secrets in configuration only; logs and client errors must identify operational context without leaking them.
- The existing synchronous Python/Strands/Gemini and Streamlit POC is migration input, not evidence that this target service or any FR is delivered. Preserve the brownfield retain/adapt/replace/retire decisions when introducing target components.

## Cross-Story Dependencies

- Story 1.1 provides the service lifecycle, validated configuration, health observability, API error contract, and testable FastAPI entry point that Stories 1.2 and 1.3 plug into.
- Story 1.2 provides the registry and agent contract consumed by Story 1.3 for role-based LLM selection. Both must preserve the API/core/adapters boundary so later agent, MCP, RAG, memory, streaming, report, and chat epics can attach without modifying API Gateway code.
