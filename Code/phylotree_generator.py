import shutil
import subprocess
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from Bio import Phylo, AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import matplotlib.pyplot as plt
import os
import logging
from Bio import SeqIO

Path("../LOG/").mkdir(parents=True, exist_ok=True)

logfile = "../LOG/phylotree_generator.log"
logging.basicConfig(
    filename=logfile,
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def run_msa(input_faa, aln_file, threads=4):
    """
    Execute multiple sequence alignment using MUSCLE on a FASTA file.
    
    Args:
        input_faa (str): Path to the input FASTA file containing sequences to align
        aln_file (str): Path where the aligned sequences will be saved
        threads (int, optional): Number of CPU threads for MUSCLE to use. Defaults to 4.
    
    Returns:
        bool: True if MUSCLE alignment completed successfully, False otherwise
    """
    if shutil.which("muscle") is None:
        logging.error("MUSCLE is not installed or not in path.")
        return False
    logging.info(f"Running MUSCLE for {input_faa} with {threads} thread(s).")
    
    result = subprocess.run(
        ["muscle", "-align", input_faa, "-output", aln_file, "-threads", str(threads)],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        logging.error(f"Error running MUSCLE for {input_faa}: {result.stderr}")
        return False
    logging.info(f"MUSCLE finished for {input_faa}. Output: {aln_file}")
    return True

def process_fasta(fasta_file, output_folder, threads):
    """
    Process a single FASTA file through the complete phylogenetic analysis pipeline.
    
    This function performs multiple sequence alignment, constructs a phylogenetic tree
    using neighbor-joining algorithm, and generates both Newick and SVG output files.
    
    Args:
        fasta_file (Path): Path object pointing to the input FASTA file
        output_folder (Path): Directory where output subfolders will be created
        threads (int): Number of threads to use for MSA processing
    
    Returns:
        tuple: A tuple containing (filename, processing_duration_seconds) where
               processing_duration_seconds is None if processing failed
    """
    seqs = list(SeqIO.parse(fasta_file, "fasta"))
    if len(seqs) < 2:
        logging.warning(f"{fasta_file} enthält weniger als 2 Sequenzen. Überspringe Datei.")
        return fasta_file.name, None
    
    MAX_SEQUENCES = 1500
    if len(seqs) > MAX_SEQUENCES:
        logging.warning(f"{fasta_file} enthält {len(seqs)} Sequenzen (>{MAX_SEQUENCES}). Das könnte zu Speicherproblemen führen. Überspringe Datei.")
        return fasta_file.name, None

    start_file = time.time()
    
    file_output_folder = output_folder / fasta_file.stem
    file_output_folder.mkdir(parents=True, exist_ok=True)

    aligned_file = file_output_folder / f"{fasta_file.stem}.aln"
    tree_file = file_output_folder / f"{fasta_file.stem}.nwk"
    svg_file = file_output_folder / f"{fasta_file.stem}.svg"

    logging.info(f"Processing {fasta_file}...")

    if not run_msa(str(fasta_file), str(aligned_file), threads):
        logging.error(f"MSA failed for {fasta_file}")
        return fasta_file.name, None

    try:
        alignment = AlignIO.read(aligned_file, "fasta")
        logging.info(f"Alignment read for {fasta_file} ({len(alignment)} sequences).")
    except Exception as e:
        logging.error(f"Error reading alignment for {fasta_file}: {e}")
        return fasta_file.name, None

    try:
        calculator = DistanceCalculator('identity')
        dm = calculator.get_distance(alignment)
        logging.info(f"Distance matrix calculated for {fasta_file}.")
        
        constructor = DistanceTreeConstructor()
        tree = constructor.nj(dm)
        
        Phylo.write(tree, tree_file, "newick")
        logging.info(f"Tree written to {tree_file}.")
    except Exception as e:
        logging.error(f"Error constructing tree for {fasta_file}: {e}")
        return fasta_file.name, None

    try:
        num_seqs = len(alignment)
        MAX_PLOT_SIZE = 50
        
        width = min(max(10, num_seqs * 0.3), MAX_PLOT_SIZE)
        height = min(max(10, num_seqs * 0.3), MAX_PLOT_SIZE)
        
        logging.info(f"Creating plot for {num_seqs} sequences with size {width}x{height} inches")
        
        fig = plt.figure(figsize=(width, height))
        axes = fig.add_subplot(1, 1, 1)
        
        Phylo.draw(tree, do_show=False, axes=axes)
        
        fig.savefig(svg_file, format="svg", dpi=100)
        plt.close(fig)
        
        plt.clf()
        plt.cla()
        logging.info(f"SVG tree plot saved to {svg_file}.")
    except Exception as e:
        logging.error(f"Error plotting tree for {fasta_file}: {e}")
        return fasta_file.name, None

    end_file = time.time()
    duration = end_file - start_file
    logging.info(f"Finished processing {fasta_file} in {print_time(duration)}.")
    return fasta_file.name, duration

def print_time(seconds):
    """
    Format a duration in seconds into a human-readable time string.
    
    Args:
        seconds (float): Duration in seconds to format
    
    Returns:
        str: Formatted time string in "X min Y.YY s" format, or "Y.YY s" if less than a minute
    """
    mins, secs = divmod(seconds, 60)
    return f"{int(mins)} min {secs:.2f} s" if mins else f"{secs:.2f} s"

submodel = "checks/sorted_fasta_small"
fasta_folder = Path(f"../DataModel/small/{submodel}")
output_folder = Path(f"../PHYLOTREE/")
output_folder.mkdir(parents=True, exist_ok=True)

start_total = time.time()

fasta_files = list(fasta_folder.rglob("*.fasta"))

max_workers = min(os.cpu_count() or 4, 4)
muscle_threads = max(1, (os.cpu_count() or 4) // max_workers)

logging.info(f"Starting processing of {len(fasta_files)} FASTA files with {max_workers} workers and {muscle_threads} MUSCLE thread(s) per file.")

with ProcessPoolExecutor(max_workers=max_workers) as executor:
    futures = [
        executor.submit(process_fasta, fasta_file, output_folder, muscle_threads)
        for fasta_file in fasta_files
    ]
    
    for future in as_completed(futures):
        name, duration = future.result()
        if duration is not None:
            msg = f"{name}: {print_time(duration)}"
            print(msg)
            logging.info(msg)
        else:
            msg = f"{name}: Error during processing."
            print(msg)
            logging.error(msg)

end_total = time.time()
logging.info(f"Total runtime: {print_time(end_total - start_total)}")
print(f"\nTotal runtime: {print_time(end_total - start_total)}")