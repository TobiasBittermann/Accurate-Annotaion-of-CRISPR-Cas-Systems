#!/usr/bin/env python3

from Helper import format_fasta
from Annotater import annotate_Marcus
from pathlib import Path
import time
import shutil

def main():
    """
    Main function to run all filtering and formatting operations.
    Processes Marcus file database, formats FASTA files, and annotates sequences.
    """
    start_time = time.time()

    data_folder = "DB"
    temp_folder = "FASTA"
    dataset_small_folder = "DataModel/small"
    dataset_big_folder = "DataModel/big"

    # Create necessary directories
    Path(f"../{temp_folder}/Marcus_File").mkdir(parents=True, exist_ok=True)
    Path(f"../{dataset_small_folder}/Marcus_File").mkdir(parents=True, exist_ok=True)
    Path(f"../{dataset_big_folder}/Marcus_File").mkdir(parents=True, exist_ok=True)

    # =============================================================================
    # SECTION 1: FORMAT AND STANDARDIZE MARCUS FASTA FILE
    # =============================================================================
    if(True):
        print("FORMAT_FASTA")
        
        # Format the Marcus FASTA file and add cas12k subtype annotation
        # This standardizes the file format and adds subtype information to headers
        input_file = Path(f"../{data_folder}/Marcus_File/marcus_file.fasta")
        output_file = Path(f"../{temp_folder}/Marcus_File/marcus_file_formatted.fasta")
        appendix = " | subtype=cas12k"  # Subtype information added to each header
        line_length = 60  # Maximum characters per sequence line

        format_fasta.format_fasta(input_file, output_file, appendix, line_length)

    # =============================================================================
    # SECTION 2: ANNOTATE FORMATTED FASTA FILE
    # =============================================================================
    if(True):
        print("ANNOTATE_FASTA")
        
        # Annotate the formatted Marcus FASTA file with additional metadata
        # This processes the formatted file and adds comprehensive annotations
        
        # Define input and output file paths
        fasta_file = f"../{temp_folder}/Marcus_File/marcus_file_formatted.fasta"
        output_file=f"../{dataset_small_folder}/Marcus_File/marcus_annotated.fasta"

        annotate_Marcus.annotate_marcus_fasta(fasta_file, output_file)


    source = f"../{dataset_small_folder}/Marcus_File/marcus_annotated.fasta"
    destination = f"../{dataset_big_folder}/Marcus_File/marcus_annotated.fasta"

    shutil.copy(source, destination)

    # Calculate and display timing information
    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"\nStart Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print("--------------------------------------------------------------------------------")
    print(f"Total execution time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")
    print("All operations completed successfully!")

if __name__ == "__main__":
    main()