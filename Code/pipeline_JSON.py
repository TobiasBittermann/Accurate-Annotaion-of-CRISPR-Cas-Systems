#!/usr/bin/env python3

import format_fasta
import merge_fasta
import filter_JSON
import json_to_fasta
import filter_JSON_FASTA
import annotate_CRISPRCas_Atlas
from pathlib import Path
import time

def main():
    """
    Main function to run all filtering and formatting operations.
    Processes CRISPR Cas Atlas database, formats FASTA files, and merges multiple files.
    """
    start_time = time.time()

    data_folder = "DB"
    temp_folder = "FASTA"
    dataset_small_folder = "DataModel/small"
    dataset_big_folder = "DataModel/big"

    # =============================================================================
    # SECTION 1: FILTER JSON FILE
    # =============================================================================
    if(True):
        print("FILTER_JSON")
        
        # This section filters a JSON file to extract relevant Type V CRISPR-Cas information.
        # It reads the input JSON, processes it according to specific criteria,
        # and writes the filtered data to an output file for further analysis.
        
        # Define input and output file paths for JSON filtering
        file_name = "crispr-cas-atlas-v1.0.json"
        filter_prefix = "Type_V_filtered_"
        input_file = f"../{data_folder}/CRISPR-Cas_Atlas/{file_name}"
        output_file = f"../{temp_folder}/CRISPR-Cas_Atlas/{filter_prefix}{file_name}"
        
        # Filter the JSON file using the filter_JSON function
        # This extracts only Type V CRISPR-Cas systems from the complete atlas
        filter_JSON.filter_json_by_subtype_v(input_file, output_file)
        print(f"Filtered JSON file saved to {output_file}")

    # =============================================================================
    # SECTION 2: CONVERT JSON TO FASTA FILES
    # =============================================================================
    if(True):
        print("\nJSON_TO_FASTA")
        
        # This section converts the filtered JSON file to FASTA format.
        # It extracts protein sequences from the JSON data and creates separate
        # FASTA files for different Cas proteins or combined files as needed.
        
        # Define input and output paths for JSON to FASTA conversion
        input_json = f"../{temp_folder}/CRISPR-Cas_Atlas/Type_V_filtered_crispr-cas-atlas-v1.0.json"
        output_folder = f"../{temp_folder}/CRISPR-Cas_Atlas/1_FASTA/"
        
        # Convert JSON to FASTA files using the json_to_fasta function
        # This creates FASTA files from the filtered JSON data
        json_to_fasta.json_to_fasta_simple(input_json, output_folder)
        print(f"FASTA files created in {output_folder}")

    # =============================================================================
    # SECTION 3: MERGE MULTIPLE FASTA FILES
    # =============================================================================
    if(True):
        print("\nMERGE_FASTA")
        
        # This section merges different FASTA files from a specified folder.
        # Can process files from a single folder or include all subfolders recursively.
        # All files with the specified ending will be combined into one output file.

        input_folder = f"../{temp_folder}/CRISPR-Cas_Atlas/1_FASTA"
        output_file = f"../{temp_folder}/CRISPR-Cas_Atlas/2_FASTA_PROCESSED/merged_CRISPR-Cas_Atlas.fasta"
        # File extension to look for in the containing folder (e.g.: .fa, .faa, .fasta)
        ending = "fasta"
        use_subfolders = False  # Set to True to include files from subdirectories

        # Merge all FASTA files with specified ending into one file
        if use_subfolders:
            merge_fasta.merge_fasta_files_all_dict(Path(input_folder), Path(output_file), ending)
        else:
            merge_fasta.merge_fasta_files_current_dir(Path(input_folder), Path(output_file), ending)
        print(f"Merged FASTA files saved to {output_file}")


    # =============================================================================
    # SECTION 4: FILTER FASTA BY KEYWORD
    # =============================================================================
    if(True):
        print("\nFILTER_JSON_FASTA")
        
        # This section filters a FASTA file to extract sequences whose headers contain
        # a specific keyword. It performs case-insensitive search and writes only
        # matching sequences (header + sequence data) to the output file.
        # This is useful for isolating specific protein families or types.

        input_file = Path(f"../{temp_folder}/CRISPR-Cas_Atlas/2_FASTA_PROCESSED/merged_CRISPR-Cas_Atlas.fasta")
        output_file = Path(f"../{temp_folder}/CRISPR-Cas_Atlas/2_FASTA_PROCESSED/filtered_CRISPR-Cas_Atlas.fasta")
        keyword = "cas12"  # Keyword to search for in sequence headers (case-insensitive)

        # Filter the FASTA file using the filter_JSON_FASTA function
        # This extracts only sequences containing the specified keyword in their headers
        filter_JSON_FASTA.filter_JSON_FASTA(input_file, output_file, keyword)
        print(f"Filtered FASTA file saved to {output_file}")

    # =============================================================================
    # SECTION 5: FORMAT SPECIFIC FASTA FILE
    # =============================================================================
    if(True):
        print("\nFORMAT_FASTA")
        
        # This section formats a specific FASTA file for standardization.
        # It is used to unify different FASTA files for proper comparability 
        # and adds a subtype appendix to the header for later recognition.
        # The sequence lines are also wrapped to a specified line length.

        # Small DataModel
        input_file = Path(f"../{temp_folder}/CRISPR-Cas_Atlas/2_FASTA_PROCESSED/filtered_CRISPR-Cas_Atlas.fasta")
        output_file = Path(f"../{temp_folder}/CRISPR-Cas_Atlas/3.1_FASTA_FORMATTED/formatted_CRISPR-Cas_Atlas.fasta")
        appendix = ""  # Subtype information added to each header
        line_length = 60  # Maximum characters per sequence line

        # Format the FASTA file with specified parameters
        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file}")

        # Big DataModel
        input_file = Path(f"../{temp_folder}/CRISPR-Cas_Atlas/2_FASTA_PROCESSED/merged_CRISPR-Cas_Atlas.fasta")
        output_file = Path(f"../{temp_folder}/CRISPR-Cas_Atlas/3.2_FASTA_FORMATTED/formatted_CRISPR-Cas_Atlas.fasta")
        appendix = ""  # Subtype information added to each header
        line_length = 60  # Maximum characters per sequence line

        # Format the FASTA file with specified parameters
        format_fasta.format_fasta(input_file, output_file, appendix, line_length)
        print(f"Formatted FASTA file saved to {output_file}")

    # =============================================================================
    # SECTION 6: UNIFY HEADER
    # =============================================================================
    if(True):
        print("\nUNIFY_HEADER")

        # Small DataModel
        # Define input file path
        fasta_folder = f"../{temp_folder}/CRISPR-Cas_Atlas/3.1_FASTA_FORMATTED"

        file_counter = 1
        for fasta_file in Path(fasta_folder).glob("*.fasta"):
            output_file = f"../{dataset_small_folder}/CRISPR-Cas_Atlas/CRISPR-Cas_Atlas_{file_counter}.fasta"
            annotate_CRISPRCas_Atlas.annotate_crispr_cas_atlas(fasta_file, output_file)
            file_counter += 1
        print(f"Unified file saved to {output_file}.")

        # Big DataModel
        fasta_folder = f"../{temp_folder}/CRISPR-Cas_Atlas/3.2_FASTA_FORMATTED"

        file_counter = 1
        for fasta_file in Path(fasta_folder).glob("*.fasta"):
            output_file = f"../{dataset_big_folder}/CRISPR-Cas_Atlas/CRISPR-Cas_Atlas_{file_counter}.fasta"
            annotate_CRISPRCas_Atlas.annotate_crispr_cas_atlas(fasta_file, output_file)
            file_counter += 1

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