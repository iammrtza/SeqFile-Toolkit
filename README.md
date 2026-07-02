# SeqFile Toolkit

[![Tests](https://github.com/iammrtza/SeqFile-Toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/iammrtza/SeqFile-Toolkit/actions/workflows/tests.yml)

SeqFile Toolkit is a small Python command-line toolkit for everyday FASTA and
FASTQ file tasks:

- convert FASTQ or FASTQ.gz files to FASTA
- remove FASTA records with long A/C/G/T homopolymer runs
- generate random DNA sequences with optional exact nucleotide counts

The toolkit is dependency-free and runs with Python 3.9+.

## Installation

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/iammrtza/SeqFile-Toolkit.git
cd SeqFile-Toolkit
python -m pip install -e .
```

After installation, use the `seqfile-toolkit` command.

## Quick Start

Convert FASTQ to FASTA:

```bash
seqfile-toolkit fastq-to-fasta reads.fastq.gz -o reads.fasta
```

Filter FASTA records containing three or more repeated A/C/G/T bases:

```bash
seqfile-toolkit filter-repeats input.fasta -o filtered.fasta
```

Generate five 20 bp sequences with exact base composition:

```bash
seqfile-toolkit random --length 20 --number 5 --counts 5 5 5 5 --fasta -o random.fasta
```

Generate reproducible random sequences:

```bash
seqfile-toolkit random --length 12 --number 3 --seed 42
```

## Commands

### `fastq-to-fasta`

Converts FASTQ records to FASTA. Plain text and `.gz` input files are supported.

```bash
seqfile-toolkit fastq-to-fasta sample.fastq -o sample.fasta
```

If `--output` is omitted, FASTA is written to stdout:

```bash
seqfile-toolkit fastq-to-fasta sample.fastq.gz > sample.fasta
```

### `filter-repeats`

Removes FASTA records with homopolymer runs longer than the allowed maximum.
The default `--max-run 2` removes records containing `AAA`, `CCC`, `GGG`, or
`TTT`.

```bash
seqfile-toolkit filter-repeats input.fasta --max-run 2 -o filtered.fasta
```

Allow runs up to four bases:

```bash
seqfile-toolkit filter-repeats input.fasta --max-run 4 -o filtered.fasta
```

### `random`

Generates random DNA sequences.

```bash
seqfile-toolkit random --length 50 --number 10
```

Use exact counts for A, C, G, and T:

```bash
seqfile-toolkit random --length 40 --counts 10 10 10 10 --number 3
```

Write FASTA output and sequence summaries:

```bash
seqfile-toolkit random --length 40 --number 3 --fasta --summary -o random.fasta
```

## Legacy Scripts

The original script names are still available for backward compatibility:

```bash
python FASTQ_to_FASTA.py reads.fastq.gz -o reads.fasta
python nuc_repetition_filtering.py input.fasta -o filtered.fasta
python Random_Seq_Generator.py --length 20 --nucleotide 5 5 5 5 --number 3 --fasta
```

New users should prefer `seqfile-toolkit` because it has consistent help,
errors, and output options.

## Development

Install the package and run the test suite:

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Roadmap

- add paired FASTQ helpers
- add sequence statistics reports
- publish releases to PyPI
- add more examples from real NGS preprocessing workflows
