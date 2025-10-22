import time
from pathlib import Path
import re

def annotate_uniprot_fasta(input_file, output_file):

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.touch(exist_ok=True)

    with open(output_file, 'w') as outfile:
            with open(input_file, 'r') as infile:
                for line in infile:
                    line = line.strip()

                    if line.startswith(">"):
                        parts = line.split("|")

                        database = parts[0][1:]
                        accession = parts[1]

                        if "GN=" in line:
                            parts = line.split("GN=")[1]
                            if "cas12" in parts.lower():
                                gene_name = parts.split("|")[0]

                                header = f">{accession}|{gene_name}|uniprot_{database}"
                                outfile.write(header + '\n')
                            else:
                                if "cas12" in line.lower():
                                    match = re.search(r'cas12([a-zA-Z])', line, re.IGNORECASE)
                                    if match:
                                        gene_name = "Cas12" + match.group(1)
                                    else:
                                        gene_name = "Cas12"

                                    header = f">{accession}|{gene_name}|uniprot_{database}"
                                    outfile.write(header + '\n')
                        elif "cas12" in line.lower():
                            match = re.search(r'cas12([a-zA-Z])', line, re.IGNORECASE)
                            if match:
                                gene_name = "Cas12" + match.group(1)
                            else:
                                gene_name = "Cas12"

                            header = f">{accession}|{gene_name}|uniprot_{database}"
                            outfile.write(header + '\n')
                        else:
                            header = f">{accession}|no_subtype_found|uniprot_{database}"
                            outfile.write(header + '\n')
                            print(f"{accession}, subtype not found.")

                    else:
                        outfile.write(line + '\n')

if __name__ == "__main__":
    # Record start time for performance tracking
    start_time = time.time()

    # Define input file path
    fasta_folder = "../FASTA/"
    fasta_file = f"{fasta_folder}/"
    output_file=f"../FASTA/fasta.fasta"

    annotate_uniprot_fasta(fasta_file, output_file)

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