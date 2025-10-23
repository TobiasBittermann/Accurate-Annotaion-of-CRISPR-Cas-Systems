#!/usr/bin/env python3

from Helper import format_fasta
from Helper import merge_fasta
from Helper import filter_faa_casette_CSV
from Annotater import annotate_NCBI
from pathlib import Path
import time

def main():
    start_time = time.time()

    data_folder = "DB"
    temp_folder = "FASTA"
    dataset_small_folder = "DataModel/small"
    dataset_big_folder = "DataModel/big"

    # =============================================================================
    # SECTION 1: FILTER FASTA FILES ACCORDING TO CASSETTE CSV
    # =============================================================================
    if(True):
        #Small DataModel
        fasta_folder = f"../{data_folder}/NCBI/2_NCBI_Processed/"
        csv_file = f"../{data_folder}/NCBI/Complete_Cassette_summary.csv"
        output_dir = f"../{temp_folder}/NCBI/3_NCBI_Filtered/"

        # Call function once with the entire folder (not per file)
        filter_faa_casette_CSV.filter_faa_casette_CSV(csv_file, fasta_folder, output_dir)


    # =============================================================================
    # SECTION 2: ANNOTATE AND SUBTYPE FASTA FILES
    # =============================================================================
    if(True):
        #Small DataModel
        fasta_folder = f"../{data_folder}/NCBI/3_NCBI_Filtered/"
        csv_file = f"../{data_folder}/NCBI/Complete_Cassette_summary.csv"
        output_dir = f"../{temp_folder}/NCBI/4.1_NCBI_subtyped/"

        for fasta_file in Path(fasta_folder).glob("*.faa"):
            annotate_NCBI.process_fasta_file(fasta_file, csv_file, output_dir)

        #Big DataModel
        fasta_folder = f"../{data_folder}/NCBI/2_NCBI_Processed/"
        csv_file = f"../{data_folder}/NCBI/Complete_Cassette_summary.csv"
        output_dir = f"../{temp_folder}/NCBI/4.2_NCBI_subtyped/"

        for fasta_file in Path(fasta_folder).glob("*.faa"):
            annotate_NCBI.process_fasta_file(fasta_file, csv_file, output_dir)

    # =============================================================================
    # SECTION 3: MERGE ANNOTATED FASTA FILES
    # =============================================================================
    if(True):
        #Small DataModel
        print("MERGE_FASTA")
        input_folder = f"../{temp_folder}/NCBI/4.1_NCBI_subtyped"
        output_file = f"../{temp_folder}/NCBI/5.1_NCBI_merged/merged_NCBI.fasta"
        ending = "fasta"
        use_subfolders = False

        if use_subfolders:
            merge_fasta.merge_fasta_files_all_dict(Path(input_folder), Path(output_file), ending)
        else:
            merge_fasta.merge_fasta_files_current_dir(Path(input_folder), Path(output_file), ending)
        print(f"Merged FASTA files saved to {output_file}")

        #Big DataModel
        print("MERGE_FASTA")
        input_folder = f"../{temp_folder}/NCBI/4.2_NCBI_subtyped"
        output_file = f"../{temp_folder}/NCBI/5.2_NCBI_merged/merged_NCBI.fasta"
        ending = "fasta"
        use_subfolders = False

        if use_subfolders:
            merge_fasta.merge_fasta_files_all_dict(Path(input_folder), Path(output_file), ending)
        else:
            merge_fasta.merge_fasta_files_current_dir(Path(input_folder), Path(output_file), ending)
        print(f"Merged FASTA files saved to {output_file}")

    # =============================================================================
    # SECTION 4: FORMAT AND STANDARDIZE FINAL FASTA FILE
    # =============================================================================
    if(True):
        #Small DataModel
        print("FORMAT_FASTA")
        input_file = Path(f"../{temp_folder}/NCBI/5.1_NCBI_merged/merged_NCBI.fasta")
        output_file = Path(f"../{dataset_small_folder}/NCBI/NCBI.fasta")
        appendix = ""
        line_length = 60

        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file}")

        #Big DataModel
        print("FORMAT_FASTA")
        input_file = Path(f"../{temp_folder}/NCBI/5.2_NCBI_merged/merged_NCBI.fasta")
        output_file = Path(f"../{dataset_big_folder}/NCBI/NCBI.fasta")
        appendix = ""
        line_length = 60

        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file}")



    # Calculate and display execution timing information
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