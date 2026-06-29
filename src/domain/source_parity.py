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

    @property
    def omp_source_paths(self) -> tuple[str, ...]:
        """Return OMP source paths that implement or adapt this OMC family."""
        return tuple(surface for surface in self.omp_surfaces if surface.startswith("src/"))


@dataclass(frozen=True)
class SourceParityReport:
    """Source parity audit report."""

    reference: str
    items: tuple[SourceParityItem, ...]
    observed_reference_counts: dict[str, int]
    workspace_root: Path

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

    @property
    def current_source_entries(self) -> tuple[str, ...]:
        """Current top-level entries under OMP src/."""
        src_root = self.workspace_root / "src"
        if not src_root.exists():
            return ()
        return tuple(sorted(path.name for path in src_root.iterdir() if path.is_dir() or path.is_file()))

    @property
    def missing_omp_source_paths(self) -> dict[str, tuple[str, ...]]:
        """Mapped OMP source paths that do not exist in the current workspace."""
        missing: dict[str, tuple[str, ...]] = {}
        for item in self.items:
            missing_paths = tuple(
                source_path
                for source_path in item.omp_source_paths
                if not (self.workspace_root / source_path.rstrip("/")).exists()
            )
            if missing_paths:
                missing[item.family] = missing_paths
        return missing

    @property
    def families_without_omp_source_paths(self) -> tuple[str, ...]:
        """Reference families without any mapped OMP src implementation path."""
        return tuple(sorted(item.family for item in self.items if not item.omp_source_paths))


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