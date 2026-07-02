import tempfile
import unittest
from pathlib import Path

from seqfile_toolkit.cli import main


class CliTests(unittest.TestCase):
    def test_fastq_to_fasta_cli_writes_output_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            fastq = Path(tmp_dir) / "reads.fastq"
            fasta = Path(tmp_dir) / "reads.fasta"
            fastq.write_text("@read1 sample\nACGT\n+\n!!!!\n", encoding="utf-8")

            exit_code = main(["fastq-to-fasta", str(fastq), "-o", str(fasta)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(fasta.read_text(encoding="utf-8"), ">read1 sample\nACGT\n")

    def test_random_cli_can_write_reproducible_fasta(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "random.fa"

            exit_code = main(
                [
                    "random",
                    "--length",
                    "4",
                    "--number",
                    "2",
                    "--counts",
                    "1",
                    "1",
                    "1",
                    "1",
                    "--seed",
                    "7",
                    "--fasta",
                    "-o",
                    str(output),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output.read_text(encoding="utf-8").startswith(">random_1\n"))


if __name__ == "__main__":
    unittest.main()
