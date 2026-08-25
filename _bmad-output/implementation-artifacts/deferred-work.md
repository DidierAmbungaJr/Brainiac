- source_spec: `_bmad-output/implementation-artifacts/spec-0-2-establish-a-repeatable-runtime-and-test-baseline.md`
  summary: Enforce `ConversationReport` validation when a report agent returns a different Pydantic model.
  evidence: The pre-existing POC intentionally accepts any `BaseModel` at `src/conversation_report.py:82-83`; the approved inventory records the strict contract as an Epic 4 migration gap, so changing it is outside this baseline story.
