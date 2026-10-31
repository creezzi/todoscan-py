from todoscan import scan
from todoscan.cli import main


def make_tree(tmp_path):
    (tmp_path / "a.py").write_text("x = 1  # TODO: fix this\n# FIXME(bob) later\nprint('ok')\n")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.js").write_text("/* HACK: temporary */\n")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "skip.js").write_text("// TODO ignored\n")
    (tmp_path / "bin.dat").write_bytes(b"\0\1TODO binary")
    return tmp_path


def test_scan_finds_tags_with_line_numbers(tmp_path):
    found = list(scan(str(make_tree(tmp_path))))
    summary = [(f.path.split("/")[-1], f.line, f.tag, f.text) for f in found]
    assert summary == [
        ("a.py", 1, "TODO", "fix this"),
        ("a.py", 2, "FIXME", "bob) later"),
        ("b.js", 1, "HACK", "temporary"),
    ]


def test_tag_filter(tmp_path):
    found = list(scan(str(make_tree(tmp_path)), tags=["HACK"]))
    assert [f.tag for f in found] == ["HACK"]


def test_words_containing_tags_do_not_match(tmp_path):
    (tmp_path / "c.txt").write_text("TODOS are not tasks\nmastodon\n")
    assert list(scan(str(tmp_path))) == []


def test_cli_strict_exit_codes(tmp_path, capsys):
    make_tree(tmp_path)
    assert main([str(tmp_path)]) == 0
    assert "a.py:1" in capsys.readouterr().out
    assert main([str(tmp_path), "--strict"]) == 1
    clean = tmp_path / "clean"
    clean.mkdir()
    (clean / "ok.py").write_text("pass\n")
    assert main([str(clean), "--strict"]) == 0
