#!/usr/bin/env python3

import subprocess
import shutil
import sys
import os
import time
import logging
from pathlib import Path

# Ensure log directory exists before setting up logging
Path("../LOG/").mkdir(parents=True, exist_ok=True)

# Setup logging
logfile = "../LOG/create_hmm.log"
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

def create_hmm_from_alignment(aln_file, hmm_file, model_name=None):
    """
    Creates an HMM profile file from a Multiple Sequence Alignment file using hmmbuild.
    
    Args:
        aln_file (str): Path to input alignment file (.aln)
        hmm_file (str): Path to output HMM file (.hmm)
        model_name (str, optional): Name for the HMM model. If None, uses filename.
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    if shutil.which("hmmbuild") is None:
        logging.error("HMMER tool 'hmmbuild' is not installed or not in PATH.")
        return False
    
    if not os.path.exists(aln_file):
        logging.error(f"Alignment file {aln_file} does not exist.")
        return False
    
    try:
        if model_name is None:
            model_name = os.path.splitext(os.path.basename(aln_file))[0]
        
        cmd = ["hmmbuild", "-n", model_name, hmm_file, aln_file]
        
        logging.info(f"Running hmmbuild for {aln_file}")
        
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        logging.info(f"HMM profile successfully created: {hmm_file}")
        
        if result.stderr:
            logging.debug(f"HMMER output: {result.stderr}")
            
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running hmmbuild for {aln_file}: {e.stderr}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error processing {aln_file}: {e}")
        return False

def batch_create_hmm_profiles(alignment_dir, hmm_output_dir):
    """
    Creates HMM profiles for all .aln files in a directory using hmmbuild.
    
    Args:
        alignment_dir (Path): Directory containing .aln files
        hmm_output_dir (Path): Output directory for .hmm files
    """
    
    hmm_output_dir.mkdir(parents=True, exist_ok=True)
    
    aln_files = list(alignment_dir.glob("**/*.aln"))
    
    if not aln_files:
        logging.warning(f"No .aln files found in {alignment_dir}.")
        return
    
    logging.info(f"Found {len(aln_files)} alignment files")
    
    start_total = time.time()
    success_count = 0
    
    for aln_file in aln_files:
        start_file = time.time()
        hmm_file = hmm_output_dir / f"{aln_file.stem}.hmm"
        
        if create_hmm_from_alignment(str(aln_file), str(hmm_file)):
            success_count += 1
        
        end_file = time.time()
        logging.info(f"Processed {aln_file.name} in {end_file - start_file:.2f} seconds")
    
    end_total = time.time()
    logging.info(f"Successfully created {success_count}/{len(aln_files)} HMM profiles")
    logging.info(f"Total processing time: {end_total - start_total:.2f} seconds")

if __name__ == "__main__":
    alignment_dir = Path("../PHYLOTREE/")
    hmm_output_dir = Path("../HMM_PROFILES/")
    
    batch_create_hmm_profiles(alignment_dir, hmm_output_dir)

