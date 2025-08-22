import sys
import json
import csv
import os
import shutil
from collections import defaultdict

def sort_by_group_and_subgroup(rows, fieldnames):
    grupo_column = None
    subgrupo_column = None
    
    for field in fieldnames:
        clean_field = field.strip('"').strip().lower()
        if clean_field in ['grupo', 'group']:
            grupo_column = field
        elif clean_field in ['sub_grupo', 'subgrupo', 'SUBGRUPO', 'SUB_GRUPO']:
            subgrupo_column = field
    
    if grupo_column is None:
        print("Warning: GRUPO column not found. Sorting by first column.")
        return rows
    
    def sort_key(row):
        grupo = row.get(grupo_column, '').strip().strip('"')
        subgrupo = row.get(subgrupo_column, '').strip().strip('"') if subgrupo_column else ''
        
        try:
            grupo_int = int(grupo) if grupo else 999999
        except ValueError:
            grupo_int = 999999
        
        try:
            subgrupo_int = int(subgrupo) if subgrupo else 999999
        except ValueError:
            subgrupo_int = 999999
            
        return (grupo_int, subgrupo_int, subgrupo)
    
    return sorted(rows, key=sort_key)

def print_subgroup_aggregation(rows, fieldnames):
    grupo_column = None
    subgrupo_column = None
    
    for field in fieldnames:
        clean_field = field.strip('"').strip().lower()
        if clean_field in ['grupo', 'group']:
            grupo_column = field
        elif clean_field in ['sub_grupo', 'subgrupo', 'sub_group', 'subgroup']:
            subgrupo_column = field
    
    if not rows:
        return
    
    aggregation = defaultdict(lambda: defaultdict(int))
    
    for row in rows:
        grupo = row.get(grupo_column, '').strip().strip('"') if grupo_column else ''
        subgrupo = row.get(subgrupo_column, '').strip().strip('"') if subgrupo_column else ''
        
        grupo_display = grupo if grupo else 'None'
        subgrupo_display = subgrupo if subgrupo else 'None'
            
        aggregation[grupo_display][subgrupo_display] += 1
    
    print("\n" + "="*60)
    print("AGGREGATION SUMMARY BY GROUP AND SUBGROUP")
    print("="*60)
    
    def sort_key(grupo):
        try:
            return (0, int(grupo))
        except ValueError:
            return (1, grupo)
    
    sorted_grupos = sorted(aggregation.keys(), key=sort_key)
    
    for grupo in sorted_grupos:
        subgroups = aggregation[grupo]
        total_grupo = sum(subgroups.values())
        
        print(f"\nGroup {grupo}: {total_grupo} items")
        print("-" * 40)
        
        def sort_subgroup_key(subgrupo):
            try:
                return (0, int(subgrupo))
            except ValueError:
                return (1, subgrupo)
        
        sorted_subgroups = sorted(subgroups.keys(), key=sort_subgroup_key)
        for subgrupo in sorted_subgroups:
            count = subgroups[subgrupo]
            print(f"  └─ {subgrupo}: {count} items")

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

    sorted_invalid_rows = sort_by_group_and_subgroup(invalid_rows, fieldnames)
    
    with open(invalids_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=quoting_style, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(sorted_invalid_rows)

    print(f"Processing complete:")
    print(f"- Invalid rows (for review): {invalids_path}")
    print(f"- Found {len(invalid_rows)} invalid NCM codes")
    print(f"- Valid rows: {len(corrected_rows)}")
    
    print_subgroup_aggregation(sorted_invalid_rows, fieldnames)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ncm_check.py <file.csv>")
        sys.exit(1)
    main(sys.argv[1])