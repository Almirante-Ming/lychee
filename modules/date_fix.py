import sys
import csv
import os
import re
from datetime import datetime

def parse_date(date_str):
    if not date_str or date_str.strip() == '':
        return date_str
    
    date_str = date_str.strip()

    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%m/%d/%Y',
        '%m-%d-%Y',
        '%Y/%m/%d',
        '%d/%m/%y',
        '%d-%m-%y',
        '%m/%d/%y',
        '%m-%d-%y',
        '%y/%m/%d',
        '%y-%m-%d',
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return None

def main(csv_path):
    base_name = os.path.basename(csv_path)
    name_without_ext = os.path.splitext(base_name)[0]
    
    os.makedirs('./files', exist_ok=True)
    
    fixed_path = f"./files/{name_without_ext}_date_fixed.csv"
    errors_path = f"./files/{name_without_ext}_date_errors.csv"

    error_rows = []
    fixed_rows = []
    has_modifications = False
    has_errors = False

    with open(csv_path, 'r', encoding='utf-8') as infile:
        first_line = infile.readline()
        uses_quotes = first_line.startswith('"')
        infile.seek(0)
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if fieldnames is None:
            print("Error: CSV file does not contain a header row.")
            sys.exit(1)
        
        date_columns = []
        target_date_fields = ['emissao', 'vencimento']
        
        for field in fieldnames:
            clean_field = field.strip('"').strip().lower()
            if clean_field in target_date_fields:
                date_columns.append(field)
        
        if not date_columns:
            print("No date columns found (looking for 'emissao' and/or 'vencimento').")
            print(f"Available columns: {fieldnames}")
            sys.exit(1)
        
        print(f"Found date columns: {date_columns}")

        for row in reader:
            row_has_error = False
            fixed_row = row.copy()
            error_row = row.copy()
            
            for date_column in date_columns:
                original_value = row.get(date_column, '').strip()
                
                if original_value:
                    parsed_date = parse_date(original_value)
                    
                    if parsed_date is None:
                        row_has_error = True
                        has_errors = True
                        print(f"Warning: Could not parse date '{original_value}' in column '{date_column}'")
                    elif parsed_date != original_value:
                        fixed_row[date_column] = parsed_date
                        has_modifications = True

            if row_has_error:
                error_rows.append(error_row)
            
            fixed_rows.append(fixed_row)

    quoting_style = csv.QUOTE_ALL if uses_quotes else csv.QUOTE_MINIMAL

    if not has_modifications and not has_errors:
        print("No issues found - all dates are already in yyyy-mm-dd format")
        return

    with open(fixed_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=quoting_style)
        writer.writeheader()
        writer.writerows(fixed_rows)

    if has_errors:
        with open(errors_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=quoting_style)
            writer.writeheader()
            writer.writerows(error_rows)

    print(f"Processing complete:")
    print(f"- Fixed file (dates → yyyy-mm-dd): {fixed_path}")
    if has_errors:
        print(f"- Error rows (unparseable dates): {errors_path}")
        print(f"- Found {len(error_rows)} rows with unparseable dates")
    if has_modifications:
        print(f"- Successfully converted dates in {len(date_columns)} column(s)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python date_fix.py <file.csv>")
        sys.exit(1)
    main(sys.argv[1])