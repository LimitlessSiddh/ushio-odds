from pathlib import Path


def test_api_image_includes_migration_inputs() -> None:
    root = Path(__file__).resolve().parents[1]
    dockerfile = (root / "Dockerfile").read_text()
    assert "COPY alembic.ini ." in dockerfile
    assert "COPY alembic ./alembic" in dockerfile
    assert "COPY tests ./tests" in dockerfile
    assert (root / "alembic.ini").is_file()
    assert (root / "alembic" / "versions" / "20261027_03_quote_lifecycle.py").is_file()
    assert (root / "alembic" / "versions" / "20261028_05_capability_evidence_and_ledger_provenance.py").is_file()
