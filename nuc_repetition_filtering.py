#!/usr/bin/env python3
"""Backward-compatible wrapper for homopolymer filtering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from seqfile_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["filter-repeats", *sys.argv[1:]]))
