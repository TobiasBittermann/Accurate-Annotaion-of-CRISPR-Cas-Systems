#!/usr/bin/env bash

# ===========================================
# make_blast_db.sh
# Creates a local protein database for BLAST
# ===========================================

# --- Settings: Set your parameters here ---
FASTA_FILE="../DB/CRISPR-Cas_Atlas/FASTA_FORMATTED/complete_CRISPR-Cas_Atlas_formatted.fasta"   # Path to your input FASTA file
DB_NAME="../DB/BLAST_DB/my_blast_db"                                                                     # Name (and path) for the BLAST database

# --- Check if the input FASTA file exists ---
if [[ ! -f "$FASTA_FILE" ]]; then
    echo "Error: FASTA file '$FASTA_FILE' not found."
    exit 1
fi

# --- Check if makeblastdb is installed and available ---
if ! command -v makeblastdb &> /dev/null; then
    echo "'makeblastdb' was not found."
    echo "   Please install BLAST+: conda install -c bioconda blast"
    exit 1
fi

# --- Create the BLAST protein database ---
echo "🔹 Creating BLAST database..."
makeblastdb -in "$FASTA_FILE" -dbtype prot -out "$DB_NAME"

# --- Print success or error message based on the result ---
if [[ $? -eq 0 ]]; then
    echo "BLAST database '$DB_NAME' created successfully."
else
    echo "Error occurred while creating the BLAST database."
    exit 1
fi