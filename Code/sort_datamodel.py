import re
from collections import defaultdict
from pathlib import Path

def sort_fasta_by_subtype(input_fasta_path, output_dir_path):
    """
    Sorts sequences from a FASTA file by subtype and writes separate files for each subtype.
    
    Args:
        input_fasta_path (str or Path): Path to the input FASTA file.
        output_dir_path (str or Path): Path to the output directory.
    """
    input_fasta = Path(input_fasta_path)
    output_dir = Path(output_dir_path)
    output_dir.mkdir(exist_ok=True)

    subtype_dict = defaultdict(list)

    with input_fasta.open("r") as infile:
        header = None
        seq_lines = []
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                if header and seq_lines:
                    match = re.search(r"\|([^|]+)\|", header)
                    if match:
                        subtype = match.group(1).lower()
                        subtype_dict[subtype].append((header, "".join(seq_lines)))
                header = line
                seq_lines = []
            else:
                seq_lines.append(line)
        if header and seq_lines:
            match = re.search(r"\|([^|]+)\|", header)
            if match:
                subtype = match.group(1).lower()
                subtype_dict[subtype].append((header, "".join(seq_lines)))

    for subtype, entries in subtype_dict.items():
        out_path = output_dir / f"{subtype}.fasta"
        with out_path.open("w") as out_f:
            for header, seq in entries:
                out_f.write(f"{header}\n{seq}\n")