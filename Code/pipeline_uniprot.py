#!/usr/bin/env python3

import format_fasta
import annotate_uniprot
import filter_uniprot
from pathlib import Path
import time

def main():
    start_time = time.time()

    data_folder = "DB"
    temp_folder = "FASTA"
    dataset_small_folder = "DataModel/small"
    dataset_big_folder = "DataModel/big"

    Path(f"../{dataset_small_folder}").mkdir(parents=True, exist_ok=True)
    Path(f"../{dataset_big_folder}").mkdir(parents=True, exist_ok=True)

    # =============================================================================
    # SECTION 1: FILTER UNIPROT
    # =============================================================================
    if(True):
        print("FILTER UNIPROT")

        input_folder = f"../{data_folder}/uniprot/1_raw/"
        output_folder = f"../{temp_folder}/uniprot/2_filtered/"

        name = "uniprot_trembl"
        input_file = f"{input_folder}/{name}.fasta"
        output_file = f"{output_folder}/{name}_filtered.fasta"
        filter_uniprot.filter_uniprot(input_file, output_file, "cas12", "-like", 5)
        print(f"Filtered UniProt Trembl file saved to {output_file}")

        name_2 = "uniprot_sprot"
        input_file_2 = f"{input_folder}/{name_2}.fasta"
        output_file_2 = f"{output_folder}/{name_2}_filtered.fasta"
        filter_uniprot.filter_uniprot(input_file_2, output_file_2, "cas12", "-like", 5)
        print(f"Filtered UniProt Sprot file saved to {output_file_2}")

    # =============================================================================
    # SECTION 2: FORMAT SPECIFIC FASTA FILE
    # =============================================================================
    if(True):
        print("\nFORMAT_FASTA")

        #Small DataModel
        input_folder = f"../{temp_folder}/uniprot/2_filtered"
        output_folder = f"../{temp_folder}/uniprot/3.1_formatted"

        name = "uniprot_trembl"
        input_file = Path(f"{input_folder}/{name}_filtered.fasta")
        output_file = Path(f"{output_folder}/{name}_formatted.fasta")

        name_2 = "uniprot_sprot"
        input_file_2 = Path(f"{input_folder}/{name_2}_filtered.fasta")
        output_file_2 = Path(f"{output_folder}/{name_2}_formatted.fasta")

        appendix = ""
        line_length = 60

        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        format_fasta.format_fasta(input_file_2, output_file_2, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_folder}")

        #Big DataModel
        input_folder = f"../{data_folder}/uniprot/1_raw/"
        output_folder = f"../{temp_folder}/uniprot/3.2_formatted"

        name = "uniprot_trembl"
        input_file = Path(f"{input_folder}/{name}.fasta")
        output_file = Path(f"{output_folder}/{name}_formatted.fasta")

        name_2 = "uniprot_sprot"
        input_file_2 = Path(f"{input_folder}/{name_2}.fasta")
        output_file_2 = Path(f"{output_folder}/{name_2}_formatted.fasta")

        appendix = ""
        line_length = 60

        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        format_fasta.format_fasta(input_file_2, output_file_2, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_folder}")
    # =============================================================================
    # SECTION 3: UNIFY HEADER
    # =============================================================================
    if(True):
        print("\nUNIFY_HEADER")

        #Small DataModel
        input_folder = f"../{temp_folder}/uniprot/3.1_formatted"
        output_folder = f"../{dataset_small_folder}/uniprot"

        name = "uniprot_trembl"
        input_file = Path(f"{input_folder}/{name}_formatted.fasta")
        output_file = Path(f"{output_folder}/{name}.fasta")

        name_2 = "uniprot_sprot"
        input_file_2 = Path(f"{input_folder}/{name_2}_formatted.fasta")
        output_file_2 = Path(f"{output_folder}/{name_2}.fasta")

        annotate_uniprot.annotate_uniprot_fasta(input_file, output_file)
        annotate_uniprot.annotate_uniprot_fasta(input_file_2, output_file_2)

        #Big DataModel
        input_folder = f"../{temp_folder}/uniprot/3.2_formatted"
        output_folder = f"../{dataset_big_folder}/uniprot"

        name = "uniprot_trembl"
        input_file = Path(f"{input_folder}/{name}_formatted.fasta")
        output_file = Path(f"{output_folder}/{name}.fasta")

        name_2 = "uniprot_sprot"
        input_file_2 = Path(f"{input_folder}/{name_2}_formatted.fasta")
        output_file_2 = Path(f"{output_folder}/{name_2}.fasta")

        annotate_uniprot.annotate_uniprot_fasta(input_file, output_file)
        annotate_uniprot.annotate_uniprot_fasta(input_file_2, output_file_2)
        




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