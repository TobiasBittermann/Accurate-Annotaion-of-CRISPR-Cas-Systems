#!/usr/bin/env python3

import time
import subprocess
import csv
from pathlib import Path
from collections import defaultdict

def run_blastp(query_fasta: Path, db_path: Path, output_csv: Path, e_value: float = 1e-5, num_threads: int = 8):
    """
    Runs BLASTP and writes all results to a temporary CSV file.
    The output format is CSV (outfmt 10) with all relevant columns including the subject sequence.
    """
    cmd = [
        "blastp",
        "-query", str(query_fasta),
        "-db", str(db_path),
        "-out", str(output_csv),
        "-evalue", str(e_value),
        "-num_threads", str(num_threads),
        "-outfmt", "10 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen sseq"
    ]
    print("Running BLASTP command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print("BLASTP finished.")

def parse_blast_results_csv(tmp_output: Path, identity_threshold: float = 80.0):
    """
    Parses the BLASTP CSV results and returns a dictionary of hits per query.
    Only hits with percent identity (identities/query length) >= identity_threshold are kept.
    The FASTA header is constructed with column names for clarity.
    """
    hits_per_query = defaultdict(list)
    header_names = [
        "query_sequence_id", "subject_sequence_id", "percent_identity", "alignment_length", "mismatches", "gap_openings",
        "query_start", "query_end", "subject_start", "subject_end", "e_value", "bit_score", "query_length"
    ]
    with tmp_output.open("r", newline='') as infile:
        reader = csv.reader(infile)
        for fields in reader:
            if len(fields) < 14:
                continue  # Skip incomplete lines
            try:
                alignment_length = float(fields[3])
                percent_identity = float(fields[2])
                query_length = float(fields[12])
                # Calculate number of identities
                identities = alignment_length * (percent_identity / 100)
                # Calculate percent identity relative to full query length
                percent_identity_new = (identities / query_length) * 100 if query_length > 0 else 0
                if percent_identity_new >= identity_threshold:
                    query_sequence_id = fields[0]
                    header = "|".join(f"{name}={value}" for name, value in zip(header_names, fields[:13]))
                    sequence = fields[13]
                    hits_per_query[query_sequence_id].append((header, sequence))
            except ValueError:
                continue  # Skip lines with invalid float conversion
    return hits_per_query

def write_fasta_per_query(hits_per_query, output_dir: Path):
    """
    Writes one FASTA file per query sequence with all its hits.
    Each file is named <query_sequence_id>_hits.fasta and contains all hits for that query.
    """
    for query_sequence_id, hits in hits_per_query.items():
        output_fasta = output_dir / f"{query_sequence_id}_hits.fasta"
        with output_fasta.open("w") as out:
            for header, sequence in hits:
                out.write(f">{header}\n{sequence}\n")
    print(f"FASTA files for each query written to {output_dir}")


def main(query_fasta: Path, db_path: Path, output_dir: Path, e_value: float = 1e-5, num_threads: int = 8, identity_threshold: float = 80.0):
    """
    Main workflow:
    - Runs BLASTP
    - Parses and filters results
    - Writes per-query FASTA files
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "blastp_tmp_results.csv"

    # Run BLASTP and collect results
    run_blastp(query_fasta, db_path, output_csv, e_value, num_threads)
    hits_per_query = parse_blast_results_csv(output_csv, identity_threshold)

    # Write one FASTA file per query
    write_fasta_per_query(hits_per_query, output_dir)
    
    # Clean up temporary CSV file
    output_csv.unlink()
    print(f"Temporary file {output_csv} removed.")

if __name__ == "__main__":
    start_time = time.time()

    # Define input and output paths
    query_fasta = Path("../DB/CasPedia/translated_casPedia.fasta")
    db_path = Path("../DB/BLAST_DB/my_blast_db")
    output_dir = Path("../DB/CasPedia/local_blast_fasta")

    # Run the main workflow
    main(query_fasta, db_path, output_dir, e_value=1e-5, num_threads=8, identity_threshold=80.0)

    # Print timing information
    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print(f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")