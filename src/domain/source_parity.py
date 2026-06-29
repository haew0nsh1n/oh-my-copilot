"""Source parity model for comparing OMC source families with OMP surfaces."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class SourceParityStatus(Enum):
    """Implementation status for a reference source family."""

    IMPLEMENTED = "implemented"
    ADAPTED = "adapted"
    PARTIAL = "partial"
    GAP = "gap"


@dataclass(frozen=True)
class SourceParityItem:
    """Parity mapping for one OMC src top-level family."""

    family: str
    reference_file_count: int
    status: SourceParityStatus
    omp_surfaces: tuple[str, ...]
    notes: str

    @property
    def needs_work(self) -> bool:
        """Return whether this family still has parity work remaining."""
        return self.status in {SourceParityStatus.PARTIAL, SourceParityStatus.GAP}


@dataclass(frozen=True)
class SourceParityReport:
    """Source parity audit report."""

    reference: str
    items: tuple[SourceParityItem, ...]
    observed_reference_counts: dict[str, int]

    @property
    def total_reference_files(self) -> int:
        """Total OMC runtime source files represented by the matrix."""
        return sum(item.reference_file_count for item in self.items)

    @property
    def family_names(self) -> tuple[str, ...]:
        """Reference source family names covered by the matrix."""
        return tuple(item.family for item in self.items)

    @property
    def gap_items(self) -> tuple[SourceParityItem, ...]:
        """Families that are missing or only partially translated."""
        return tuple(item for item in self.items if item.needs_work)

    @property
    def unknown_reference_families(self) -> tuple[str, ...]:
        """Observed OMC source families not represented by the matrix."""
        represented = set(self.family_names)
        return tuple(sorted(set(self.observed_reference_counts) - represented))

    @property
    def changed_reference_counts(self) -> dict[str, tuple[int, int]]:
        """Return expected/observed count mismatches for known families."""
        mismatches: dict[str, tuple[int, int]] = {}
        for item in self.items:
            observed = self.observed_reference_counts.get(item.family)
            if observed is not None and observed != item.reference_file_count:
                mismatches[item.family] = (item.reference_file_count, observed)
        return mismatches


def count_reference_source_families(reference_src: Path) -> dict[str, int]:
    """Count runtime files by OMC src top-level family, excluding tests and caches."""
    counts: dict[str, int] = {}
    for path in reference_src.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(reference_src)
        if "__tests__" in relative.parts or "node_modules" in relative.parts:
            continue
        family = relative.parts[0]
        counts[family] = counts.get(family, 0) + 1
    return counts