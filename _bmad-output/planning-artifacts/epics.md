---
stepsCompleted: [1, 2, 3, 4]
inputDocuments:
  - "_bmad-output/planning-artifacts/prds/prd-onboracoreai-2026-08-21/prd.md"
  - "_bmad-output/planning-artifacts/architecture/architecture-onboracoreai-2026-08-21/ARCHITECTURE-SPINE.md"
---

# onboracoreai - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for onboracoreai, decomposing the requirements from the PRD and architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-1: Provide `POST /api/v1/copilot/stream` to receive text fragments and stream status events and `SuggestionCard` events; emit a suggestion within 1.5 seconds when an intent is detected.

FR-2: Provide `POST /api/v1/copilot/feedback` to accept a suggestion ID, accepted/rejected status, and optional reason, then update session memory.

FR-3: Provide `POST /api/v1/reports/generate` to turn a transcript or session ID into a strictly validated `ConversationReport` JSON object.

FR-4: Provide `POST /api/v1/company/research` to return a company summary from its name and/or website.

FR-5: Provide `POST /api/v1/chat/message` to manage inbound prospect conversation turns and stream responses.

FR-6: Allow the orchestrator to assign an LLM provider/model per agent role.

FR-7: Allow a new sub-agent to register through a standard class that declares its prompt, MCP tools, input schema, and structured output schema.

FR-8: Analyse copilot chunks but create a `SuggestionCard` only when configurable confidence reaches the threshold or a major objection is detected.

FR-9: Require every `SuggestionCard` to contain `need_detected`, `suggested_offer`, `pitch_argument`, `confidence_score`, and `card_id`.

FR-10: Ingest Orange B2B source documents in PDF, Markdown, and JSON formats.

FR-11: Run dense semantic retrieval and BM25 lexical retrieval for every RAG query.

FR-12: Inject the most relevant Top-K RAG document chunks into the requesting agent's prompt.

FR-13: Maintain working session memory and asynchronously compress older conversation context while preserving established facts and accepted/rejected cards.

FR-14: Persist durable company and contact facts and reinject them in future interactions with the same company.

FR-15: Expose MCP CRM/Django tools for client history, lead creation, client notes, and conversation-report saving.

FR-16: Expose MCP web-reconnaissance tools for public company research.

FR-17: Expose the MCP `search_orange_catalog(query, category, limit)` tool to all sub-agents.

FR-18: Define and validate a strict `ConversationReport` containing summary, key points, customer needs, pain points, objections, recommended next actions, interest level, lead status, qualification score, and missing information.

FR-19: Retry output correction when a generated report JSON cannot be parsed before returning an error.

### NonFunctional Requirements

NFR-1: End-to-end copilot `SuggestionCard` latency via SSE must not exceed 1,500 ms after receipt of a text chunk.

NFR-2: All commercial-report outputs must validate against the Pydantic model without unhandled exceptions.

NFR-3: Adding a sub-agent or MCP server must not require changes to the API Gateway code.

NFR-4: The system must be able to fail over to a configured backup LLM provider when the primary provider is unavailable or quota-limited.

NFR-5: Context compression must keep the active prompt below 8,000 tokens regardless of meeting duration.

### Additional Requirements

- Implement the greenfield repository using Python 3.11+, FastAPI/Uvicorn, Pydantic v2 and Pydantic Settings, async SQLAlchemy, and the MCP Python SDK; pin the selected dependencies in project configuration.
- Maintain Hexagonal Architecture: the domain core must not depend on transport frameworks; sub-agents access external systems only through MCP tool ports or memory ports.
- Keep all production I/O async; do not introduce blocking I/O in API, LLM, MCP, persistence, or RAG paths.
- Create the structural seed defined by the architecture: `src/api`, `src/core`, `src/adapters`, `src/schemas`, `data`, and `tests`.
- Standardize SSE events as `status`, `suggestion_card`, `token`, `error`, and `done`.
- Use strict Pydantic v2 models for API payloads, agent inputs/outputs, `SuggestionCard`, `ConversationReport`, and `CompanyProfile`; expose these via OpenAPI.
- Use ISO 8601 UTC timestamps and UUIDv4 session and suggestion-card IDs.
- Centralize configuration in validated Pydantic Settings loaded from `.env`.
- Use domain exceptions and FastAPI middleware to return `{ "error": { "code": "...", "message": "...", "details": {} } }` for failures.
- Implement hybrid retrieval with dense embeddings, BM25, and Reciprocal Rank Fusion before Top-K context injection.
- Support in-memory session storage locally with optional Redis; use SQLite for development and PostgreSQL for production entity persistence.
- Provide tests for agents, hybrid RAG, memory compression, copilot streaming, reports API, and MCP servers; Dockerize the service with a local Docker Compose stack.

