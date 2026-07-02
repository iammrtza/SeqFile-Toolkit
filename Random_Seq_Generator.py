#!/usr/bin/env python3
"""Backward-compatible wrapper for random DNA sequence generation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from seqfile_toolkit.cli import main


def _translate_legacy_args(argv):
    translated = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in {"-c", "--nucleotide"}:
            translated.append("--counts")
            translated.extend(argv[index + 1:index + 5])
            index += 5
            continue
        translated.append(arg)
        index += 1
    return translated


if __name__ == "__main__":
    raise SystemExit(main(["random", *_translate_legacy_args(sys.argv[1:])]))
