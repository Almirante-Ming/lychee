import sys
import csv
import os

def main(csv_path):
    base_name = os.path.basename(csv_path)
    name_without_ext = os.path.splitext(base_name)[0]
    
    os.makedirs('./files', exist_ok=True)
    
    fixed_path = f"./files/{name_without_ext}_table_fixed.csv"

    with open(csv_path, 'r', encoding='utf-8') as infile:
        first_line = infile.readline()
        infile.seek(0)
        
        if ',' in first_line and '"' in first_line:
            delimiter = ','
        elif ';' in first_line:
            delimiter = ';'
        else:
            delimiter = ','
        
        reader = csv.reader(infile, delimiter=delimiter)
        rows = list(reader)
    
    if not rows:
        print("Error: CSV file is empty.")
        sys.exit(1)
    
    header = rows[0]
    processed_header = []
    for field in header:
        clean_field = field.strip('"').strip("'").strip()
        processed_header.append(clean_field.upper())
    
    processed_rows = []
    for row in rows[1:]:
        processed_row = []
        for field in row:
            processed_field = field.replace('"', "'")
            processed_row.append(f'"{processed_field}"')
        processed_rows.append(processed_row)
    
    with open(fixed_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';', quoting=csv.QUOTE_NONE, escapechar='\\')
        
        writer.writerow(processed_header)
        
        for row in processed_rows:
            outfile.write(';'.join(row) + '\n')
    
    print(f"Table processing complete:")
    print(f"- Fixed file (semicolon separator, quoted values): {fixed_path}")
    print(f"- Header converted to uppercase")
    print(f"- All data values quoted as strings")
    print(f"- Internal quotes replaced with single quotes")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python table_fix.py <file.csv>")
        sys.exit(1)
    main(sys.argv[1])
