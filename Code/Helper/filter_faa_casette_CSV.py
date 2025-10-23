import os
import csv
import sys
import time

def filter_faa_casette_CSV(csv_file_path, faa_folder_path, filtered_folder_path):
    """
    This function filters sequences from .faa files based on start and end coordinates
    provided in the CSV file and saves the filtered sequences into a new folder.
    """

    # Create the output folder if it doesn't already exist
    os.makedirs(filtered_folder_path, exist_ok=True)

    # List all .faa files in the faa_folder_path and sort them
    faa_files = sorted(file_name for file_name in os.listdir(faa_folder_path) if file_name.endswith('.faa'))

    # Open the CSV file to read genomic data
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Skip the header row of the CSV file
        next(csv_reader)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Extract genomic name, start and end coordinates from the CSV row
            name_csv, start_csv, end_csv = row[0], int(row[3]), int(row[4])
            
            # Set a buffer value to extend the range around the start and end coordinates
            buffer = 15

            # Iterate through each .faa file
            for faa_file in faa_files:
                # Check if the genome name matches the base name of the .faa file (without the .faa extension)
                if name_csv == os.path.splitext(faa_file)[0]:
                    faa_file_path = os.path.join(faa_folder_path, faa_file)

                    # Open the .faa file and read its content
                    with open(faa_file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    
                    # Initialize a list to store filtered lines
                    filtered_lines = []
                    keep_sequence = False

                    # Iterate through each line in the .faa file
                    for line in lines:
                        line = line.strip()
                        
                        # Check if the line is a header (starts with '>')
                        if line.startswith('>'):
                            header = line[1:]
                            parts = header.split('_')  # Split header into parts (assuming the format: '>name_start_end')
                            
                            # Extract the start and end coordinates from the header
                            start = int(parts[1])
                            end = int(parts[2])
                            
                            # Check if the sequence falls within the range defined in the CSV (with buffer)
                            if start_csv - buffer <= start <= end_csv + buffer and start_csv - buffer <= end <= end_csv + buffer:
                                keep_sequence = True  # Keep the sequence if it matches the coordinates
                            else:
                                keep_sequence = False  # Skip the sequence if it doesn't match the coordinates

                        # If the sequence should be kept, append the line to filtered_lines
                        if keep_sequence:
                            filtered_lines.append(line + '\n')

                            # Print header line when added to filtered lines
                            if line.startswith('>'):
                                print(f"Header added: {line}")

                    # Path to save the filtered .faa file
                    filtered_file_path = os.path.join(filtered_folder_path, faa_file)

                    # Append the filtered lines to the corresponding output file
                    with open(filtered_file_path, 'a', encoding='utf-8') as file:
                        file.writelines(filtered_lines)


if __name__ == "__main__":

    start_time = time.time()

    if len(sys.argv) == 4:
        csv_file_path = sys.argv[1]
        faa_folder_path = sys.argv[2]
        filtered_folder_path = sys.argv[3]
        filter_faa_casette_CSV(csv_file_path, faa_folder_path, filtered_folder_path)
    else:
        print("Program: filter_faa_casette_CSV.py")
        print("Missing or wrong arguments. Parameters needed.")
        print("Usage:")
        print("  python script.py <csv_file_path><input_folder><output_folder>")
        sys.exit(1)

    end_time = time.time()
    elapsed_time = int(end_time - start_time)

    #Format elapsed time as hh:mm:ss
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"Start Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
    print(f"End Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}\n")
    print("--------------------------------------------------------------------------------")
    print (f"Finished total time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("--------------------------------------------------------------------------------")