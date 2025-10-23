from pathlib import Path

def annotate_CasPedia(input_file, output_file):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.touch(exist_ok=True)
    print(f"{output_file} created.")
    accession_number_counter = 1

    with open(output_file, 'w') as outfile, open(input_file, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                header_line = line[1:]  # Entfernt das '>'
                if "subject_sequence_id=" in header_line:
                    parts = header_line.split('|')
                    accession = parts[1].split('=')[1] 
                    gene_name = parts[2].split('=')[1]
                    database =  parts[17]
                elif header_line.startswith('hit'):
                    parts = header_line.split('|')
                    accession = parts[3] 
                    gene_name = "no_gene_name"
                    database = parts[10]
                else:
                    parts = header_line.split('|')
                    accession = "no_accession_number" + str(accession_number_counter)
                    if "TnpB" in header_line:
                        gene_name = "TnpB"
                    else:
                        gene_name = parts[0]
                    database = parts[1]
                    accession_number_counter += 1

                header = f">{accession}|{gene_name}|{database}"
                outfile.write(header)
            else:
                outfile.write(line)

if __name__ == "__main__":
    input_folder = f"../DB/CasPedia/6_FORMATTED"
    output_folder = f"../DB/CasPedia/7_UNIFIED"
    input_file = Path(f"{input_folder}/formatted_tblastn_casPedia.fasta")
    output_file = Path(f"{output_folder}/BlastPCasPedia.fasta")
    print(output_folder)

    annotate_CasPedia(input_file, output_file)