### UX Design Requirements

No UX design contract was provided. Client-facing Flutter and web UX are outside this Core IA repository's MVP scope.

### FR Coverage Map

FR-1: Epic 3 - Real-time field copilot streaming.

FR-2: Epic 3 - Commercial feedback and session adjustment.

FR-3: Epic 4 - Visit-report generation.

FR-4: Epic 2 - Company intelligence and preparation.

FR-5: Epic 5 - Inbound prospect conversation.

FR-6: Epic 1 - Per-agent multi-LLM configuration.

FR-7: Epic 1 - Extensible agent registry.

FR-8: Epic 3 - Confidence-gated and objection-aware copilot suggestions.

FR-9: Epic 3 - Complete `SuggestionCard` contract.

FR-10: Epic 2 - Multi-format Orange catalog ingestion.

FR-11: Epic 2 - Hybrid dense and BM25 retrieval.

FR-12: Epic 2 - Top-K retrieval context injection.

FR-13: Epic 3 - Working memory and automatic context compression.

FR-14: Epic 2 - Durable company and contact memory.

FR-15: Epic 4 - MCP CRM/Django integration and report saving.

FR-16: Epic 2 - MCP web reconnaissance.

FR-17: Epic 2 - MCP Orange catalog search.

FR-18: Epic 4 - Strict `ConversationReport` validation.

FR-19: Epic 4 - Report JSON correction and retry.

## Epic List

### Epic 0: Existing POC Reconciliation and Delivery Baseline

The delivery team can evolve the existing Brainiac POC into the Onbora Core IA without duplicating, silently discarding, or misrepresenting existing work.

### Epic 1: Integrable and Extensible AI Core

Client application teams can integrate a reliable Core IA API, while the product team can configure LLM providers and add specialized agents without modifying the API Gateway.

**FRs covered:** FR-6, FR-7

### Epic 2: Trusted Orange Knowledge and Company Intelligence

Sales representatives can prepare for a company and receive grounded Orange B2B recommendations based on hybrid catalog retrieval and durable company knowledge.

**FRs covered:** FR-4, FR-10, FR-11, FR-12, FR-14, FR-16, FR-17

### Epic 3: Real-Time Field Copilot

Sales representatives receive fast, relevant, non-intrusive advice cards during a meeting, and their feedback improves the active session.

**FRs covered:** FR-1, FR-2, FR-8, FR-9, FR-13

### Epic 4: CRM-Ready Visit Reports

Key Account Managers receive strictly valid commercial visit reports that can be saved to the CRM even when an LLM initially returns malformed JSON.

**FRs covered:** FR-3, FR-15, FR-18, FR-19

### Epic 5: Inbound Prospect Qualification and Lead Handoff

Inbound prospects can complete a streamed diagnostic conversation and be handed off as actionable leads through the established CRM integration.

**FRs covered:** FR-5

## Epic 0: Existing POC Reconciliation and Delivery Baseline

The delivery team can evolve the existing Brainiac POC into the Onbora Core IA
without duplicating, silently discarding, or misrepresenting existing work.

### Story 0.1: Establish the Verified Brownfield Baseline

As a delivery team,
I want an auditable inventory of the existing POC and its relationship to the
MVP requirements,
So that implementation decisions start from verified facts.

**Acceptance Criteria:**

**Given** the repository at the approved baseline commit,
**When** the inventory is completed,
**Then** every tracked runtime module and dependency is classified as retain, adapt, replace, or retire with rationale.

**Given** a POC capability resembles an FR,
**When** it is assessed,
**Then** the inventory states the missing acceptance criteria and does not mark the FR done.

**Given** the baseline is accepted,
**When** any BMad workflow starts,
**Then** it can load `AGENTS.md` and `project-context.md` as repository context.

### Story 0.2: Establish a Repeatable Runtime and Test Baseline

As a developer,
I want to run and test the current POC reproducibly before migration,
So that later architecture changes have a known behavioral reference.

**Acceptance Criteria:**

**Given** documented non-secret environment variables,
**When** a developer follows the baseline instructions,
**Then** they can launch the CLI or Streamlit POC.

