# Project context — Onbora Core IA

This repository is a brownfield Python/Strands/Gemini POC, not a greenfield
project. The tracked source already provides a CLI assistant, Streamlit operator
interface, multi-agent supervision, research delegation, and structured
commercial-report generation.

Treat those capabilities as migration inputs only: they do not meet a PRD
functional requirement until its story acceptance criteria and automated tests
pass. The FastAPI/MCP Core IA remains the target architecture.

Before proposing or implementing a change, inspect the affected POC code and
the `bmad:context` block in `AGENTS.md`. Classify any affected POC component as
retain, adapt, replace, or retire under Epic 0 before removing or rewriting it.

Planning artifacts: `_bmad-output/planning-artifacts/`.
Delivery status: `_bmad-output/implementation-artifacts/sprint-status.yaml`.
Recorded, provisional classifications: [_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md](_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md), anchored to the approved evidence revision `7c8434106bbd09fadbd410fd22b700f85693ca48`.
POC behavior remains migration input, not MVP delivery; the classifications require human approval.
