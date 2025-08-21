# 🍃 CSV Processor - Lychee

A comprehensive CSV processing toolkit with both GUI and CLI interfaces for table formatting and database migration.

## Features

### Available Modules:
1. **NCM Check** - Validates NCM codes against official database
2. **Date Fix** - Converts various date formats to yyyy-mm-dd standard  
3. **Table Fix** - Converts CSV to semicolon-separated format with quotes
4. **Table Out** - Removes quotes and validates CSV format
5. **Regex Replace** - Normalizes Unicode characters to ASCII
6. **NCM Valid Generator** - Generates valid NCM codes from JSON data

## Quick Start

### GUI Mode (if available)
```bash
python app.py
```
The app will automatically detect if GUI is available and launch the graphical interface.

### CLI Mode
If GUI is not available, the app automatically falls back to CLI mode with an interactive menu:

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
python modules/ncm_valid_generator.py data/ncm_codes.json

# Then validate your CSV
python modules/ncm_check.py your_file.csv
```

### Date Processing
```bash
python modules/date_fix.py your_file.csv
```

### Table Formatting
```bash
python modules/table_fix.py your_file.csv
python modules/table_out.py your_file.csv
```

### Character Normalization
```bash
python modules/regex_replace.py your_file.csv
```

## File Structure

```
lychee/
├── app.py                    # Main application (auto GUI/CLI)
├── app_gui.py               # GUI-only version (Dear PyGui)
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

## Requirements

- Python 3.7+
- Standard library modules (csv, json, os, sys, etc.)
- Optional: dearpygui (for GUI mode)

## Installation

1. Clone or download this repository
2. For GUI support: `pip install dearpygui`
3. Run: `python app.py`

Compatible with Windows and Linux systems. The application works without any external dependencies in CLI mode!
