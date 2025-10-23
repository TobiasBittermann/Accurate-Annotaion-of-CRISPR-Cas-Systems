import time
from pathlib import Path

def filter_JSON_FASTA(input_file, output_file, keyword="cas12"):
    """
    Filter a FASTA file to extract sequences whose headers contain a specific keyword.
    
    Args:
        input_file (str): Path to the input FASTA file
        output_file (str): Path to the output FASTA file
        keyword (str): Keyword to search for in sequence headers (case-insensitive)
    """

    # Convert file paths to Path objects for better path handling
    input_path = Path(input_file)
    output_path = Path(output_file)
    
    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Open input and output files simultaneously
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        write_entry = False  # Flag to track whether current sequence should be written

        for line in infile:
            # Check if line is a FASTA header (starts with '>')
            if line.startswith('>'):
                # Check if header contains the keyword (case-insensitive search)
                if keyword in line.lower():
                    write_entry = True
                    outfile.write(line)  # Write the matching header
                else:
                    write_entry = False  # Reset flag for non-matching headers
            # Write sequence lines only if the header matched
            elif write_entry:
                outfile.write(line)

if __name__ == "__main__":
    start_time = time.time()

    input_file = f""
    output_file = f""
    keyword = "cas12"

    filter_JSON_FASTA(input_file, output_file, keyword)

    end_time = time.time()

    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print (f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")