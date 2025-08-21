import sys
import csv
import os
import re

def lint_csv_format(csv_path, delimiter=','):
    errors = []
    warnings = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    if not lines:
        errors.append("File is empty")
        return errors, warnings

    header_line = lines[0].strip()
    if not header_line:
        errors.append("Line 1: Header is empty")
        return errors, warnings
    
    header_fields = header_line.split(delimiter)
    expected_columns = len(header_fields)
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            warnings.append(f"Line {line_num}: Empty line")
            continue
        
        fields = line.split(delimiter)
        actual_columns = len(fields)
        
        if actual_columns != expected_columns:
            errors.append(f"Line {line_num}: Expected {expected_columns} columns, found {actual_columns}")
        
        for field_num, field in enumerate(fields, 1):
            quote_count = field.count('"')
            if quote_count % 2 != 0:
                errors.append(f"Line {line_num}, Field {field_num}: Unmatched quote in '{field}'")
            
            if '"' in field and not (field.startswith('"') and field.endswith('"')):
                if quote_count > 0:
                    warnings.append(f"Line {line_num}, Field {field_num}: Quote not properly escaped in '{field}'")
    
    return errors, warnings

def remove_quotes_and_clean(csv_path):
    base_name = os.path.basename(csv_path)
    name_without_ext = os.path.splitext(base_name)[0]
    
    os.makedirs('./files', exist_ok=True)
    
    cleaned_path = f"./files/{name_without_ext}_no_quotes.csv"
    
    with open(csv_path, 'r', encoding='utf-8') as infile:
        first_line = infile.readline()
        if ';' in first_line:
            delimiter = ';'
        elif ',' in first_line:
            delimiter = ','
        else:
            delimiter = ','
    
    print(f"Detected delimiter: '{delimiter}'")
    
    cleaned_lines = []
    
    with open(csv_path, 'r', encoding='utf-8') as infile:
        for line_num, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue
            
            cleaned_line = line.replace('"', '')
            
            fields = [field.strip() for field in cleaned_line.split(delimiter)]
            cleaned_line = delimiter.join(fields)
            
            cleaned_lines.append(cleaned_line)
    
    with open(cleaned_path, 'w', encoding='utf-8') as outfile:
        for line in cleaned_lines:
            outfile.write(line + '\n')
    
    return cleaned_path, delimiter

def main(csv_path):
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' not found.")
        sys.exit(1)
    
    print(f"Processing: {csv_path}")
    print("=" * 50)
    
    print("1. LINTING ORIGINAL FILE:")
    
    with open(csv_path, 'r', encoding='utf-8') as infile:
        first_line = infile.readline()
        if ';' in first_line:
            delimiter = ';'
        elif ',' in first_line:
            delimiter = ','
        else:
            delimiter = ','
    
    errors, warnings = lint_csv_format(csv_path, delimiter)
    
    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(f"{error}")
    else:
        print("No format errors found")
    
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"{warning}")
    else:
        print("No warnings")
    
    print("\n2. REMOVING QUOTES AND CLEANING:")

    cleaned_path, detected_delimiter = remove_quotes_and_clean(csv_path)
    
    print(f"Quotes removed successfully")
    print(f"File cleaned and saved to: {cleaned_path}")
    
    print("\n3. LINTING CLEANED FILE:")
    
    errors_cleaned, warnings_cleaned = lint_csv_format(cleaned_path, detected_delimiter)
    
    if errors_cleaned:
        print("ERRORS IN CLEANED FILE:")
        for error in errors_cleaned:
            print(f"{error}")
    else:
        print("No format errors in cleaned file")
    
    if warnings_cleaned:
        print("WARNINGS IN CLEANED FILE:")
        for warning in warnings_cleaned:
            print(f"  {warning}")
    else:
        print("No warnings in cleaned file")
    
    print("\n4. SUMMARY:")
    print(f"  • Original file: {len(errors)} errors, {len(warnings)} warnings")
    print(f"  • Cleaned file: {len(errors_cleaned)} errors, {len(warnings_cleaned)} warnings")
    print(f"  • Output file: {cleaned_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python table_out.py <file.csv>")
        sys.exit(1)
    main(sys.argv[1])