import json
import time
from pathlib import Path

def filter_json_by_subtype_v(input_file, output_file):
    """
    Filters a JSON file and writes all entries where the subtype in the summary starts with 'V' (case-insensitive)
    to a new JSON file. Works for subtypes like 'V1', 'Vt', 'V 23', etc.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSON file where filtered entries will be saved.
    """

    print(f"Start filtering JSON file: {input_file}")

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)

    # Load the JSON data from the input file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Filter entries: check if 'summary' and 'subtype' exist and subtype starts with 'V'
    # and if the operon contains any cas12 genes
    filtered = [
        entry for entry in data
        if "summary" in entry
        and "subtype" in entry["summary"]
        and entry["summary"]["subtype"] is not None
        and str(entry["summary"]["subtype"]).strip().upper().startswith("V")
    ]

    with open(output_file, "w") as f:
        json.dump(filtered, f, indent=2)

    print(f"Filtered records written to {output_file}")

if __name__ == "__main__":
    start_time = time.time()


    # Define file paths and names here for clarity and easy modification
    file_name = "crispr-cas-atlas-v1.0.json"
    folder_name = "../DB/CRISPR-Cas_Atlas/"
    filter_name = "Type_V_cas12_filtered_"
    input_file = f"{folder_name}{file_name}"
    output_file = f"{folder_name}{filter_name}{file_name}"

    filter_json_by_subtype_v(input_file, output_file)
    print("Filtering complete. Filtered JSON file is saved as:", output_file)

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
