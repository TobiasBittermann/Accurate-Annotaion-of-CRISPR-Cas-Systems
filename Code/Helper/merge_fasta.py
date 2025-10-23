#!/usr/bin/env python3

import time
import sys
from pathlib import Path

def merge_fasta_files_all_dict(source_folder: Path, output_file: Path, ending):
    """
    Merge all FASTA files from the source folder (including subfolders) into a single output file.

    Args:
        source_folder (path): path to the source folder
        output_file (path): path to the output_file
    """

    #Ensure the output folder exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Check if the output file already exists
    output_file.touch(exist_ok=True)

    with open(output_file, 'w') as outfile:
        processed_sequences = 0

        # Recursively iterate over all FASTA files
        for fasta_file in Path(source_folder).resolve().rglob(f"*.{ending}"):
            if fasta_file.resolve() == output_file.resolve():
                # Skip the output file if it already exists
                continue
            with open(fasta_file, 'r') as infile:
                contents = infile.read()
                outfile.write(contents)
        
            processed_sequences += 1
            #print(f"Added {fasta_file.name}")
    
    print(f"Sequences added: {processed_sequences}")
    print(f"All files have been merged into {output_file}")

def merge_fasta_files_current_dir(source_folder: Path, output_file: Path, ending):
    """
    Merge all FASTA files from the source folder (only current directory, no subfolders) into a single output file.

    Args:
        source_folder (str): path to the source folder
        output_file (str): path to the output_file
    """
    
    #Ensure the output folder exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # Check if the output file already exists
    output_file.touch(exist_ok=True)

    with open(output_file, 'w') as outfile:
        processed_sequences = 0

        # Iterate only over FASTA files in the current directory
        for fasta_file in Path(source_folder).resolve().glob(f"*.{ending}"):
            if fasta_file.resolve() == output_file.resolve():
                # Skip the output file if it already exists
                continue
            with open(fasta_file, 'r') as infile:
                contents = infile.read()
                outfile.write(contents)
            processed_sequences += 1
            #print(f"Added {fasta_file.name}")
    
    print(f"\nSequences added: {processed_sequences}")
    print(f"All files in current directory have been merged into {output_file}")

if __name__ == "__main__":

    start_time = time.time()

    source_folder = Path('../DataModel/small/checks/cleaned_fasta')
    output_file = Path('../DataModel/small/checks/merge/merged.fasta')
    ending = "fasta"
    use_subfolders = True

    if (use_subfolders):
        merge_fasta_files_all_dict(source_folder, output_file, ending)
    else:
        merge_fasta_files_current_dir(source_folder, output_file, ending)


    end_time = time.time()
    elapsed_time = int(end_time - start_time)

    #Format elapsed time as hh:mm:ss
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print (f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")