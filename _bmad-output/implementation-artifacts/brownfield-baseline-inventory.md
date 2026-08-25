# Verified Brownfield Baseline Inventory

## Decision Record

- **Approved evidence revision:** `7c8434106bbd09fadbd410fd22b700f85693ca48`.
- **Evidence method:** `git ls-tree` and `git show` at that exact commit. The current worktree, including `AGENTS.md` and `project-context.md`, is not evidence for what existed at the baseline.
- **Decision vocabulary:** `retain`, `adapt`, `replace`, and `retire` only.
- **Decision status:** the classifications are recorded and provisional until human approval; the evidence revision itself is approved.
- **MVP delivery status:** no functional requirement is delivered by this POC. These are migration decisions, not implementation claims.

This record covers all 24 paths returned by `git ls-tree -r --name-only 7c8434106bbd09fadbd410fd22b700f85693ca48`: the 12 runtime/configuration paths and the 12 explicitly excluded non-runtime paths. The six runtime dependencies in `requirements.txt` are classified individually. `AGENTS.md` and `project-context.md` are current delivery artifacts for this story; the approved revision predates them.

## Scope and Reproduction

Run these commands from the repository root to reproduce the evidence without launching the POC:

```powershell
$evidenceCommit = '7c8434106bbd09fadbd410fd22b700f85693ca48'
git cat-file -e '7c8434106bbd09fadbd410fd22b700f85693ca48^{commit}'
$expectedRuntimePaths = @(
  '.env.example', 'requirements.txt', 'src/__init__.py', 'src/agent.py',
  'src/config.py', 'src/conversation_report.py', 'src/main.py',
  'src/multi_agent.py', 'src/response.py', 'src/tools/__init__.py',
  'src/tools/custom_tools.py', 'streamlit_app.py'
)
$actualRuntimePaths = git ls-tree -r --name-only $evidenceCommit |
  Where-Object { $_ -match '^(\.env\.example|requirements\.txt|src/.*\.py|streamlit_app\.py)$' }
if (@(Compare-Object $expectedRuntimePaths $actualRuntimePaths)) {
  throw 'The approved runtime manifest differs from the inventory scope.'
}
$expectedRuntimePaths | ForEach-Object { git show "${evidenceCommit}:$_" | Out-Null }
```

The manifest comparison and `git show` loop deterministically validate all 12 runtime/configuration paths. Runtime launch and test-baseline instructions are intentionally out of scope for Story 0.1; they belong to Story 0.2.

## Baseline Evidence Anchors

Every anchor below is `SHA:path:line-range` at the approved evidence revision. It supports the corresponding rationale in the classification tables rather than describing the current worktree.

