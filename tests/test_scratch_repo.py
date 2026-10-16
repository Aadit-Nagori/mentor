from .conftest import ScratchRepo


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
