import time
import json
import os

def json_to_fasta_simple(input_file, output_folder):
    """
    Converts a JSON file with operon entries to separate FASTA files per operon.
    The FASTA header contains operon_id, gene_name, length, score, and all metadata fields.
    """
    os.makedirs(output_folder, exist_ok=True)

    # Load JSON data
    with open(input_file, "r") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries from JSON")
    print(f"First entry keys: {list(data[0].keys()) if data else 'No data'}")

    # If the JSON is a single dict, wrap it in a list for uniform processing
    if isinstance(data, dict):
        data = [data]

    processed_operons = 0
    for entry in data:
        operon_id = entry.get("operon_id", "unknown_operon")
        # Write all Cas proteins to a FASTA file for this operon
        cas_list = entry.get("cas", [])
        #print(f"Processing operon: {operon_id}, cas_list length: {len(cas_list)}")
        
        if cas_list:
            processed_operons += 1
            fasta_path = os.path.join(output_folder, f"{operon_id}.fasta")
            with open(fasta_path, "w") as fasta:
                for cas in cas_list:
                    # Extract fields
                    cas_id = cas.get("id", operon_id)
                    gene_name = cas.get("gene_name", "unknown_gene")
                    length = cas.get("length", "NA")
                    score = cas.get("score", "NA")
                    source_db = cas.get("source_db", "NA")
                    assembly_type = cas.get("assembly_type", "NA")
                    biosample_id = cas.get("biosample_id", "NA")
                    sample_name = cas.get("sample_name", "NA")
                    taxonomy = cas.get("taxonomy", "NA")
                    biome = cas.get("biome", "NA")
                    subtype = cas.get("subtype", "NA")
                    protein_seq = cas.get("protein", "")
                    
                    # Build header
                    header = f">{cas_id}|gene_name={gene_name}|length={length}|score={score}|source_db:{source_db}|assembly_type:{assembly_type}|biosample_id:{biosample_id}|sample_name:{sample_name}|taxonomy:{taxonomy}|biome:{biome}|subtype={subtype}"
                    
                    fasta.write(header + "\n")
                    fasta.write(protein_seq + "\n")

    print(f"Processed {processed_operons} operons with cas proteins")
    print(f"Finished creating FASTA out of JSON. File saved in {output_folder}")


input_file = "../DB/CRISPR-Cas_Atlas/Type_V_filtered_crispr-cas-atlas-v1.0.json"
output_folder = "../DB/CRISPR-Cas_Atlas/FASTA"

# Example usage
if __name__ == "__main__":
    start_time = time.time()

    json_to_fasta_simple(input_file, output_folder)

    end_time = time.time()

    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print("\n")
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
    print("--------------------------------------------------------------------------------")
    print(f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")