| Classification item | Precise baseline evidence |
| --- | --- |
| `.env.example` | `7c8434106bbd09fadbd410fd22b700f85693ca48:.env.example:1-10` |
| `requirements.txt` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:1-6` |
| `src/__init__.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/__init__.py:1` |
| `src/agent.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/agent.py:3-8`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/agent.py:17-34` |
| `src/config.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/config.py:3-30` |
| `src/conversation_report.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/conversation_report.py:13-26`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/conversation_report.py:39-51`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/conversation_report.py:54-62`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/conversation_report.py:65-88` |
| `src/main.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/main.py:3-5`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/main.py:8-41` |
| `src/multi_agent.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/multi_agent.py:3-9`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/multi_agent.py:32-45`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/multi_agent.py:48-83` |
| `src/response.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/response.py:14-30`; `7c8434106bbd09fadbd410fd22b700f85693ca48:src/response.py:72-109` |
| `src/tools/__init__.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/tools/__init__.py:1-3` |
| `src/tools/custom_tools.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:src/tools/custom_tools.py:7-24` |
| `streamlit_app.py` | `7c8434106bbd09fadbd410fd22b700f85693ca48:streamlit_app.py:17-27`; `7c8434106bbd09fadbd410fd22b700f85693ca48:streamlit_app.py:121-127` |
| `strands-agents[gemini]>=1.0.0` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:1` |
| `strands-agents-tools>=0.8.6` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:2` |
| `python-dotenv>=1.0.0` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:3` |
| `pydantic>=2.0.0` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:4` |
| `streamlit>=1.40.0` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:5` |
| `requests>=2.31.0` | `7c8434106bbd09fadbd410fd22b700f85693ca48:requirements.txt:6` |

## Runtime Classification

| Artifact | Kind | Decision | Evidence-based rationale |
| --- | --- | --- | --- |
| `.env.example` | Runtime configuration | adapt | It documents non-secret model, session, mode, and Django URL variables, but target configuration must use validated Pydantic Settings and provider-neutral policies rather than direct Gemini environment settings. |
| `requirements.txt` | Runtime dependency manifest | replace | It is an unpinned synchronous POC manifest. The target requires a separately selected, pinned async FastAPI/MCP dependency set. |
| `src/__init__.py` | Python package module | retain | Its one-line docstring identifies a Gemini/Strands-built agent, so that wording is POC-specific; the otherwise behavior-free package module can remain only as a package boundary after its description is updated during migration. |
| `src/agent.py` | Single-agent construction module | replace | It builds a synchronous Strands agent with a file session manager and direct in-process tools. The target must expose behavior through async ports and a governed agent contract. |
| `src/config.py` | Model configuration module | replace | `create_model` loads dotenv values and constructs a Gemini-specific `GeminiModel` directly, with synchronous provider coupling and no validated configuration, provider abstraction, or failover. |
| `src/conversation_report.py` | Report schema and formatting module | adapt | `ConversationReport`, transcript formatting, JSON, and Markdown rendering are useful source material, but validation is not the strict API/OpenAPI contract and generation directly calls a synchronous provider without repair handling. |
| `src/main.py` | CLI entry point and module | retire | The blocking terminal loop is a POC operator interface, not a target Core IA API entry point. |
| `src/multi_agent.py` | Multi-agent orchestration module | replace | It names supervisor, researcher, and reporter roles, but composes synchronous Strands agents directly and exposes them as tools; it has no `BaseAgent` registry contract, declared schemas, MCP tool ports, or provider failover. |
| `src/response.py` | Response normalization module | adapt | Its response-content extraction and callback collector may inform adapter-level normalization, but `invoke_agent` synchronously invokes a concrete agent and cannot enter the async target core unchanged. |
| `src/tools/__init__.py` | POC tools package module | retire | It only re-exports the POC's in-process demo tools; governed target tools must be supplied through MCP ports. |
| `src/tools/custom_tools.py` | POC tool module | retire | `current_time`, `calculate_age`, and `get_user_profile` are local demo implementations, not declared MCP CRM, catalogue, or web-reconnaissance integrations. |
| `streamlit_app.py` | Streamlit operator UI entry point | retire | It couples UI state, blocking report generation, and a direct `requests.post` Django call to the POC. Streamlit must not enter the target Core IA domain core. |

## Runtime Dependency Classification

| Baseline dependency | Decision | Evidence-based rationale |
| --- | --- | --- |
| `strands-agents[gemini]>=1.0.0` | replace | The baseline agent runtime is tied directly to Gemini and synchronous Strands construction; target role routing needs provider adapters and failover behind a common async interface. |
| `strands-agents-tools>=0.8.6` | retire | No target requirement permits the baseline's in-process tool mechanism; external capabilities must be governed MCP tools. |
| `python-dotenv>=1.0.0` | replace | Direct dotenv loading is superseded by validated target settings and startup validation. |
| `pydantic>=2.0.0` | adapt | Pydantic v2 is required by the target, but baseline models need strict fields, enums/constraints, API schemas, and tested validation behavior. |
| `streamlit>=1.40.0` | retire | Streamlit is a POC UI dependency and is outside the FastAPI/MCP Core IA runtime. |
| `requests>=2.31.0` | replace | The only baseline use is the blocking, UI-owned Django POST; target integrations must use an async, typed MCP CRM adapter. |

## Explicit Non-Runtime Exclusions

The following baseline paths were returned by `git ls-tree` but are not runtime modules, entry points, configuration artifacts, or dependencies. They are excluded explicitly rather than silently omitted: `.bash_profile`, `.bashrc`, `.gitconfig`, `.gitignore`, `.gitmodules`, `.idea`, `.mcp.json`, `.profile`, `.ripgreprc`, `.vscode`, `.zprofile`, and `.zshrc`. At the approved revision, all except `.gitignore` are empty placeholders; `.gitignore` is version-control metadata. None is imported, read, or executed by the tracked POC runtime.

## POC-to-MVP Gap Assessment

No entry in this section is evidence of a delivered requirement. A source-level resemblance records only migration context and its unmet acceptance gaps.

| POC evidence | Resembles | Unmet MVP acceptance gaps | Delivery status |
| --- | --- | --- | --- |
| `ConversationReport`, `format_transcript`, and `generate_conversation_report` | FR-3 and Epic 4 report generation | No asynchronous `POST /api/v1/reports/generate`; no transcript-or-session-ID API contract; no active/compressed session context; no standard API errors; and no provider routing through Epic 1. | Undelivered. |
| The baseline `ConversationReport` Pydantic model | FR-18 strict report contract | `interest_level` and `lead_status` are free strings rather than constrained values; fields are not exposed through OpenAPI; `generate_conversation_report` accepts any `BaseModel` structured output rather than guaranteeing `ConversationReport`; and there is no target API/MCP serialization boundary or explicit missing-information enforcement. | Undelivered. |
| Report-agent structured output raises immediately when absent or invalid | FR-19 malformed-report correction | No bounded correction pass, no validation-error repair context, and no typed/redacted failure path after correction fails. | Undelivered. |
| `create_model(role=...)` selects role-specific Gemini environment variables | FR-6 per-agent LLM routing | Only one Gemini provider is directly constructed; there is no common provider interface, primary/fallback policy, startup validation, retry, or failover logging. | Undelivered. |
| Supervisor, researcher, and reporter are composed with `Agent.as_tool` | FR-7 extensible sub-agent registration | No standard `BaseAgent`, unique registry, declared input/output schemas, declared MCP tools, role policy metadata, or duplicate/incomplete-contract error. | Undelivered. |
| Researcher prompt and local `TOOLS` delegation | FR-4 and Epic 2 company intelligence | No company-research endpoint, normalized company profile, declared public web-recon MCP tools, durable facts, or reliable-unavailable-field behavior. | Undelivered. |
| No baseline code beyond a generic research prompt and demo tools | Epic 2 knowledge, catalogue, and memory capabilities | No PDF/Markdown/JSON ingestion, deduplication, dense-plus-BM25 retrieval, reciprocal-rank fusion, Top-K source context, `search_orange_catalog` MCP tool, asynchronous durable entity storage, or governed web reconnaissance. | Undelivered. |
| CLI and Streamlit conversational interaction with file sessions | Epic 3 real-time copilot | No UUIDv4 working-memory contract, asynchronous compression below the prompt budget, confidence/objection policy, validated `SuggestionCard`, SSE stream, 1,500 ms latency behavior, feedback endpoint, or typed feedback/not-found errors. | Undelivered. |
| Streamlit chat UI and supervisor conversation | Epic 5 inbound qualification and handoff | No streamed `/api/v1/chat/message` endpoint, grounded qualification flow, Pydantic qualification result, threshold decision, or CRM MCP `create_lead` handoff/error behavior. | Undelivered. |
| `streamlit_app.py` sends a validated report with `requests.post` when approved | FR-15 MCP CRM/Django integration | No MCP server or tools for client history, lead creation, notes, or report saving; no Django adapter, traceable result, typed retry-safe error, or credential-safe boundary. | Undelivered. |
| Local demo tools and generic researcher role | FR-16 MCP web reconnaissance | No web-reconnaissance MCP server, declared public-company research tool, normalized sector/size/technology/news/local-presence signals, or unavailable-field behavior. | Undelivered. |

## Audit Checks

The following checks validate the durable record after edits:

```powershell
rg -n '7c8434106bbd09fadbd410fd22b700f85693ca48|## Runtime Classification|## POC-to-MVP Gap Assessment' _bmad-output/implementation-artifacts/brownfield-baseline-inventory.md
rg -n 'brownfield-baseline-inventory' AGENTS.md project-context.md
git diff --check
```

Run this mechanical revalidation after the scope-and-reproduction commands:

```powershell
$inventoryPath = '_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md'
$inventoryLines = Get-Content $inventoryPath
$allowedDecisions = @('retain', 'adapt', 'replace', 'retire')
foreach ($runtimePath in $expectedRuntimePaths) {
  $pattern = '^\| `' + [regex]::Escape($runtimePath) + '` \| [^|]+ \| (?<decision>[^|]+) \|'
  $rows = @($inventoryLines | Where-Object { $_ -match $pattern })
  if ($rows.Count -ne 1) {
    throw "Expected exactly one allowed classification for $runtimePath."
  }
  $null = $rows[0] -match $pattern
  if ($Matches['decision'].Trim() -notin $allowedDecisions) {
    throw "Expected exactly one allowed classification for $runtimePath."
  }
}
$baselineDependencies = git show "${evidenceCommit}:requirements.txt" |
  Where-Object { $_ -and -not $_.StartsWith('#') }