**Given** the report-generation path,
**When** unit tests run with a fake agent/model,
**Then** schema validation, transcript formatting, and serialization behavior are covered without a live LLM call.

**Given** the baseline checks run,
**When** an external dependency is unavailable,
**Then** the failure is explicit and no production-MVP claim is made.

## Epic 1: Integrable and Extensible AI Core

Client application teams can integrate a reliable Core IA API, while the product team can configure LLM providers and add specialized agents without modifying the API Gateway.

### Story 1.1: Runnable and Observable Core Service

As a client application developer,
I want a runnable Core IA service with documented health endpoints and validated configuration,
So that I can verify integration readiness and diagnose configuration failures before using AI features.

**Acceptance Criteria:**

**Given** a developer installs the project dependencies and supplies a valid `.env` configuration,
**When** they start the ASGI application,
**Then** the FastAPI service starts asynchronously and exposes OpenAPI documentation.

**Given** the service is running,
**When** a client calls `GET /health`,
**Then** it receives a structured successful health response.

**Given** required configuration is absent or invalid,
**When** the service starts,
**Then** startup fails with a clear validation error and no partially initialized service is exposed.

**Given** an unhandled domain or request error occurs,
**When** the API returns an error,
**Then** it uses the standard `{ error: { code, message, details } }` response shape.

### Story 1.2: Register Specialized Agents Through a Stable Contract

As a product engineer,
I want to define and register a specialized agent through one standard contract,
So that new capabilities can be added without changing API Gateway code.

**Acceptance Criteria:**

**Given** a developer implements an agent from the `BaseAgent` contract,
**When** the application initializes,
**Then** the agent is registered by a unique `agent_id` in `AgentRegistry`.

**Given** a registered agent is inspected,
**When** the registry exposes its metadata,
**Then** its system prompt, declared MCP tools, LLM role policy, input schema, and structured output schema are available.

**Given** an agent is registered with a duplicate ID or incomplete contract,
**When** the registry initializes,
**Then** initialization fails with a clear domain error and does not silently overwrite a valid registration.

**Given** a caller requests a registered agent by ID,
**When** the ID exists,
**Then** the registry returns the agent without importing API-layer dependencies.

### Story 1.3: Configure Per-Agent Multi-LLM Routing and Failover

As a product engineer,
I want to configure a primary and fallback LLM provider for each agent role,
So that each capability balances latency and quality while remaining available during provider failures.

**Acceptance Criteria:**

**Given** an agent role has a valid primary-provider configuration,
**When** the orchestrator requests an LLM for that role,
**Then** `LLMProviderFactory` returns the matching provider adapter through a common interface.

**Given** a role has a configured fallback provider,
**When** the primary provider reports an availability or quota failure,
**Then** the request is retried through the fallback provider and the failover is logged with the role and provider names.

**Given** both primary and fallback providers fail,
**When** the request completes,
**Then** the caller receives a typed, standardized service error without leaking credentials or provider internals.

**Given** a configured provider name is unsupported or its mandatory settings are missing,
**When** the service validates configuration,
**Then** startup fails with a clear validation error.

## Epic 2: Trusted Orange Knowledge and Company Intelligence

Sales representatives can prepare for a company and receive grounded Orange B2B recommendations based on hybrid catalog retrieval and durable company knowledge.

### Story 2.1: Ingest Orange B2B Knowledge Sources

As a knowledge-base administrator,
I want to ingest approved Orange B2B documents in JSON, Markdown, and PDF formats,
So that the Core IA can use a traceable, up-to-date product knowledge base.

**Acceptance Criteria:**

**Given** valid JSON, Markdown, or PDF files are placed in the configured catalog sources,
**When** the ingestion pipeline runs,
**Then** it extracts, normalizes, chunks, and stores each document with source metadata.

**Given** a source has already been ingested unchanged,
**When** ingestion runs again,
**Then** the pipeline does not create duplicate indexed content.

**Given** one source is unreadable or malformed,
**When** ingestion runs,
**Then** the failure identifies the source and does not prevent valid sources from being indexed.

**Given** ingestion finishes,
**When** an operator reviews the result,
**Then** it reports counts for processed, skipped, and failed sources.

### Story 2.2: Retrieve Grounded Orange Offers with Hybrid Search

As a specialized agent,
I want to retrieve Orange B2B knowledge using semantic and exact-keyword search,
So that recommendations are relevant while preserving exact offer names and product codes.

