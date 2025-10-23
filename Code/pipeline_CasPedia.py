#!/usr/bin/env python3

from Helper import format_fasta
from Helper import merge_fasta
from Helper import cas_translator
from Annotater import annotate_CasPedia
from pathlib import Path
import time
import shutil

def main():
    """
    Main function to run all filtering and formatting operations.
    Processes UniProt databases, formats FASTA files, and merges multiple files.
    """
    start_time = time.time()

    data_folder = "DB"
    temp_folder = "FASTA"
    dataset_small_folder = "DataModel/small/CasPedia"
    dataset_big_folder = "DataModel/big/CasPedia"

    # Create destination directories if they don't exist
    Path(f"../{dataset_small_folder}").mkdir(parents=True, exist_ok=True)
    Path(f"../{dataset_big_folder}").mkdir(parents=True, exist_ok=True)

    # =============================================================================
    # SECTION 2: MERGE MULTIPLE FASTA FILES
    # =============================================================================
    if(True):
        print("\nMERGE_FASTA")
        
        # This section merges different FASTA files from a specified folder.
        # Can process files from a single folder or include all subfolders recursively.
        # All files with the specified ending will be combined into one output file.

        input_folder = f"../{data_folder}/CasPedia/2_CasPedia_tblastn_blasted"
        output_file = f"../{temp_folder}/CasPedia/4_MERGED/merged_tblastn_CasPedia.fasta"
        
        input_folder_2 = f"../{data_folder}/CasPedia/3_CasPedia_local_blastp_blasted"
        output_file_2 = f"../{temp_folder}/CasPedia/4_MERGED/merged_blastp_CasPedia.fasta"

        # File extension to look for in the containing folder (e.g.: .fa, .faa, .fasta)
        ending = "fasta"
        use_subfolders = False  # Set to True to include files from subdirectories

        # Merge all FASTA files with specified ending into one file
        if use_subfolders:
            merge_fasta.merge_fasta_files_all_dict(Path(input_folder), Path(output_file), ending)
        else:
            merge_fasta.merge_fasta_files_current_dir(Path(input_folder), Path(output_file), ending)
            merge_fasta.merge_fasta_files_current_dir(Path(input_folder_2), Path(output_file_2), ending)
        print(f"Merged FASTA files saved to {output_file}")

    # =============================================================================
    # SECTION 2: TRANSLATE OLD NAMES OF CAS14 TO CAS12f
    # =============================================================================
    if True:
        print("\nTRANSLATE FASTA")

        input_file = Path(f"../{data_folder}/CasPedia/1_raw/phylogeny_type5.faa")
        output_file = Path(f"../{temp_folder}/CasPedia/5_TRANSLATED/translated_casPedia.fasta")

        input_file_2 = Path(f"../{temp_folder}/CasPedia/4_MERGED/merged_blastp_CasPedia.fasta")
        output_file_2 = Path(f"../{temp_folder}/CasPedia/5_TRANSLATED/translated_blastp_casPedia.fasta")

        input_file_3 = Path(f"../{temp_folder}/CasPedia/4_MERGED/merged_tblastn_CasPedia.fasta")
        output_file_3 = Path(f"../{temp_folder}/CasPedia/5_TRANSLATED/translated_tblastn_casPedia.fasta")

        cas_translator.translator(input_file, output_file)
        cas_translator.translator(input_file_2, output_file_2)
        cas_translator.translator(input_file_3, output_file_3)

    # =============================================================================
    # SECTION 3: FORMAT SPECIFIC FASTA FILE
    # =============================================================================
    if True:
        print("\nFORMAT_FASTA")
        
        # This section formats a specific FASTA file for standardization.
        # It is used to unify different FASTA files for proper comparability 
        # and adds a subtype appendix to the header for later recognition.
        # The sequence lines are also wrapped to a specified line length.

        input_file = Path(f"../{temp_folder}/CasPedia/5_TRANSLATED/translated_casPedia.fasta")
        output_file = Path(f"../{temp_folder}/CasPedia/6_FORMATTED/formatted_casPedia.fasta")

        input_file_2 = Path(f"../{temp_folder}/CasPedia/5_TRANSLATED/translated_blastp_casPedia.fasta")
        output_file_2 = Path(f"../{temp_folder}/CasPedia/6_FORMATTED/formatted_blastp_casPedia.fasta")

        input_file_3 = Path(f"../{temp_folder}/CasPedia/5_TRANSLATED/translated_tblastn_casPedia.fasta")
        output_file_3 = Path(f"../{temp_folder}/CasPedia/6_FORMATTED/formatted_tblastn_casPedia.fasta")
        
        appendix = "|CasPedia"  # Subtype information added to each header
        line_length = 60  # Maximum characters per sequence line

        # Format the FASTA file with specified parameters
        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file}")

        appendix = "|blastp_CasPedia"
        format_fasta.format_fasta(input_file_2, output_file_2, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file_2}")

        appendix = "|tblastn_CasPedia"
        format_fasta.format_fasta(input_file_3, output_file_3, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file_3}")

    # =============================================================================
    # SECTION 4: UNIFY HEADERS
    # =============================================================================
    if True:
        print("\nUNIFY HEADERS")

        input_folder = f"../{temp_folder}/CasPedia/6_FORMATTED"

        input_file = Path(f"{input_folder}/formatted_casPedia.fasta")
        output_file = Path(f"../{dataset_small_folder}/CasPedia.fasta")

        input_file_2 = Path(f"{input_folder}/formatted_blastp_casPedia.fasta")
        output_file_2 = Path(f"../{dataset_small_folder}/blastp_CasPedia.fasta")

        input_file_3 = Path(f"{input_folder}/formatted_tblastn_casPedia.fasta")
        output_file_3 = Path(f"../{dataset_small_folder}/tblastn_CasPedia.fasta")

        annotate_CasPedia.annotate_CasPedia(input_file, output_file)
        annotate_CasPedia.annotate_CasPedia(input_file_2, output_file_2)
        annotate_CasPedia.annotate_CasPedia(input_file_3, output_file_3)

        source = f"../{dataset_small_folder}/CasPedia.fasta"
        destination = f"../{dataset_big_folder}/CasPedia.fasta"

        source_2 = f"../{dataset_small_folder}/blastp_CasPedia.fasta"
        destination_2 = f"../{dataset_big_folder}/blastp_CasPedia.fasta"

        source_3 = f"../{dataset_small_folder}/tblastn_CasPedia.fasta"
        destination_3 = f"../{dataset_big_folder}/tblastn_CasPedia.fasta"

        shutil.copy(source, destination)
        shutil.copy(source_2, destination_2)
        shutil.copy(source_3, destination_3)

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