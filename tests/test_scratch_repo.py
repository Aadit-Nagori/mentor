from conftest import ScratchRepo


def test_merge_base(tmp_path):
    r = ScratchRepo(tmp_path)
    r.write("app.py", "def f():\n    return 1\n")
    base = r.commit("initial")
    r.branch("feature")
    r.write("other.py", "x = 1\n")
    r.commit("unrelated work on main")
    r.checkout("feature")
    r.write("app.py", "def f():\n    return 2\n")
    r.commit("change f")

    assert r.run("merge-base", "main", "feature") == base

def test_2_dot_vs_3_dot(tmp_path):
    r = ScratchRepo(tmp_path)
    r.write("app.py", "def f():\n    return 1\n")
    r.commit("initial")
    r.branch("feature")
    r.write("other.py", "x = 1\n")      # still on main
    r.commit("unrelated work on main")   # <- main advances past the fork point
    r.checkout("feature")
    r.write("app.py", "def f():\n    return 2\n")
    r.commit("change f")
    two_dot = r.run("diff", "--name-only", "main..feature").splitlines()
    three_dot = r.run("diff", "--name-only", "main...feature").splitlines()

    assert "other.py" in two_dot
    assert "other.py" not in three_dot
    assert "app.py" in two_dot and "app.py" in three_dot

def test_binary(tmp_path):
    r = ScratchRepo(tmp_path)
    r.write("app.py", "def f():\n    return 1\n")
    r.commit("initial")
    r.branch("feature")
    r.checkout("feature")
    r.write_bytes("byte.py", b"\x00\x01\x02")
    r.commit("bytes")

    diff = r.run("diff","--numstat","main...feature")
    added, deleted, path = diff.split("\t")
    assert (added, deleted, path) == ("-", "-", "byte.py")

def test_no_trailing_newline(tmp_path):
    r = ScratchRepo(tmp_path)
    r.write("app.py", "def f():\n    return 1\n")
    r.commit("initial")
    r.branch("feature")
    r.checkout("feature")
    r.write("app.py", "def f():\n    return 1")   # same text, newline removed
    r.commit("strip newline")

    diff = r.run("diff", "main...feature")
    assert "\\ No newline at end of file" in diff

    numstat = r.run("diff", "--numstat", "main...feature")
    assert numstat == "1\t1\tapp.py"

