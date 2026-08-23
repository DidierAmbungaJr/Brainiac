<!-- bmad:context -->
<!-- Verified 2026-08-23 against 7c8434106bbd09fadbd410fd22b700f85693ca48. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## onboracoreai

Onbora Core IA is currently a Python/Strands/Gemini brownfield POC. `src/` contains the CLI, agent orchestration, and commercial-report prototype; `streamlit_app.py` is its operator UI. The FastAPI/MCP MVP target and migration decisions live in `_bmad-output/planning-artifacts/`.

## Where things are

- Current POC entry points: `src/main.py` and `streamlit_app.py`.
- Agent and report prototypes: `src/agent.py`, `src/multi_agent.py`, and `src/conversation_report.py`.
- Product target, architecture, and backlog: `_bmad-output/planning-artifacts/`.
- Delivery status: `_bmad-output/implementation-artifacts/sprint-status.yaml`.

## Conventions that differ from defaults

- Treat the existing POC as migration input, not as proof that an MVP requirement is delivered.
- Before replacing POC code, classify the affected component as retain, adapt, replace, or retire in Epic 0.

## Known pitfalls

- The FastAPI/MCP directory tree in the architecture is a target structural seed, not the current repository structure.
- Do not let Streamlit or synchronous POC dependencies enter the target domain core.

<!-- /bmad:context -->

## Authoritative Brownfield Inventory

The approved baseline evidence and recorded, provisional retain/adapt/replace/retire
decisions are in
[_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md](_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md).
It is anchored to `7c8434106bbd09fadbd410fd22b700f85693ca48`; POC behavior
remains migration input and not MVP delivery.
