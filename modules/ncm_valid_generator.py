import json
import re
import sys
import os

def main():
    if len(sys.argv) != 2:
        print("Uso: python ncm_valid_generator.py <arquivo_json>")
        sys.exit(1)
    ncm_valid_file = sys.argv[1]
    with open(ncm_valid_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                data = value
                break

    valid_ncm_list = []
    for item in data:
        if isinstance(item, dict):
            ncm_code = item.get('Codigo', '') or item.get('codigo', '')
        elif isinstance(item, str):
            ncm_code = item
        else:
            continue

        cleaned_code = re.sub(r'\D', '', ncm_code)

        if cleaned_code and len(cleaned_code) <= 8:
            padded_code = cleaned_code.ljust(8, '0')
            valid_ncm_list.append(padded_code)

    os.makedirs('./files', exist_ok=True)
    
    with open('./files/valid_ncm.json', 'w', encoding='utf-8') as f:
        json.dump(valid_ncm_list, f, ensure_ascii=False, indent=2)

    print(f'{len(valid_ncm_list)} ncm validos processados')

if __name__ == "__main__":
    main()
