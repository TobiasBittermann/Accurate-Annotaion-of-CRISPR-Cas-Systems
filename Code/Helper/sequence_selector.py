import subprocess
import os
import logging
from datetime import datetime

input_folder = "../DataModel/small/checks/sorted_fasta_small"
# Input file with 13000 sequences in FASTA format
input_fasta = f"{input_folder}/cas12m.fasta"
# Output file for reduced set
output_fasta = f"{input_folder}/cas12m_subset.fasta"

def setup_logging():
    # Create LOG directory if it doesn't exist
    log_dir = "../LOG"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}/sequence_selector_{timestamp}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logging.info(f"Started sequence selector - Log: {log_filename}")

def count_sequences_in_fasta(fasta_file):
    """Count the number of sequences in a FASTA file"""
    if not os.path.exists(fasta_file):
        return 0
    
    count = 0
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                count += 1
    return count

def reduce_sequences(input_file, output_file):
    logging.info(f"Processing: {input_file}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        logging.error(f"Input file '{input_file}' not found!")
        return False
    
    # Count input sequences
    input_seq_count = count_sequences_in_fasta(input_file)
    logging.info(f"Input sequences: {input_seq_count}")
    
    # CD-HIT command - higher -c value for fewer sequences
    cmd = [
        "cd-hit",
        "-i", input_file,
        "-o", output_file,
        "-c", "0.5",
        "-n", "2",
        "-M", "16000",
        "-T", "4"
    ]
    
    logging.info("Running CD-HIT clustering...")
    
    # Execute CD-HIT
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        # Count output sequences
        output_seq_count = count_sequences_in_fasta(output_file)
        
        # Delete cluster file (.clstr)
        cluster_file = f"{output_file}.clstr"
        if os.path.exists(cluster_file):
            os.remove(cluster_file)
            logging.info("Cluster file removed")
        
        # Final summary
        reduction_pct = ((input_seq_count - output_seq_count) / input_seq_count) * 100
        logging.info(f"Sequence reduction completed: {input_seq_count} → {output_seq_count} sequences ({reduction_pct:.1f}% reduction)")
        logging.info(f"Output saved to: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"CD-HIT failed: {e}")
        return False
    except FileNotFoundError:
        logging.error("CD-HIT not found! Is it installed and in PATH?")
        return False

if __name__ == "__main__":
    setup_logging()
    success = reduce_sequences(input_fasta, output_fasta)
    
    if success:
        logging.info("Script completed successfully")
    else:
        logging.error("Script failed")
