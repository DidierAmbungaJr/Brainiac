# Epic 0 Context: Existing POC Reconciliation and Delivery Baseline

<!-- Compiled from planning artifacts. Edit freely. Regenerate with compile-epic-context if planning docs change. -->

## Goal

Establish a factual, auditable starting point for evolving the existing Brainiac proof of concept into Onbora Core IA. The team must preserve useful learning without duplicating, silently discarding, or treating prototype behavior as delivered MVP functionality; a verified component inventory and reproducible baseline make later migration decisions safe and traceable.

## Stories

- Story 0.1: Establish the Verified Brownfield Baseline
- Story 0.2: Establish a Repeatable Runtime and Test Baseline

## Requirements & Constraints

- Treat the repository as a brownfield Python/Strands/Gemini POC. Its CLI assistant, Streamlit operator interface, supervisor/researcher delegation, structured commercial-report generation, optional Django report POST, and per-role Gemini model setting are migration inputs only.
- Record the approved baseline revision before evaluating the POC. The planning baseline identifies `7c8434106bbd09fadbd410fd22b700f85693ca48` as the verified repository revision; the inventory must make its findings auditable against that revision.
- Classify every tracked runtime module and dependency as **retain**, **adapt**, **replace**, or **retire**, and give a concise, evidence-based rationale for each decision. Do not remove or rewrite affected POC code before its decision is recorded.
- For every POC capability that resembles a product requirement, record its gap to the MVP acceptance criteria. Existing behavior must never be counted as an implemented functional requirement merely because it has a similar name or outcome.
- Make both `AGENTS.md` and `project-context.md` available as durable repository context so future BMad workflows begin with the brownfield constraints.
- Document non-secret setup required to launch the existing CLI or Streamlit POC. Baseline checks must surface unavailable external services or credentials explicitly and must not make production-MVP claims.
- Cover the POC report-generation path with isolated tests using a fake agent or model. The tests must exercise schema validation, transcript formatting, and serialization without a live LLM call.

## Technical Decisions

- The current POC is synchronous and organized around `src/agent.py`, `src/multi_agent.py`, `src/conversation_report.py`, `src/main.py`, `src/config.py`, and `streamlit_app.py`. Inventory these as existing implementation, not as the target architecture.
- Preserve the distinction between POC and target: the target is an asynchronous FastAPI/MCP Core IA using hexagonal architecture. The planned `src/api`, `src/core`, `src/adapters`, `src/schemas`, `data`, and `tests` structure is a future structural seed, not evidence that those components already exist.
- Domain code in the target must not depend on transport frameworks. Sub-agents must reach external systems only through MCP tool ports or memory ports; avoid allowing Streamlit, transport, or synchronous I/O dependencies to enter the domain core during any retained or adapted migration.
- Existing report code is only a partial precursor to the eventual strict `ConversationReport` contract. Existing multi-agent coordination has no established registry contract, and existing role-level Gemini selection has no provider abstraction or failover; preserve these gaps in the inventory.
- No FastAPI application or routes, MCP servers, hybrid RAG engine, durable-memory adapter, Docker assets, or automated-test suite should be represented as already delivered by the POC unless the verified inventory finds new evidence at the baseline revision.

## Cross-Story Dependencies

- Complete and accept the component/dependency classification before deciding what can be carried forward into the repeatable runtime and test baseline.
- Epic 1 and later epics depend on this reconciliation: their implementation must use the approved retain/adapt/replace/retire decisions and must not infer MVP delivery from prototype capabilities.
