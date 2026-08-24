# Onbora Core IA

Onbora Core IA now provides an asynchronous FastAPI service foundation. The
legacy synchronous Strands/Gemini CLI and Streamlit prototype remain migration
input only; the Core IA service does not import `streamlit_app.py` or POC agents.

## Requirements and installation

Use Python 3.11 or later. The legacy POC baseline was verified with Python 3.12
on Windows, macOS, or Linux.

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

`requirements-dev.txt` installs the fully pinned `requirements.lock`; the
direct runtime constraints remain recorded in `requirements.txt`.

`SERVICE_NAME` and `ENVIRONMENT` are required non-secret settings. `ENVIRONMENT`
must be one of `development`, `test`, or `production`. The service validates
them during ASGI startup and will not accept traffic if they are absent or
unsupported.

## Run the service

```powershell
.\.venv\Scripts\uvicorn src.main:app --reload
```

After startup, use [GET /health](http://127.0.0.1:8000/health) for the typed
service readiness response. FastAPI also generates OpenAPI documentation at
http://127.0.0.1:8000/docs and the OpenAPI schema at
http://127.0.0.1:8000/openapi.json.

All API errors use this envelope:

```json
{"error":{"code":"...","message":"...","details":{}}}
```

## Tests

```powershell
.\.venv\Scripts\python -m pytest
```

The test suite uses in-process clients and does not open network connections.
If a package is absent, rerun the pinned installation command. If Gemini is
unavailable after configuration, that affects only the retained legacy POC;
do not represent it as an MVP result.

The FastAPI service replaces the old CLI entry-point role. The former Gemini
settings, including `GEMINI_REPORTER_MODEL` and `DJANGO_REPORT_URL`, are POC
migration details and no longer configure the service. Use the approved POC
baseline if you need to reproduce those retired operator flows.
