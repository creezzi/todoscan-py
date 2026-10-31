"""Scan source trees for task comments."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Iterator, Sequence

__all__ = ["Finding", "scan"]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "target", "dist", "build"}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    tag: str
    text: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.tag}] {self.text}"


def _is_text(path: str) -> bool:
    with open(path, "rb") as f:
        return b"\0" not in f.read(2048)


def scan(root: str, tags: Sequence[str] = ("TODO", "FIXME", "HACK")) -> Iterator[Finding]:
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, tags)) + r")\b[:\s(]*(.*)")
    paths = [root] if os.path.isfile(root) else (
        os.path.join(d, f)
        for d, dirs, files in os.walk(root)
        for _ in [dirs.sort() or dirs.__setitem__(slice(None), [x for x in dirs if x not in SKIP_DIRS])]
        for f in sorted(files)
    )
    for path in paths:
        try:
            if not _is_text(path):
                continue
            with open(path, encoding="utf-8", errors="replace") as f:
                for number, line in enumerate(f, 1):
                    m = pattern.search(line)
                    if m:
                        yield Finding(path, number, m.group(1), m.group(2).strip().rstrip("*/").strip())
        except OSError:
            continue
