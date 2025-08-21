import sys
import json
import csv
import os
import shutil

def main(csv_path):
    valid_ncm_path = './files/valid_ncm.json'
    
    if not os.path.exists(valid_ncm_path):
        print(f"Error: {valid_ncm_path} not found. Please run ncm_valid_generator.py first.")
        sys.exit(1)
    
    with open(valid_ncm_path, 'r', encoding='utf-8') as f:
        valid_ncm = set(json.load(f))

    base_name = os.path.basename(csv_path)
    name_without_ext = os.path.splitext(base_name)[0]
    
    os.makedirs('./files', exist_ok=True)
    
    corrected_path = f"./files/{name_without_ext}_checked.csv"
    invalids_path = f"./files/{name_without_ext}_invalid.csv"

    invalid_rows = []
    corrected_rows = []
    has_modifications = False

    with open(csv_path, 'r', encoding='utf-8') as infile:
        first_line = infile.readline()
        uses_quotes = first_line.startswith('"')
        
        if ';' in first_line:
            delimiter = ';'
        elif ',' in first_line:
            delimiter = ','
        else:
            delimiter = ','
        
        print(f"Detected delimiter: '{delimiter}'")
        infile.seek(0)
        
        reader = csv.DictReader(infile, delimiter=delimiter)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            print("Error: CSV file does not contain a header row.")
            sys.exit(1)
        
        ncm_column = None
        possible_ncm_names = ['NCM', 'ncm', '"NCM"', '"ncm"'] 
        
        for field in fieldnames:
            clean_field = field.strip('"').strip()
            if clean_field.lower() == 'ncm':
                ncm_column = field
                break
        
        if ncm_column is None:
            print("Error: CSV file does not contain an NCM column.")
            print(f"Available columns: {fieldnames}")
            sys.exit(1)

        for row in reader:
            ncm_value = row.get(ncm_column, '').strip()
            
            if ncm_value not in valid_ncm:
                invalid_rows.append(row.copy())
                has_modifications = True
            else:
                corrected_rows.append(row)

    if not has_modifications:
        print("No issues found - all rows are valid")
        return

    quoting_style = csv.QUOTE_ALL if uses_quotes else csv.QUOTE_MINIMAL

    with open(corrected_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=quoting_style, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(corrected_rows)

    with open(invalids_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=quoting_style, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(invalid_rows)

    print(f"Processing complete:")
    print(f"- Invalid rows (for review): {invalids_path}")
    print(f"- Found {len(invalid_rows)} invalid NCM codes")
    print(f"- Valid rows: {len(corrected_rows)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ncm_check.py <file.csv>")
        sys.exit(1)
    main(sys.argv[1])