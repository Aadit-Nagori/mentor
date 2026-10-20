from pathlib import Path

from git import Repo
from unidiff.patch import Line as UnidiffLine
from unidiff.patch import PatchedFile, PatchSet

from .datamodels import ChangedFile, ChangeType, Diff, Hunk, Line, LineKind


def _change_type(pf: PatchedFile) -> ChangeType:
    if pf.is_rename:
        return ChangeType.RENAMED
    elif pf.is_added_file:
        return ChangeType.ADDED
    elif pf.is_removed_file:
        return ChangeType.DELETED
    elif pf.is_modified_file:
        return ChangeType.MODIFIED
    else:
        raise ValueError(f"Unidentified File Type with info {pf.patch_info}")

def _line_kind(line: UnidiffLine) -> LineKind:
    if line.is_added:
        return LineKind.ADDED
    elif line.is_removed:
        return LineKind.REMOVED
    elif line.is_context:
        return LineKind.CONTEXT
    else:
        raise ValueError(f"Unidentified Line type {line.line_type}")


def extract(repo_path: Path, base_ref: str, head_ref: str) -> Diff:
    repo = Repo(repo_path)
    base = repo.commit(base_ref)
    head = repo.commit(head_ref)
    merge_bases = repo.merge_base(base,head)

    if len(merge_bases) == 0:
        raise ValueError(f"Unrelated Histories between {base_ref} and {head_ref}")
    elif len(merge_bases) > 1:
        raise NotImplementedError("Criss Cross Merge Not Currently Supported")

    merge_base = merge_bases[0]

    #may need to add extra context passing with -U tag
    # pin options so the user's git config can't change the output format
    diff_text = repo.git.diff(
        merge_base, head,
        "-M", "--no-color", "--no-ext-diff",
        "--src-prefix=a/", "--dst-prefix=b/",
        strip_newline_in_stdout=False,
    )

    patch = PatchSet.from_string(diff_text)

    files = []
    for file in patch:
        hunks = []
        for hunk in file:
            lines = []
            for line in hunk:
                if line.line_type == "\\":
                    continue
                lines.append(Line(
                    content=line.value,
                    kind=_line_kind(line),
                    old_line_no=line.source_line_no,
                    new_line_no=line.target_line_no
                ))
            hunks.append(Hunk(
                old_start = hunk.source_start,
                old_length = hunk.source_length,
                new_start = hunk.target_start,
                new_length = hunk.target_length,
                section_heading = hunk.section_header,
                lines = tuple(lines)
            ))
        files.append(ChangedFile(
                old_path = None if file.is_added_file else
                    Path(file.source_file.removeprefix("a/")),
                new_path = None if file.is_removed_file else
                    Path(file.target_file.removeprefix("b/")),
                change_type = _change_type(file),
                is_binary = file.is_binary_file,
                hunks = tuple(hunks)
        ))

    return Diff(
        base_sha=merge_base.hexsha,
        head_sha=head.hexsha,
        files=tuple(files)
    )

