

from pathlib import Path
import csv
from datetime import datetime

def find_fasta_files(root_dir):
    """
    Recursively finds all FASTA files (*.fasta) in the given root directory.
    Args:
        root_dir (str or Path): The root directory to search for FASTA files.
    Returns:
        generator: Generator of Path objects for each found FASTA file.
    """
    return Path(root_dir).rglob("*.fasta")

def parse_fasta(file_path):
    """
    Parses a FASTA file and returns a list of (header, sequence) tuples.
    Args:
        file_path (str or Path): Path to the FASTA file.
    Returns:
        list: List of tuples containing header and sequence strings.
    """
    entries = []
    header = None
    seq_lines = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if header is not None:
                    sequence = ''.join(seq_lines).replace('\n', '').replace('\r', '')
                    entries.append((header, sequence))
                header = line[1:].strip()
                seq_lines = []
            else:
                seq_lines.append(line.strip())
        if header is not None:
            sequence = ''.join(seq_lines).replace('\n', '').replace('\r', '')
            entries.append((header, sequence))
    return entries

def write_counts_to_csv(header_stats, csv_path):
    """
    Writes header and sequence count statistics to a CSV file.
    Args:
        header_stats (dict): Dictionary with header statistics and sequence counts.
        csv_path (str or Path): Output path for the CSV file.
    """
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['duplikat', 'header', 'header_count', 'sequence_count', 'sequence'])
        for header, stat in header_stats.items():
            for seq, seq_count in stat['sequences'].items():
                duplikat = 'duplicate' if seq_count > 1 else 'no'
                writer.writerow([duplikat, header, stat['header_count'], seq_count, seq])

def log_message(message, logfile):
    """
    Logs a message with a timestamp to both the console and a log file.
    Args:
        message (str): The message to log.
        logfile (str or Path): Path to the log file.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(logfile, 'a') as f:
        f.write(log_entry + '\n')

def main(root_dir, out_dir, logfile):
    """
    Main function to process all FASTA files in a directory, count distinct headers and sequences, and write results to CSV files.
    Args:
        root_dir (str or Path): Directory containing input FASTA files.
        out_dir (str or Path): Directory to write CSV files with header and sequence counts.
        logfile (str or Path): Path to the log file.
    """
    root_dir = Path(root_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = Path(logfile)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.touch()
    fasta_files = list(find_fasta_files(root_dir))
    log_message(f"Starte Verarbeitung von {len(fasta_files)} FASTA-Dateien.", logfile)
    for i, fasta_file in enumerate(fasta_files, 1):
        log_message(f"[{i}/{len(fasta_files)}] Verarbeite: {fasta_file}", logfile)
        entries = parse_fasta(fasta_file)
        header_stats = {}
        for header, sequence in entries:
            if header not in header_stats:
                header_stats[header] = {'header_count': 0, 'sequences': {}}
            header_stats[header]['header_count'] += 1
            header_stats[header]['sequences'][sequence] = header_stats[header]['sequences'].get(sequence, 0) + 1
        rel_path = fasta_file.relative_to(root_dir).with_suffix('.csv')
        csv_path = out_dir / rel_path
        write_counts_to_csv(header_stats, csv_path)
        log_message(f"CSV geschrieben: {csv_path}", logfile)
    log_message("Fertig!", logfile)

if __name__ == '__main__':
    main('../DataModel/small/checks/cleaned_fasta', '../DataModel/small/checks/header_counts', '../LOG/header_counts.log')