**Acceptance Criteria:**

**Given** the knowledge base contains indexed Orange sources,
**When** an agent submits a catalog query,
**Then** the retrieval engine runs dense semantic search and BM25 lexical search in parallel.

**Given** both retrieval modes return results,
**When** the engine prepares the response,
**Then** it merges and ranks them with Reciprocal Rank Fusion before returning the Top-K chunks.

**Given** matching chunks are found,
**When** an agent invokes retrieval,
**Then** it receives the ranked chunks with source metadata suitable for prompt-context injection.

**Given** no matching knowledge is found,
**When** retrieval completes,
**Then** it returns an explicit empty result without inventing an offer or product fact.

### Story 2.3: Expose Catalog Search Through MCP

As a specialized agent,
I want to query the Orange catalog through a standard MCP tool,
So that every agent uses the same governed knowledge-access path.

**Acceptance Criteria:**

**Given** the RAG retrieval engine is available,
**When** an MCP client lists the catalog server tools,
**Then** it finds `search_orange_catalog(query, category, limit)` with documented input and output schemas.

**Given** an authorized agent calls the tool with valid arguments,
**When** the search completes,
**Then** it receives ranked catalog results from the hybrid retrieval engine, limited to the requested maximum.

**Given** `category` or `limit` is omitted,
**When** the tool executes,
**Then** it applies documented defaults.

**Given** tool arguments are invalid or the retrieval engine is unavailable,
**When** the tool returns,
**Then** it emits a typed MCP error without exposing implementation details.

### Story 2.4: Preserve Durable Company and Contact Knowledge

As a sales representative,
I want company and contact facts from prior interactions to be retained safely,
So that future preparation and conversations start with the right business context.

**Acceptance Criteria:**

**Given** an agent has validated durable facts about a company or contact,
**When** it saves them through `EntityMemory`,
**Then** they are persisted asynchronously in SQLite for development and through a PostgreSQL-compatible adapter for production.

**Given** a company has prior stored facts,
**When** an agent requests its context,
**Then** it receives the company, contacts, installed solutions, decision makers, and relevant historical facts.

**Given** a fact is updated,
**When** it is saved,
**Then** the current value and its update timestamp are retained without creating duplicate entities.

**Given** entity storage is temporarily unavailable,
**When** a read or write is attempted,
**Then** the operation returns a typed domain error and does not corrupt existing data.

### Story 2.5: Prepare a Company Brief Through Web Reconnaissance

As a sales representative,
I want to request a concise company brief before a meeting,
So that I can anticipate relevant Orange B2B needs.

**Acceptance Criteria:**

**Given** the web-reconnaissance MCP server is configured,
**When** `company_researcher` requests public company information,
**Then** it obtains normalized sector, size, technologies, news, and local-presence signals through declared MCP tools.

**Given** a client submits a company name and/or website to `POST /api/v1/company/research`,
**When** research completes,
**Then** the API returns a Pydantic-validated company profile and brief in the standard response shape.

**Given** durable company facts already exist,
**When** the brief is prepared,
**Then** they are included and distinguished from newly researched public information.

**Given** no sufficiently reliable public result is available,
**When** research completes,
**Then** the response identifies unavailable fields rather than fabricating information.

## Epic 3: Real-Time Field Copilot

Sales representatives receive fast, relevant, non-intrusive advice cards during a meeting, and their feedback improves the active session.

### Story 3.1: Maintain and Compress the Active Meeting Context

As a sales representative,
I want the active meeting context to retain key facts and automatically compact long conversations,
So that the copilot remains useful throughout a meeting without losing validated information.

**Acceptance Criteria:**

**Given** a session is created with a UUIDv4 ID,
**When** transcript chunks, facts, and suggestion outcomes are added,
**Then** `WorkingMemory` makes the active context available to the assigned agent.

**Given** active context exceeds the configured compression threshold,
**When** compression is triggered,
**Then** an asynchronous summarization task replaces older conversational detail while preserving established facts and accepted/rejected suggestion cards.

**Given** compression completes,
**When** the active context is requested,
**Then** it remains below the configured prompt budget of 8,000 tokens.

**Given** Redis is unavailable in a local environment,
**When** a session is used,
**Then** the system uses the documented in-memory fallback without changing the memory contract.

### Story 3.2: Generate Confidence-Gated Advice Cards

