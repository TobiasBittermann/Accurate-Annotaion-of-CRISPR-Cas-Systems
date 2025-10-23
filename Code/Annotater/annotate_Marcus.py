import time
from pathlib import Path

def annotate_marcus_fasta(input_file, output_file):
    """
    Process a FASTA file and convert Marcus-style headers.
    
    Args:
        input_file (str): Path to input FASTA file
        output_file (str): Path to output FASTA file
    """

    input_file = Path(input_file)
    output_file = Path(output_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.touch(exist_ok=True)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            
            if line.startswith('>'):
                # Parse the header line
                # Expected format: >WP_106260488.1 | subtype=cas12k
                
                # Split by ' | subtype=' to get accession and subtype
                if ' | subtype=' in line:
                    parts = line.split(' | subtype=')
                    accession = parts[0][1:]  # Remove the '>' character
                    subtype = parts[1]
                    
                    # Create new header format: >accession|subtype|Marcus
                    new_header = f">{accession}|{subtype}|Marcus"
                    outfile.write(new_header + '\n')
                else:
                    # If header doesn't match expected format, keep original
                    print(f"Warning: Header doesn't match expected format: {line}")
                    outfile.write(line + '\n')
            else:
                # Write sequence lines unchanged
                outfile.write(line + '\n')


if __name__ == "__main__":
    # Record start time for performance tracking
    start_time = time.time()

    # Define input file path
    fasta_folder = "../DB/Marcus_File/FASTA_FORMATTED"
    fasta_file = f"{fasta_folder}/marcus_file_formatted.fasta"
    output_file=f"../FASTA/Marcus_File/marcus_annotated.fasta"

    if(False):
        for fasta_file in Path(fasta_folder).glob("*.fasta"):
            annotate_marcus_fasta(fasta_file, output_file)
    else:
        annotate_marcus_fasta(fasta_file, output_file)

    # Calculate and display execution time
    end_time = time.time()
    elapsed_time = int(end_time - start_time)

    # Format elapsed time as hh:mm:ss
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Print execution summary
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print (f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")