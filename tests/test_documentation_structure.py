"""Guard the documentation boundary and canonical source layout."""

from pathlib import Path

ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs"


def test_documentation_has_one_canonical_audience_map() -> None:
    required = {
        "index.md",
        "status.md",
        "getting-started/installation.md",
        "getting-started/examples.md",
        "concepts/algorithms.md",
        "concepts/correctness.md",
        "concepts/limitations.md",
        "guides/benchmarking.md",
        "reference/index.md",
        "research/provenance.md",
        "project/testing.md",
        "archive/architecture-review.md",
    }
    missing = sorted(path for path in required if not (DOCS / path).is_file())
    assert not missing, f"missing canonical documentation files: {missing}"


def test_historical_documents_are_not_in_the_active_root() -> None:
    assert not (DOCS / "HISTORICAL_ARCHITECTURE_REVIEW.md").exists()
    assert not (DOCS / "START_HERE.md").exists()
    assert not (DOCS / "GLOSSARY.md").exists()
    assert not (DOCS / "PAPER.md").exists()