As a sales representative,
I want the copilot to identify a customer need or major objection and produce a structured advice card only when it is sufficiently reliable,
So that I receive actionable recommendations without distracting noise.

**Acceptance Criteria:**

**Given** a transcript chunk and its active session context are available,
**When** `realtime_copilot` detects an Orange B2B need or a major objection,
**Then** it can use the catalog-search tool to ground its recommendation.

**Given** a recommendation is eligible for delivery,
**When** the agent creates a `SuggestionCard`,
**Then** the card includes `card_id`, `need_detected`, `suggested_offer`, `pitch_argument`, and `confidence_score`, all validated by Pydantic.

**Given** the confidence score is below the configured threshold and no major objection is identified,
**When** the agent evaluates the chunk,
**Then** it records no deliverable advice card.

**Given** a major objection is identified,
**When** the confidence threshold would otherwise block a card,
**Then** the copilot may emit an objection-oriented card according to the configured policy.

### Story 3.3: Stream Copilot Guidance During a Meeting

As a sales representative,
I want to send transcript chunks to the copilot and receive guidance as SSE events,
So that I can act on relevant Orange offers during the conversation.

**Acceptance Criteria:**

**Given** a valid text chunk and session ID are sent to `POST /api/v1/copilot/stream`,
**When** the copilot begins processing,
**Then** the endpoint returns a non-blocking SSE stream using the standard `status`, `suggestion_card`, `error`, and `done` event types.

**Given** the copilot produces an eligible `SuggestionCard`,
**When** streaming is active,
**Then** it emits a Pydantic-validated `suggestion_card` event containing the complete card.

**Given** a chunk contains a detectable buying intent under normal provider conditions,
**When** the request is received,
**Then** the suggestion-card event is emitted within 1,500 ms end-to-end.

**Given** processing fails after the stream starts,
**When** the failure is handled,
**Then** the stream emits a standardized `error` event followed by `done` without blocking other requests.

### Story 3.4: Capture Commercial Feedback on Advice Cards

As a sales representative,
I want to accept or reject a copilot advice card with an optional reason,
So that the active meeting context reflects what was useful.

**Acceptance Criteria:**

**Given** a card exists in the active session,
**When** the client sends `{ suggestion_id, status, reason? }` to `POST /api/v1/copilot/feedback`,
**Then** the API validates the payload and records the accepted or rejected outcome in `WorkingMemory`.

**Given** feedback is accepted,
**When** later copilot processing uses the session context,
**Then** it can access the card outcome and optional reason.

**Given** `status` is not `accepted` or `rejected`,
**When** the endpoint receives the request,
**Then** it returns a validation error in the standard API error shape.

**Given** the referenced card or session does not exist,
**When** feedback is submitted,
**Then** the endpoint returns a typed not-found error and does not create feedback state.

## Epic 4: CRM-Ready Visit Reports

Key Account Managers receive strictly valid commercial visit reports that can be saved to the CRM even when an LLM initially returns malformed JSON.

### Story 4.1: Define the Strict Commercial Visit Report Contract

As a Key Account Manager,
I want every visit report to use one strict, documented data contract,
So that it can be consumed by the CRM without manual cleanup.

**Acceptance Criteria:**

**Given** a `ConversationReport` is created,
**When** it is validated,
**Then** it requires `summary`, `key_points`, `customer_needs`, `pain_points`, `objections`, `recommended_next_actions`, `interest_level`, `lead_status`, `qualification_score`, and `missing_information`.

**Given** `interest_level`, `lead_status`, or `qualification_score` contains an invalid value,
**When** validation runs,
**Then** it fails with field-level validation details.

**Given** a valid report is serialized,
**When** an API client or MCP tool consumes it,
**Then** it receives a JSON-compatible Pydantic v2 payload and its schema is exposed through OpenAPI.

**Given** report fields are unavailable from a conversation,
**When** a report is assembled,
**Then** they are represented using the contract’s explicit missing-information mechanism rather than omitted silently.

### Story 4.2: Generate a Structured Visit Report

As a Key Account Manager,
I want a commercial transcript or completed session to produce a structured visit report,
So that I can act on customer needs and next steps without re-reading the full conversation.

**Acceptance Criteria:**

**Given** a transcript or existing `session_id` is provided to `POST /api/v1/reports/generate`,
**When** `conversation_reporter` completes successfully,
**Then** the endpoint returns a `ConversationReport` validated against the strict contract.