if ($baselineDependencies.Count -ne 6) { throw 'Expected six baseline dependencies.' }
foreach ($dependency in $baselineDependencies) {
  $pattern = '^\| `' + [regex]::Escape($dependency) + '` \| (?<decision>retain|adapt|replace|retire) \|'
  $rows = @($inventoryLines | Where-Object { $_ -match $pattern })
  if ($rows.Count -ne 1) {
    throw "Expected exactly one allowed classification for $dependency."
  }
  $null = $rows[0] -match $pattern
  if ($Matches['decision'].Trim() -notin $allowedDecisions) {
    throw "Expected exactly one allowed classification for $dependency."
  }
}
$markdownArtifacts = @(
  '_bmad-output/implementation-artifacts/brownfield-baseline-inventory.md',
  '_bmad-output/implementation-artifacts/spec-0-1-establish-verified-brownfield-baseline.md'
)
foreach ($artifact in $markdownArtifacts) {
  if ([IO.File]::ReadAllText((Resolve-Path $artifact)) -match '(?m)[ \t]+(?=\r?$)') {
    throw "Trailing whitespace found in $artifact."
  }
}
```

Expected result: the inventory names the exact approved revision; both durable repository-context files point to this single provisional decision record; all 12 manifest paths, their 12 allowed classification rows, and six dependency classifications validate mechanically; and Git plus non-Git checks find no whitespace errors.
