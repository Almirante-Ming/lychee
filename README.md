# 🍃 CSV Processor - Lychee

A CSV processing toolkit with CLI interface.

## Requirements

- Python 3.13+
- command shell (powershell, bash, zsh)

## Installation

1. Clone or download this repository
2. Run: `python app.py` **on project root**

Compatible with Windows and Linux systems.

## Features

### Available Modules:
1. **Table Fix** - Converts CSV to semicolon-separated format with quotes
2. **Regex Replace** - Normalizes Unicode characters to ASCII
3. **NCM Check** - Validates NCM codes against official database
4. **NCM Valid Generator** - Generates valid NCM codes from JSON data
5. **Date Fix** - Converts various date formats to yyyy-mm-dd standard  
6. **Table Out** - Removes quotes and validates CSV format

**p.s: use modules in same order when is showing**

## Quick Start

### GUI Mode (if available)
```bash
python app.py
```
The app will launch in  the command line interface.

```bash
python app.py
```

Then select from the menu:
- Enter 1-6 to run processing modules
- Enter 7 to open the output files folder
- Enter 8 to exit

## Individual Module Usage

Each module can also be run independently:

### NCM Validation
```bash
# First generate valid NCM codes
python modules/ncm_valid_generator.py tabela_vigente_*.json

# Others modules
python modules/module_name.py your_file.csv
```

## File Structure

```
lychee/
├── app.py                    # Main application
├── modules/                 # Processing modules
│   ├── ncm_check.py
│   ├── ncm_valid_generator.py
│   ├── date_fix.py
│   ├── table_fix.py
│   ├── table_out.py
│   └── regex_replace.py
├── files/                   # Output directory
└── README.md
```

## Output Files

All processed files are saved to the `./files/` directory with descriptive suffixes:
- `*_valid.csv` - Valid records
- `*_invalid.csv` - Invalid records  
- `*_fixed.csv` - Processed/fixed data
- `*_errors.txt` - Error reports