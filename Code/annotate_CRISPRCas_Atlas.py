import time
from pathlib import Path


def annotate_crispr_cas_atlas(input_file, output_file):
    output_file = Path(output_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.touch(exist_ok=True)
    print(f"{output_file} created.")

    with open(output_file, 'w')as outfile:
        print(f"{outfile} opened.")
        #for file in input_file.glob('*.fasta'):

        #for file in input_file:
        print(f"Looking at {input_file}")
        with open(input_file, 'r') as infile:
            print(f"{infile} opened.")
            for line in infile:

                if line.startswith(">"):
                    parts = line.split("|")
                    # accession contains '>' already
                    accession = parts[0]
                    gene_name = parts[1]
                    gene_name = gene_name.split("gene_name=")[1]

                    header = f"{accession}|{gene_name}|CRISPR-Cas_Atlas"
                    outfile.write(header + "\n")
                    
                else:
                    outfile.write(line)


if __name__ == "__main__":
    # Record start time for performance tracking
    start_time = time.time()

    # Define input file path
    fasta_folder = "../DB/CRISPR-Cas_Atlas/3_FASTA_FORMATTED"
    fasta_file = f"{fasta_folder}/formatted_CRISPR-Cas_Atlas.fasta"
    output_file = f"../FASTA/CRISPR-Cas_Atlas/CRISPR-Cas_Atlas.fasta"

    if False:
        for fasta_file in Path(fasta_folder).glob("*.faa"):
            annotate_crispr_cas_atlas(fasta_file, output_file)
    else:
        annotate_crispr_cas_atlas(fasta_file, output_file)

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