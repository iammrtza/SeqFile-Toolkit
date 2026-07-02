import io
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from seqfile_toolkit.core import (
    FastaRecord,
    filter_homopolymers,
    generate_random_sequences,
    has_homopolymer,
    read_fasta,
    read_fastq,
    write_fasta,
)


class CoreTests(unittest.TestCase):
    def test_read_fasta_parses_multiline_records(self):
        data = io.StringIO(">seq1 description\nACG\nTT\n>seq2\nccgg\n")

        records = list(read_fasta(data))

        self.assertEqual(
            records,
            [
                FastaRecord("seq1", "ACGTT", "description"),
                FastaRecord("seq2", "CCGG", ""),
            ],
        )

    def test_read_fastq_validates_quality_length(self):
        data = io.StringIO("@seq1\nACGT\n+\n!!!\n")

        with self.assertRaisesRegex(ValueError, "sequence and quality lengths"):
            list(read_fastq(data))

    def test_write_fasta_wraps_sequences(self):
        output = io.StringIO()

        count = write_fasta([FastaRecord("seq1", "ACGTACGT")], output, line_width=4)

        self.assertEqual(count, 1)
        self.assertEqual(output.getvalue(), ">seq1\nACGT\nACGT\n")

    def test_homopolymer_filter_keeps_records_with_allowed_runs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            fasta = Path(tmp_dir) / "input.fa"
            fasta.write_text(">keep\nAACCGGTT\n>drop\nAACCCGTT\n", encoding="utf-8")
            output = io.StringIO()

            kept, removed = filter_homopolymers(fasta, output, max_run=2)

        self.assertEqual(kept, 1)
        self.assertEqual(removed, 1)
        self.assertEqual(output.getvalue(), ">keep\nAACCGGTT\n")

    def test_has_homopolymer_uses_configurable_run_length(self):
        self.assertFalse(has_homopolymer("AAGGTT", max_run=2))
        self.assertTrue(has_homopolymer("AAAGTT", max_run=2))
        self.assertFalse(has_homopolymer("AAAGTT", max_run=3))

    def test_generate_random_sequences_uses_exact_counts_and_seed(self):
        sequences = generate_random_sequences(
            length=8,
            counts={"A": 2, "C": 2, "G": 2, "T": 2},
            number=3,
            seed=42,
        )

        self.assertEqual(len(sequences), 3)
        self.assertEqual(
            sequences,
            generate_random_sequences(
                length=8,
                counts={"A": 2, "C": 2, "G": 2, "T": 2},
                number=3,
                seed=42,
            ),
        )
        self.assertTrue(all(Counter(sequence) == Counter("AACCGGTT") for sequence in sequences))

    def test_generate_random_sequences_rejects_bad_counts(self):
        with self.assertRaisesRegex(ValueError, "add up to length"):
            generate_random_sequences(length=4, counts={"A": 4, "C": 1}, number=1)


if __name__ == "__main__":
    unittest.main()
