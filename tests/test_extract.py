from pathlib import Path

from conftest import ScratchRepo

from mentor.datamodels import ChangeType, LineKind
from mentor.extract import extract


def test_simple_modification(tmp_path):
    r = ScratchRepo(tmp_path)
    r.write("app.py", "def f():\n    return 1\n")
    base = r.commit("initial")
    r.write("app.py", "def f():\n    return 2\n")
    head = r.commit("change f")

    diff = extract(tmp_path, base, head)

    assert diff.base_sha == base
    assert diff.head_sha == head
    assert len(diff.files) == 1

    f = diff.files[0]
    assert f.change_type == ChangeType.MODIFIED
    assert f.old_path == f.new_path == Path("app.py")
    assert not f.is_binary
    assert len(f.hunks) == 1

    lines = [(Ln.kind, Ln.content, Ln.old_line_no, Ln.new_line_no) for Ln in f.hunks[0].lines]
    assert lines == [
        (LineKind.CONTEXT, "def f():\n",     1,    1),
        (LineKind.REMOVED, "    return 1\n", 2,    None),
        (LineKind.ADDED,   "    return 2\n", None, 2),
    ]

def test_simple_modification_refs(tmp_path):
    r = ScratchRepo(tmp_path)
    r.write("app.py", "def f():\n    return 1\n")
    base = r.commit("initial")
    r.branch("feature")
    r.checkout("feature")
    r.write("app.py", "def f():\n    return 2\n")
    head = r.commit("change f")

    diff = extract(tmp_path, "main", "feature")

    assert diff.base_sha == base
    assert diff.head_sha == head
    assert len(diff.files) == 1

    f = diff.files[0]
    assert f.change_type == ChangeType.MODIFIED
    assert f.old_path == f.new_path == Path("app.py")
    assert not f.is_binary
    assert len(f.hunks) == 1

    lines = [(Ln.kind, Ln.content, Ln.old_line_no, Ln.new_line_no) for Ln in f.hunks[0].lines]
    assert lines == [
        (LineKind.CONTEXT, "def f():\n",     1,    1),
        (LineKind.REMOVED, "    return 1\n", 2,    None),
        (LineKind.ADDED,   "    return 2\n", None, 2),
    ]