**Given** the request uses a `session_id`,
**When** the report is generated,
**Then** the reporter uses the active and compressed session context, including accepted/rejected advice-card outcomes.

**Given** both a transcript and session ID are missing or invalid,
**When** the endpoint is called,
**Then** it returns a standard validation or not-found error.

**Given** the report provider is configured for the reporter role,
**When** generation runs,
**Then** it is invoked through the per-agent LLM routing established in epic 1.

### Story 4.3: Correct Malformed Report Output Before Failing

As a Key Account Manager,
I want the Core IA to recover from a malformed LLM report response when possible,
So that a usable report is not lost because of a formatting error.

**Acceptance Criteria:**

**Given** the reporter’s first LLM response cannot be parsed or fails `ConversationReport` validation,
**When** report generation handles the failure,
**Then** it invokes one bounded correction pass with the validation errors as repair context.

**Given** the correction pass produces valid output,
**When** validation completes,
**Then** the endpoint returns the corrected `ConversationReport`.

**Given** the correction pass still produces invalid output,
**When** the request completes,
**Then** the endpoint returns a typed standard error and logs the validation failure without logging sensitive transcript content.

**Given** a report is valid on the first attempt,
**When** generation completes,
**Then** no correction pass is invoked.

### Story 4.4: Synchronize Reports and Leads Through the CRM MCP Server

As a Key Account Manager,
I want the Core IA to use a standardized CRM connector for reports, leads, notes, and client history,
So that commercial information reaches Django without bespoke integrations per agent.

**Acceptance Criteria:**

**Given** the CRM/Django MCP server is configured,
**When** an authorized agent lists its tools,
**Then** it finds documented tools for `get_client_history`, `create_lead`, `update_client_note`, and `save_conversation_report`.

**Given** a valid `ConversationReport` is ready,
**When** the reporter calls `save_conversation_report`,
**Then** the CRM server receives the validated payload and returns a traceable success result.

**Given** an agent requests client history, creates a lead, or updates a note with valid input,
**When** the relevant CRM MCP tool is called,
**Then** the server forwards the request through its Django adapter and returns a typed result.

**Given** Django is unavailable or returns a failure,
**When** an MCP CRM tool is called,
**Then** it returns a typed, retry-safe MCP error without exposing CRM credentials or internal responses.

## Epic 5: Inbound Prospect Qualification and Lead Handoff

Inbound prospects can complete a streamed diagnostic conversation and be handed off as actionable leads through the established CRM integration.

### Story 5.1: Qualify an Inbound Prospect with Grounded Guidance

As an inbound business prospect,
I want a virtual advisor to understand my connectivity and mobility needs through a guided conversation,
So that I receive relevant Orange B2B options without technical jargon.

**Acceptance Criteria:**

**Given** a prospect starts a new inbound conversation,
**When** `lead_qualifier` processes their messages,
**Then** it maintains the conversation context and asks only relevant follow-up questions about needs, constraints, scale, and budget.

**Given** the prospect describes a need that matches catalog knowledge,
**When** the agent responds,
**Then** it grounds its offer guidance in hybrid-retrieval results and does not invent Orange offer details.

**Given** sufficient qualification information has been collected,
**When** the agent evaluates the conversation,
**Then** it produces a Pydantic-validated qualification result with customer needs, missing information, recommended next actions, interest level, lead status, and a 0–100 qualification score.

**Given** information is incomplete,
**When** the agent cannot qualify the prospect confidently,
**Then** it identifies the missing information instead of marking the lead as qualified.

### Story 5.2: Stream Inbound Responses and Hand Off Qualified Leads

As an inbound business prospect,
I want responses to appear as they are generated and my qualified request to reach the sales team,
So that I get a smooth conversation and timely follow-up.

**Acceptance Criteria:**

**Given** a valid chat message and conversation ID are sent to `POST /api/v1/chat/message`,
**When** `lead_qualifier` generates a response,
**Then** the endpoint returns non-blocking SSE `token`, `error`, and `done` events.

**Given** the qualification result reaches the configured handoff threshold,
**When** the conversation turn completes,
**Then** the system calls the CRM MCP `create_lead` tool with a validated lead payload and returns a handoff status.

**Given** the lead does not meet the handoff threshold,
**When** the turn completes,
**Then** the response continues the qualification flow without creating a CRM lead.

**Given** the CRM handoff fails,
**When** the SSE response completes,
**Then** the prospect still receives the advisor response and the system reports the handoff failure through the standard error contract for follow-up.
