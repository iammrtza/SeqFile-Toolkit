"""Core FASTA/FASTQ utilities used by the command-line interface."""

from __future__ import annotations

import gzip
import random
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, TextIO


NUCLEOTIDES = ("A", "C", "G", "T")


@dataclass(frozen=True)
class FastaRecord:
    """One FASTA record."""

    identifier: str
    sequence: str
    description: str = ""


@dataclass(frozen=True)
class FastqRecord:
    """One FASTQ record."""

    identifier: str
    sequence: str
    quality: str
    description: str = ""


def open_text(path: str | Path, mode: str = "rt") -> TextIO:
    """Open plain text or gzip-compressed files by file extension."""

    path = Path(path)
    if path.suffix == ".gz":
        return gzip.open(path, mode)
    return path.open(mode, encoding="utf-8")


def read_fasta(handle: TextIO) -> Iterator[FastaRecord]:
    """Yield FASTA records from an open text handle."""

    header: str | None = None
    chunks: list[str] = []

    for line_number, raw_line in enumerate(handle, start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                yield _build_fasta_record(header, chunks)
            header = line[1:].strip()
            chunks = []
            continue
        if header is None:
            raise ValueError(f"Expected FASTA header before line {line_number}.")
        chunks.append(line)

    if header is not None:
        yield _build_fasta_record(header, chunks)


def read_fastq(handle: TextIO) -> Iterator[FastqRecord]:
    """Yield FASTQ records from an open text handle."""

    record_number = 0
    while True:
        header = handle.readline()
        if not header:
            return
        record_number += 1
        sequence = handle.readline()
        plus = handle.readline()
        quality = handle.readline()

        if not quality:
            raise ValueError(f"FASTQ record {record_number} is incomplete.")
        if not header.startswith("@"):
            raise ValueError(f"FASTQ record {record_number} does not start with '@'.")
        if not plus.startswith("+"):
            raise ValueError(f"FASTQ record {record_number} is missing the '+' line.")

        sequence_text = sequence.strip()
        quality_text = quality.strip()
        if len(sequence_text) != len(quality_text):
            raise ValueError(
                f"FASTQ record {record_number} has sequence and quality lengths "
                f"{len(sequence_text)} and {len(quality_text)}."
            )

        identifier, description = _split_header(header[1:].strip())
        yield FastqRecord(
            identifier=identifier,
            description=description,
            sequence=sequence_text.upper(),
            quality=quality_text,
        )


def write_fasta(records: Iterable[FastaRecord], handle: TextIO, line_width: int = 80) -> int:
    """Write FASTA records and return the number of records written."""

    count = 0
    for record in records:
        count += 1
        header = record.identifier
        if record.description:
            header = f"{header} {record.description}"
        handle.write(f">{header}\n")
        for start in range(0, len(record.sequence), line_width):
            handle.write(f"{record.sequence[start:start + line_width]}\n")
    return count


def convert_fastq_to_fasta(input_path: str | Path, output: TextIO = sys.stdout) -> int:
    """Convert FASTQ records from a file to FASTA written to an output handle."""

    with open_text(input_path) as handle:
        records = (
            FastaRecord(record.identifier, record.sequence, record.description)
            for record in read_fastq(handle)
        )
        return write_fasta(records, output)


def filter_homopolymers(
    input_path: str | Path,
    output: TextIO = sys.stdout,
    max_run: int = 2,
) -> tuple[int, int]:
    """Keep FASTA records whose A/C/G/T homopolymer runs are at most max_run."""

    kept = 0
    removed = 0

    with open_text(input_path) as handle:
        for record in read_fasta(handle):
            if has_homopolymer(record.sequence, max_run=max_run):
                removed += 1
            else:
                kept += write_fasta([record], output)

    return kept, removed


def has_homopolymer(sequence: str, max_run: int = 2) -> bool:
    """Return True if sequence contains an A/C/G/T run longer than max_run."""

    if max_run < 1:
        raise ValueError("max_run must be at least 1.")

    current_base = ""
    current_run = 0
    for base in sequence.upper():
        if base in NUCLEOTIDES and base == current_base:
            current_run += 1
        else:
            current_base = base
            current_run = 1
        if base in NUCLEOTIDES and current_run > max_run:
            return True
    return False


def generate_random_sequences(
    length: int,
    counts: dict[str, int] | None = None,
    number: int = 1,
    seed: int | None = None,
) -> list[str]:
    """Generate random DNA sequences with exact optional nucleotide counts."""

    if length < 1:
        raise ValueError("length must be at least 1.")
    if number < 1:
        raise ValueError("number must be at least 1.")

    rng = random.Random(seed)
    sequences: list[str] = []

    if counts is None:
        for _ in range(number):
            sequences.append("".join(rng.choice(NUCLEOTIDES) for _ in range(length)))
        return sequences

    normalized_counts = {base: int(counts.get(base, 0)) for base in NUCLEOTIDES}
    if any(value < 0 for value in normalized_counts.values()):
        raise ValueError("nucleotide counts cannot be negative.")
    if sum(normalized_counts.values()) != length:
        raise ValueError("nucleotide counts must add up to length.")

    template = "".join(base * normalized_counts[base] for base in NUCLEOTIDES)
    for _ in range(number):
        bases = list(template)
        rng.shuffle(bases)
        sequences.append("".join(bases))

    return sequences


def sequence_summary(sequence: str) -> dict[str, int | float]:
    """Return length, base counts, and GC percentage for a sequence."""

    counts = Counter(sequence.upper())
    length = len(sequence)
    gc = counts["G"] + counts["C"]
    gc_percent = round((gc / length) * 100, 2) if length else 0.0
    return {
        "length": length,
        "A": counts["A"],
        "C": counts["C"],
        "G": counts["G"],
        "T": counts["T"],
        "GC_percent": gc_percent,
    }


def _build_fasta_record(header: str, chunks: list[str]) -> FastaRecord:
    identifier, description = _split_header(header)
    return FastaRecord(identifier, "".join(chunks).upper(), description)


def _split_header(header: str) -> tuple[str, str]:
    parts = header.split(maxsplit=1)
    if not parts:
        raise ValueError("Encountered an empty sequence identifier.")
    description = parts[1] if len(parts) == 2 else ""
    return parts[0], description
