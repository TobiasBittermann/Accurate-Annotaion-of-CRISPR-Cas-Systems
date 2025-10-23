import time
import re
from pathlib import Path

def translator(input_file: str, output_file: str):

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                line = re.sub(r'cas14', 'Cas12f', line, flags=re.IGNORECASE)
                line = re.sub(r'u1', 'Cas12m', line, flags=re.IGNORECASE)
                line = re.sub(r'u2', 'Cas12u2', line, flags=re.IGNORECASE)
                line = re.sub(r'u3', 'Cas12u3', line, flags=re.IGNORECASE)
                line = re.sub(r'u4', 'Cas12n', line, flags=re.IGNORECASE)
                line = re.sub(r'u5', 'Cas12k', line, flags=re.IGNORECASE)
                line = re.sub(r'tnpb', 'TnpB', line, flags=re.IGNORECASE)
                # Keep only the Cas12 variant (e.g. Cas12f, Cas12m, ...)
                match = re.search(r'(Cas12[a-zA-Z])', line)
                if match:
                    line = match.group(1) + '\n'
                    outfile.write(">" + line)
                else:
                    outfile.write(line)
            else:
                outfile.write(line)

if __name__ == "__main__":
    start_time = time.time()

    input_file = Path("../DB/CasPedia/1_raw/phylogeny_type5.faa")
    output_file = Path("../DB/CasPedia/1_raw/translated_casPedia.fasta")

    translator(input_file, output_file)

    end_time = time.time()
    elapsed_time = int(end_time - start_time)
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print(f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")