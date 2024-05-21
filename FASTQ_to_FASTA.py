# This script converts FASTQ files to FASTA files.
import gzip
from Bio import SeqIO
import sys

def fastq_to_fasta():
    # Retrieve the script name and input file name from the command line arguments
    script = sys.argv[0]
    input_f = sys.argv[1]

    # Open the input FASTQ file, handling gzip compression
    with gzip.open(input_f, 'rt') as Fastq:
        # Parse the FASTQ file and process each record
        for record in SeqIO.parse(Fastq, 'fastq'):
            # Print the sequence ID in FASTA format
            print('>' + record.id)
            # Print the sequence
            print(record.seq)

# If the script is executed directly (not imported as a module), run the function
if __name__ == '__main__':
    fastq_to_fasta()