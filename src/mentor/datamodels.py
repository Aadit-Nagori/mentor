from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path


class ChangeType(StrEnum):
    ADDED = auto()
    MODIFIED = auto()
    DELETED = auto()
    RENAMED = auto()

class LineKind(StrEnum):
    ADDED = auto()
    REMOVED = auto()
    CONTEXT = auto()

class FilteredReason(StrEnum):
    LOCKFILE = auto()
    GENERATED = auto()
    VENDORED = auto()
    BINARY = auto()
    TOO_LARGE = auto()
    OVER_BUDGET = auto()

@dataclass(frozen=True)
class Exclusion:
    reason: FilteredReason
    detail: str | None

@dataclass(frozen=True)
class Line:
    content: str
    kind: LineKind
    old_line_no : int | None
    new_line_no : int | None

@dataclass(frozen=True)
class Hunk:
    old_start: int
    old_length: int
    new_start: int
    new_length: int
    section_heading: str | None
    lines: tuple[Line, ...]

@dataclass(frozen=True)
class ChangedFile:
    old_path: Path | None
    new_path: Path | None
    change_type: ChangeType
    is_binary: bool
    exclusion: Exclusion | None
    hunks: tuple[Hunk, ...]

@dataclass(frozen=True)
class Diff:
    base_sha: str
    head_sha: str
    files: list[ChangedFile]

    @property
    def reviewable(self) -> list[ChangedFile]:
        return [f for f in self.files if f.exclusion is None]
