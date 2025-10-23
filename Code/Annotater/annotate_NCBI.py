import time
from pathlib import Path
import pandas as pd
from Bio import SeqIO

def load_subtype_mapping(csv_path):
    dataframe = pd.read_csv(csv_path)
    mapping = {}
    for _, row in dataframe.iterrows():
        accession = str(row.iloc[0])
        subtype_raw = str(row.iloc[6])
        subtype_mapped = detect_cas_subtype(subtype_raw)
        mapping[accession] = subtype_mapped
    return mapping

def extract_accession_number(sequence_id: str) -> str:
    """
    Extracts the accession number from a sequence ID.
    Example: AE000511_330588_330872 -> AE000511
    """
    # Takes everything before the first underscore
    return sequence_id.split('_')[0]

def detect_cas_subtype(title: str) -> str:
    """
    Maps cas subtypes. Source: Classification and Nomenclature of CRISPR-Cas Systems: Where from Here?
    """
    cas12_map = {
    "CAS-V-A": "Cas12a",
    "CAS-V-B": "Cas12b",
    "CAS-V-C": "Cas12c",
    "CAS-V-D": "Cas12d",
    "CAS-V-E": "Cas12e",
    "CAS-V-F": "Cas12f"
}
    if title in cas12_map:
        return cas12_map[title]
    else:
        return "Unknown"

def process_fasta_file(fasta_file, csv_file, output_dir):
    """"""
    print(f"\nProcessing file: {fasta_file}")
    print(f"Using {csv_file} for mapping.")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    subtype_mapping= load_subtype_mapping(csv_file)
    print(f"Loaded {len(subtype_mapping)} entries from {csv_file}")

    records = list(SeqIO.parse(fasta_file, "fasta"))
    output_file = output_dir / (Path(fasta_file).stem + "_subtyped.fasta")

    annotated_records = []

    for record in records:
        accession = extract_accession_number(record.id)

        if accession in subtype_mapping:
            subtype = subtype_mapping[accession]
            print(f"Found {accession} -> {subtype}")
        else:
            subtype = "NotFound"
            print(f"Accession {accession} not found in CSV")

        record.id = f"{accession}|{subtype}|NCBI"
        record.description = ""
        annotated_records.append(record)

    SeqIO.write(annotated_records, output_file, "fasta")
    print(f"Annotated FASTA saved: {output_file}")

if __name__ == "__main__":
    # Record start time for performance tracking
    start_time = time.time()

    # Define input file path
    fasta_folder = "../DB/NCBI/NCBI_Filtered/"
    fasta_file = f"{fasta_folder}AE000511(Copy).faa"
    csv_file = "../DB/NCBI/Complete_Cassette_summary.csv"
    output_dir=f"../DB/NCBI/NCBI_subtyped/"

    for fasta_file in Path(fasta_folder).glob("*.faa"):
        process_fasta_file(fasta_file, csv_file, output_dir)

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