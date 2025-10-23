#!/usr/bin/env python3

import time
import os

def filter_uniprot(input_file, output_file, keyword="cas12", keyword2="-like", pe_threshold=5):
    """
    Filters a UniProt FASTA file based on keywords and protein evidence (PE) score.
    
    Args:
        input_file (str): Path to the input UniProt FASTA file
        output_file (str): Path to the output filtered FASTA file
        keyword (str): Primary keyword to search for in headers (default: "cas")
        keyword2 (str): Keyword to exclude from results (default: "-like")
        pe_threshold (int): Maximum PE value to include (default: 5)
    
    The function keeps sequences where:
    - Header contains the primary keyword (case-insensitive)
    - Header does NOT contain the exclusion keyword (case-insensitive)
    - PE value is <= pe_threshold
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        write_entry = False  # Flag to track whether current entry should be written
        
        for line in infile:
            if line.startswith(">"):  # Header line
                # Check if header contains the primary keyword
                if keyword in line.lower():
                    # Exclude entries containing the secondary keyword
                    if keyword2 not in line.lower():
                        # Check for PE value <= threshold
                        pe_check = False
                        line_lower = line.lower()

                        line = line.replace(' ', '|')
                        
                        # Look for PE= in the header
                        if "pe=" in line_lower:
                            try:
                                # Extract PE value from header
                                pe_start = line_lower.find("pe=") + 3
                                pe_end = pe_start
                                # Find the end of the PE number
                                while pe_end < len(line_lower) and line_lower[pe_end].isdigit():
                                    pe_end += 1
                                
                                # Parse PE value if found
                                if pe_end > pe_start:
                                    pe_value = int(line_lower[pe_start:pe_end])
                                    if pe_value <= pe_threshold:
                                        pe_check = True
                            except ValueError:
                                pass  # Skip if PE value cannot be parsed
                        
                        # Write entry if all conditions are met
                        if pe_check:
                            write_entry = True
                            outfile.write(line)
                            print(f"{line.strip()} written.")
                        else:
                            write_entry = False
                    else:
                        write_entry = False  # Skip entries with exclusion keyword
                else:
                    write_entry = False  # Skip entries without primary keyword
            elif write_entry:
                # Write sequence lines for accepted entries
                outfile.write(line)

if __name__ == "__main__":
    start_time = time.time()

    # Process UniProt Trembl database
    name = "uniprot_trembl"
    input_file = f"../DB/uniprot/raw/{name}.fasta"
    output_file = f"../FASTA/uniprot/{name}_filtered.fasta"
    filter_uniprot(input_file, output_file, "cas12", "-like", 5)
    print(f"Filtered UniProt Trembl file saved to {output_file}")

    # Process UniProt Sprot database
    name2 = "uniprot_sprot"
    input_file_2 = f"../DB/uniprot/raw/{name2}.fasta"
    output_file_2 = f"../FASTA/uniprot/{name2}_filtered.fasta"
    filter_uniprot(input_file_2, output_file_2, "cas12", "-like", 5)
    print(f"Filtered UniProt Sprot file saved to {output_file_2}")

    # Calculate and display timing information
    end_time = time.time()
    elapsed_time = int(end_time - start_time)

    # Format elapsed time as hh:mm:ss
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print(f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")