"""Small command-line tools for FASTA and FASTQ files."""

from .core import (
    FastaRecord,
    FastqRecord,
    convert_fastq_to_fasta,
    filter_homopolymers,
    generate_random_sequences,
    read_fasta,
    read_fastq,
    write_fasta,
)

__all__ = [
    "FastaRecord",
    "FastqRecord",
    "convert_fastq_to_fasta",
    "filter_homopolymers",
    "generate_random_sequences",
    "read_fasta",
    "read_fastq",
    "write_fasta",
]
