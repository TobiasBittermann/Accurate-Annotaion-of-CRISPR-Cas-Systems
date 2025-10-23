import os
import time
import random
from pathlib import Path
from Bio import SeqIO
from Bio.Blast import NCBIWWW, NCBIXML
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Lock to ensure only one thread accesses BLAST web service at a time
blast_lock = Lock()

def run_blast_and_filter(record):
    """
    Run a tBLASTn search for the given protein sequence record, 
    then filter the results for high-scoring hits.
    Skips records with empty BLAST results.
    """ 
    with blast_lock:
        print(f"Starting BLASTp for {record.id}...")

        # Random pause between 3–5 seconds to avoid overloading the NCBI server
        time.sleep(random.uniform(3.0, 5.0))

        # Submit tBLASTn query to NCBI
        try:
            result_handle = NCBIWWW.qblast("tblastn", "nt", record.seq, format_type="XML")
            blast_record = NCBIXML.read(result_handle)
        except Exception as e:
            print(f"Error for {record.id}: {e}")
            return record.id, [], []

        print(f"BLAST completed for {record.id}.")

    high_score_hits = []

    # Fehlerbehandlung: Wenn keine Alignments vorhanden sind, skippen
    if not getattr(blast_record, "alignments", None) or len(blast_record.alignments) == 0:
        print(f"No BLAST hits for {record.id}, skipping.")
        return record.id, [], []  # Leere Listen zurückgeben

    for alignment in blast_record.alignments:
        for hsp in alignment.hsps:
            align_length = hsp.align_length
            identity = hsp.identities
            percent_identity = (identity / align_length) * 100
            score = hsp.score
            e_value = hsp.expect

            hit = {
                "title": alignment.title,
                "sequence": hsp.sbjct,
                "identity": identity,
                "percent_identity": percent_identity, 
                "alignment_length": align_length,
                "score": score,
                "e-value": e_value
            }

            if percent_identity >= 80:
                high_score_hits.append(hit)

    return record.id, [], high_score_hits  # Cas12 hits are now always empty

def save_to_fasta(hits, filename):
    """
    Save the filtered hits as a FASTA file with appropriate metadata in the description.
    """
    records = [
        SeqRecord(
            Seq(hit["sequence"]),
            id=f"hit_{i+1}",
            description=f"{hit['title']} | Identity: {hit['identity']:.2f} | Identity Percentage: {hit['percent_identity']:.2f}% | Alignment_length: {hit['alignment_length']} | Score: {hit['score']} | E-value: {hit['e-value']:.2e}"
        )
        for i, hit in enumerate(hits)
    ]
    SeqIO.write(records, filename, "fasta")

def process_fasta_file_parallel(fasta_path):
    """
    Process a given FASTA file:
    Run BLAST searches in parallel for each sequence record,
    then save the filtered high-score hits to a FASTA file.
    Additionally, remove empty result files and log processed headers.
    """
    print(f"\nProcessing file: {fasta_path}")
    output_dir = Path(f"../results/blast_results") / Path(fasta_path).stem
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    records = list(SeqIO.parse(fasta_path, "fasta"))
    log_file = "../processed_headers.txt"

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(run_blast_and_filter, record) for record in records]

        for future in as_completed(futures):
            record_id, cas12_hits, high_score_hits = future.result()
            fasta_file = output_dir / f"{record_id}_high_score_hits.fasta"
            save_to_fasta(high_score_hits, fasta_file)
            if os.path.exists(fasta_file) and os.path.getsize(fasta_file) == 0:
                os.remove(fasta_file)
                print(f"Deleted empty file: {fasta_file}")
            else:
                print(f" {len(high_score_hits)} High-score hits saved for {record_id}")
            with open(log_file, "a", encoding="utf-8") as log:
                log.write(f"{record_id}\n")

if __name__ == "__main__":
    start_time = time.time()
    fasta_folder = "../DB/CasPedia/"

    for fasta_file in Path(fasta_folder).glob("*.faa"):
        process_fasta_file_parallel(fasta_file)

    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Finished! Total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
