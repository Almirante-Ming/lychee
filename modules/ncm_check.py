import sys
import json
import csv
import os

def main(valid_ncm_path, csv_path):
    with open(valid_ncm_path, 'r', encoding='utf-8') as f:
        valid_ncm = set(json.load(f))

    base, ext = os.path.splitext(csv_path)
    invalids_path = f"{base}_invalids.csv"

    with open(csv_path, 'r', encoding='utf-8') as infile, \
         open(invalids_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            print("Error: CSV file does not contain a header row.")
            sys.exit(1)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ncm_value = row.get('ncm', '')
            if ncm_value not in valid_ncm:
                row['ncm'] = '00000000'
                writer.writerow(row)

    print(f"Invalid NCM rows written to: {invalids_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ncm_validator.py valid_ncm.json <file.csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])