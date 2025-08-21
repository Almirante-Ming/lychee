import sys
import csv
import os
import unicodedata
import re

def normalize_text(text):
    if not text:
        return text
    
    normalized = unicodedata.normalize('NFD', text)
    
    ascii_text = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    
    # Additional manual replacements for common cases (sugest)
    replacements = {
        'ß': 'ss',
        'œ': 'oe',
        'æ': 'ae',
        'ø': 'o',
        'đ': 'd',
        'ł': 'l',
        'Ł': 'L',
        'Đ': 'D',
        'Ø': 'O',
        'Æ': 'AE',
        'Œ': 'OE',
        '¿': '?',
        '¡': '!',
        '«': '"',
        '»': '"',
        ''': "'",
        ''': "'",
        '"': '"',
        '"': '"',
        '–': '-',
        '—': '-',
        '…': '...',
        '€': 'EUR',
        '£': 'GBP',
        '¥': 'JPY',
        '©': '(c)',
        '®': '(r)',
        '™': '(tm)',
        '°': 'deg',
        'µ': 'u',
        '²': '2',
        '³': '3',
        '¹': '1',
        '¼': '1/4',
        '½': '1/2',
        '¾': '3/4',
    }
    
    for original, replacement in replacements.items():
        ascii_text = ascii_text.replace(original, replacement)
    
    ascii_text = re.sub(r'[^\x00-\x7F]+', '', ascii_text)
    
    return ascii_text

def main(csv_path):
    base_name = os.path.basename(csv_path)
    name_without_ext = os.path.splitext(base_name)[0]
    
    os.makedirs('./files', exist_ok=True)
    
    cleaned_path = f"./files/{name_without_ext}_normalized.csv"

    with open(csv_path, 'r', encoding='utf-8') as infile:
        first_line = infile.readline()
        if ';' in first_line:
            delimiter = ';'
        elif ',' in first_line:
            delimiter = ','
        else:
            delimiter = ','
        
        print(f"Detected delimiter: '{delimiter}'")
        infile.seek(0)
        
        uses_quotes = first_line.startswith('"')
        
        reader = csv.DictReader(infile, delimiter=delimiter)
        fieldnames = reader.fieldnames
        
        if fieldnames is None:
            print("Error: CSV file does not contain a header row.")
            sys.exit(1)
        
        cleaned_fieldnames = [normalize_text(field) for field in fieldnames]
        
        cleaned_rows = []
        changes_made = 0
        
        for row_num, row in enumerate(reader, 1):
            cleaned_row = {}
            row_changed = False
            
            for original_field, cleaned_field in zip(fieldnames, cleaned_fieldnames):
                original_value = row.get(original_field, '')
                cleaned_value = normalize_text(original_value)
                
                if original_value != cleaned_value:
                    row_changed = True
                    changes_made += 1
                
                cleaned_row[cleaned_field] = cleaned_value
            
            if row_changed:
                print(f"Row {row_num}, normalized")
            
            cleaned_rows.append(cleaned_row)

    quoting_style = csv.QUOTE_ALL if uses_quotes else csv.QUOTE_MINIMAL

    with open(cleaned_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=cleaned_fieldnames, quoting=quoting_style, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"ASCII cleaning complete:")
    print(f"- Cleaned file: {cleaned_path}")
    print(f"- Total character replacements: {changes_made}")
    print(f"- All non-ASCII characters normalized to ASCII equivalents")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python regex_replace.py <file.csv>")
        sys.exit(1)
    main(sys.argv[1])
