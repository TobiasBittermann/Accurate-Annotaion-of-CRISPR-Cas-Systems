#!/usr/bin/env python3

import time
from pathlib import Path

def format_fasta(input_file: Path, output_file: Path, appendix: str, line_length: int):
    """
    Reads a FASTA file and rewrites the sequences so that
    each sequence line has a maximum of `line_length` characters.
    Writes the formatted sequences to a new output file.
    The appendix is added to each header line.
    """
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Create the output file if it does not exist
    output_file.touch(exist_ok=True)

    with input_file.open("r") as infile, output_file.open("w") as outfile:
        sequence = ""
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                # Write the previous sequence before processing the new header
                if sequence:
                    for i in range(0, len(sequence), line_length):
                        outfile.write(sequence[i:i+line_length] + "\n")
                # Write the header with appendix
                outfile.write(f"{line}{appendix}\n")
                sequence = ""
            else:
                sequence += line
        # Write the last sequence after file is fully read
        if sequence:
            for i in range(0, len(sequence), line_length):
                outfile.write(sequence[i:i+line_length] + "\n")
    print(f"Formatted FASTA file written to {output_file}")

input_file = Path("../DB/Marcus_File/marcus_file.fasta")
output_file = Path("../FASTA/Marcus_File/marcus_file_formatted.fasta")
appendix = " | subtype=cas12k"  # Subtype information added to each header
line_length = 60  # Maximum characters per sequence line

if __name__ == "__main__":
    start_time = time.time()

    format_fasta(input_file, output_file, appendix, line_length)

    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("\n")
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print("--------------------------------------------------------------------------------")
    print(f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")

