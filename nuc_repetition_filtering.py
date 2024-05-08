#!/usr/bin/python3

###
#This script removes sequences containing repeated nucleotides (GGG, AAA, TTT, CCC) from a FASTA file.
###

import sys
from Bio import SeqIO

def remove_seqs():
    """
    Function to remove sequences containing repeated nucleotides.
    """
    script = sys.argv[0]  # Path of the script
    file_name = sys.argv[1]  # Input FASTA file name

    # Define nucleotide repetition conditions
    Condition_A = 'AAA'
    Condition_T = 'TTT'
    Condition_C = 'CCC'
    Condition_G = 'GGG'

    # Open the input FASTA file
    with open(file_name, "r") as fasta:
        # Iterate over each sequence in the file
        for record in SeqIO.parse(fasta, "fasta"):
            # Check if any of the nucleotide repetitions are present in the sequence
            if Condition_A not in record.seq and \
                Condition_T not in record.seq and \
                Condition_C not in record.seq and \
                Condition_G not in record.seq:
                # Print the sequence ID and sequence itself if no repetitions are found
                print('>' + record.id)
                print(record.seq)

if __name__ == '__main__':
    remove_seqs()

