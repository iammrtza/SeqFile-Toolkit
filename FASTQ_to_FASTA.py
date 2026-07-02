#!/usr/bin/env python3
"""Backward-compatible wrapper for FASTQ to FASTA conversion."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from seqfile_toolkit.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["fastq-to-fasta", *sys.argv[1:]]))
