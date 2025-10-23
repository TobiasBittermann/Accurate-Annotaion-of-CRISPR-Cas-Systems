import count_distinct_headers_and_sequences
import delete_duplicate_sequences
import merge_fasta
import sort_datamodel
from pathlib import Path


delete_duplicate_sequences.main('../DataModel/small', '../DataModel/small/checks/cleaned_fasta', '../LOG/cleaned_fasta.log')
count_distinct_headers_and_sequences.main('../DataModel/small/checks/cleaned_fasta', '../DataModel/small/checks/header_counts', '../LOG/header_counts.log')

source_folder = Path('../DataModel/small/checks/cleaned_fasta')
output_file = Path('../DataModel/small/checks/merge/merged.fasta')
ending = "fasta"
use_subfolders = True

if (use_subfolders):
    merge_fasta.merge_fasta_files_all_dict(source_folder, output_file, ending)
else:
    merge_fasta.merge_fasta_files_current_dir(source_folder, output_file, ending)

sort_datamodel.sort_fasta_by_subtype('../DataModel/small/checks/merge/merged.fasta', '../DataModel/small/checks/sorted_fasta_small')