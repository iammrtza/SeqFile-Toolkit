"""Command-line interface for SeqFile Toolkit."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import (
    convert_fastq_to_fasta,
    filter_homopolymers,
    generate_random_sequences,
    open_text,
    sequence_summary,
)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return args.func(args)
    except BrokenPipeError:
        return 1
    except (OSError, ValueError) as exc:
        parser.exit(2, f"seqfile-toolkit: error: {exc}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seqfile-toolkit",
        description="Small, dependency-free utilities for FASTA and FASTQ files.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    convert = subparsers.add_parser(
        "fastq-to-fasta",
        help="Convert FASTQ or FASTQ.gz records to FASTA.",
    )
    convert.add_argument("input", help="Input FASTQ file. .gz files are supported.")
    convert.add_argument(
        "-o",
        "--output",
        help="Output FASTA file. Defaults to stdout.",
    )
    convert.set_defaults(func=run_fastq_to_fasta)

    filter_parser = subparsers.add_parser(
        "filter-repeats",
        help="Remove FASTA records with long A/C/G/T homopolymer runs.",
    )
    filter_parser.add_argument("input", help="Input FASTA file. .gz files are supported.")
    filter_parser.add_argument(
        "-m",
        "--max-run",
        type=int,
        default=2,
        help="Maximum allowed homopolymer run length. Default: 2.",
    )
    filter_parser.add_argument(
        "-o",
        "--output",
        help="Output FASTA file. Defaults to stdout.",
    )
    filter_parser.set_defaults(func=run_filter_repeats)

    random_parser = subparsers.add_parser(
        "random",
        help="Generate random DNA sequences.",
    )
    random_parser.add_argument("-l", "--length", type=int, required=True)
    random_parser.add_argument("-n", "--number", type=int, default=1)
    random_parser.add_argument(
        "-c",
        "--counts",
        nargs=4,
        metavar=("A", "C", "G", "T"),
        type=int,
        help="Exact counts for A C G T. Values must add up to --length.",
    )
    random_parser.add_argument("--seed", type=int, help="Seed for reproducible output.")
    random_parser.add_argument(
        "--fasta",
        action="store_true",
        help="Write generated sequences as FASTA instead of one sequence per line.",
    )
    random_parser.add_argument(
        "--summary",
        action="store_true",
        help="Print tab-separated sequence summaries to stderr.",
    )
    random_parser.add_argument("-o", "--output", help="Output file. Defaults to stdout.")
    random_parser.set_defaults(func=run_random)

    return parser


def run_fastq_to_fasta(args: argparse.Namespace) -> int:
    with _output_handle(args.output) as output:
        count = convert_fastq_to_fasta(args.input, output)
    print(f"Converted {count} record(s).", file=sys.stderr)
    return 0


def run_filter_repeats(args: argparse.Namespace) -> int:
    with _output_handle(args.output) as output:
        kept, removed = filter_homopolymers(args.input, output, max_run=args.max_run)
    print(f"Kept {kept} record(s); removed {removed} record(s).", file=sys.stderr)
    return 0


def run_random(args: argparse.Namespace) -> int:
    counts = None
    if args.counts:
        counts = dict(zip(("A", "C", "G", "T"), args.counts))

    sequences = generate_random_sequences(
        length=args.length,
        counts=counts,
        number=args.number,
        seed=args.seed,
    )

    with _output_handle(args.output) as output:
        for index, sequence in enumerate(sequences, start=1):
            if args.fasta:
                output.write(f">random_{index}\n{sequence}\n")
            else:
                output.write(f"{sequence}\n")

            if args.summary:
                summary = sequence_summary(sequence)
                print(
                    "random_{index}\tlength={length}\tA={A}\tC={C}\tG={G}\tT={T}\tGC={GC_percent}%".format(
                        index=index,
                        **summary,
                    ),
                    file=sys.stderr,
                )

    return 0


def _output_handle(path: str | None):
    if path is None:
        return _StdoutContext()
    return open_text(Path(path), "wt")


class _StdoutContext:
    def __enter__(self):
        return sys.stdout

    def __exit__(self, exc_type, exc, traceback):
        return False


if __name__ == "__main__":
    raise SystemExit(main())
