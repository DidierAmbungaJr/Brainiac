from pathlib import Path


def test_service_docs_describe_installation_and_poc_boundaries() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    requirements = Path("requirements.txt").read_text(encoding="utf-8")
    lock = Path("requirements.lock").read_text(encoding="utf-8")

    assert "Python 3.11 or later" in readme
    assert "pip install -r requirements-dev.txt" in readme
    assert "uvicorn src.main:app --reload" in readme
    assert "SERVICE_NAME" in readme
    assert "ENVIRONMENT" in readme
    assert "/health" in readme
    assert "OpenAPI" in readme
    assert "does not import `streamlit_app.py`" in readme
    assert "fastapi==0.141.1" in requirements
    assert "fastapi==0.141.1" in lock
    assert "-r requirements.lock" in Path("requirements-dev.txt").read_text(encoding="utf-8")
    assert "fully pinned `requirements.lock`" in readme
