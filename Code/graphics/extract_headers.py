#!/usr/bin/env python3

import os
import time
import csv
from pathlib import Path
from collections import defaultdict

def write_header(input_folder: str):
    """
    Extracts headers from all FASTA files in a directory tree and creates
    separate CSV files for each folder containing FASTA files.
    
    Args:
        input_folder (str): Path to the root directory to search for FASTA files
    """
    
    # Convert input folder to Path object for easier file operations
    root_folder = Path(input_folder)
    outfolder = f"../../HEADERS"  # Output directory for CSV files
    name = "headers"  # Base name for output files

    # Create output directory if it doesn't exist
    os.makedirs(outfolder, exist_ok=True)

    # Dictionary to group FASTA files by their parent folder
    folders = defaultdict(list)

    # Recursively find all FASTA files and group them by folder
    for file in root_folder.rglob("*fasta"):
        folder = file.parent  # Get the parent directory of the FASTA file
        folders[folder].append(file)  # Add file to the folder's list

    # Process each folder that contains FASTA files
    for folder, fasta_files in folders.items():
        folder_name = folder.name  # Get the folder name for the output filename
        outfile = f"{outfolder}/headers_{folder_name}.csv"  # Create output filename

        # Create CSV file for this folder
        with open(outfile, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Header'])  # Write CSV header row
                
            # Process each FASTA file in this folder
            for file in fasta_files:
                with open(file, 'r') as infile:
                    # Read each line in the FASTA file
                    for line in infile:
                        # Check if line is a header (starts with '>')
                        if line.startswith('>'):
                            header = line.strip()  # Remove newline characters
                            writer.writerow([header])  # Write header to CSV
                print(f"{folder_name}_header CSV written.")

if __name__ == "__main__":
    start_time = time.time()

    write_header("../../FASTA")

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


