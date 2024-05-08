#!/usr/bin/python3

"""
This script generates random DNA sequences with equal proportions for each nucleotide.
"""

import argparse
import numpy as np
import sys

# Initialize argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--length", type=int, required=True, help="The length of each DNA sequence")
parser.add_argument('-c', "--nucleotide", type=int, nargs='+', required=True,
                    help="Number of occurrences for A, C, G, T respectively")
parser.add_argument("-n", "--number", type=int, required=True, help="The number of DNA sequences to generate")
options = parser.parse_args()

# Check if the total sum of nucleotides matches the specified length
if sum(options.nucleotide) != options.length:
    print('An error occurred:')
    print('-- The total number of nucleotides does not match the specified length --')
else:
    def Random_generator(x):
        """
        Generates a random DNA sequence of specified length.

        Args:
        x (int): Length of the DNA sequence.

        Returns:
        str: Random DNA sequence.
        """
        dna = ''
        for i in range(x):
            # A simple weighted choice for nucleotides
            alphabet = np.random.choice(['A', 'T', 'C', 'G'], p=[0.25, 0.25, 0.25, 0.25])
            dna += alphabet
        return dna


    def oligo_generator():
        """
        Generates DNA sequences with specified nucleotide occurrences and lengths.
        """
        script = sys.argv[0]
        lengths = options.length
        number_of_oligos = options.number
        nucleotide_A = options.nucleotide[0]
        nucleotide_C = options.nucleotide[1]
        nucleotide_G = options.nucleotide[2]
        nucleotide_T = options.nucleotide[3]
        z = 2
        i = 1
        cnt = 1
        while i < z:
            dna = Random_generator(lengths)  # Length of oligo
            dna_length = len(dna)
            A_cnt = dna.count('A')
            T_cnt = dna.count('T')
            C_cnt = dna.count('C')
            G_cnt = dna.count('G')
            a_percentage = (A_cnt) * 100.0 / dna_length
            t_percentage = (T_cnt) * 100.0 / dna_length
            c_percentage = (C_cnt) * 100.0 / dna_length
            g_percentage = (G_cnt) * 100.0 / dna_length
            if A_cnt == nucleotide_A and \
                    C_cnt == nucleotide_C and \
                    G_cnt == nucleotide_G and \
                    T_cnt == nucleotide_T:
                print(dna)
                print('-------')
                print('total length is ' + str(len(dna)))
                print('number of A ' + str(A_cnt))
                print('number of C ' + str(C_cnt))
                print('number of G ' + str(G_cnt))
                print('number of T ' + str(T_cnt))
                print('-------')
                print('% of A ' + str(a_percentage) + '\n' +
                      '% of C ' + str(c_percentage) + '\n' +
                      '% of G ' + str(g_percentage) + '\n' +
                      '% of T ' + str(t_percentage))
                if cnt == number_of_oligos:  # Number of outputs
                    break
                cnt += 1
                print('\n')


    if __name__ == '__main__':
        oligo_generator()
