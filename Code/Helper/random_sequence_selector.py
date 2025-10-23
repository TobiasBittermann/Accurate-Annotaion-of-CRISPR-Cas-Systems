import random
from Bio import SeqIO
import argparse
import sys

input_folder = "../DataModel/small/checks/sorted_fasta_small"

input_fasta = f"{input_folder}/cas12m.fasta"
output_fasta = f"{input_folder}/cas12m_subset.fasta"

def select_random_sequences(input_fasta, output_fasta, num_sequences=600):
    """
    Selects random sequences from a FASTA file and writes them to a new file.
    
    Args:
        input_fasta (str): Path to input FASTA file
        output_fasta (str): Path to output FASTA file
        num_sequences (int): Number of sequences to select (default: 600)
    """
    try:
        # Read all sequences from input file
        sequences = list(SeqIO.parse(input_fasta, "fasta"))
        total_sequences = len(sequences)
        
        print(f"Total sequences in input file: {total_sequences}")
        
        # Check if we have enough sequences
        if total_sequences < num_sequences:
            print(f"Warning: Only {total_sequences} sequences available, selecting all of them.")
            selected_sequences = sequences
        else:
            # Randomly select sequences
            selected_sequences = random.sample(sequences, num_sequences)
            print(f"Randomly selected {num_sequences} sequences.")
        
        # Write selected sequences to output file
        with open(output_fasta, "w") as output_handle:
            SeqIO.write(selected_sequences, output_handle, "fasta")
        
        print(f"Selected sequences written to: {output_fasta}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_fasta}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    # Set a default seed for reproducibility
    random.seed(42)
    
    # Use the predefined paths
    select_random_sequences(input_fasta, output_fasta, 400)

if __name__ == "__main__":
    main()