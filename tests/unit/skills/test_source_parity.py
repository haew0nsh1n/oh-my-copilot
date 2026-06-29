"""Tests for OMC source parity audits."""

from pathlib import Path

from domain import SourceParityStatus
from skills import SourceParitySkill


def test_source_parity_matrix_covers_omc_runtime_source_families():
    """OMP records an explicit parity status for every OMC runtime src family."""
    report = SourceParitySkill().audit()

    assert report.total_reference_files == 523
    assert len(report.items) == 29
    assert "agents" in report.family_names
    assert "hooks" in report.family_names
    assert "mcp" in report.family_names
    assert "team" in report.family_names

    statuses = {item.family: item.status for item in report.items}
    assert statuses["ultragoal"] is SourceParityStatus.IMPLEMENTED
    assert statuses["hooks"] is SourceParityStatus.PARTIAL
    assert statuses["mcp"] is SourceParityStatus.GAP


def test_source_parity_can_compare_observed_reference_src_counts(tmp_path):
    """A local OMC src checkout can be checked for unknown or changed families."""
    reference_src = tmp_path / "src"
    (reference_src / "agents").mkdir(parents=True)
    (reference_src / "agents" / "index.ts").write_text("", encoding="utf-8")
    (reference_src / "new-runtime").mkdir()
    (reference_src / "new-runtime" / "index.ts").write_text("", encoding="utf-8")
    (reference_src / "__tests__").mkdir()
    (reference_src / "__tests__" / "agents.test.ts").write_text("", encoding="utf-8")

    report = SourceParitySkill().audit(reference_src)

    assert report.observed_reference_counts == {"agents": 1, "new-runtime": 1}
    assert report.unknown_reference_families == ("new-runtime",)
    assert report.changed_reference_counts["agents"] == (22, 1)