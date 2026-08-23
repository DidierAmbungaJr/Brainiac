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
