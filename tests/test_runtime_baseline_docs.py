from pathlib import Path


def test_baseline_docs_describe_unavailable_dependency_remediation() -> None:
    readme = " ".join(Path("README.md").read_text(encoding="utf-8").split())

    assert "If a package is absent" in readme
    assert "If Gemini is unavailable after configuration" in readme
    assert "do not represent it as an MVP result" in readme


def test_baseline_docs_cover_the_locked_setup_and_poc_boundaries() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "Use Python 3.12" in readme
    assert "pip install -r requirements-dev.txt" in readme
    assert "python -m src.main" in readme
    assert "streamlit run streamlit_app.py" in readme
    assert "GEMINI_REPORTER_MODEL" in readme
    assert "DJANGO_REPORT_URL" in readme
    assert "do not import `streamlit_app.py`" in readme
