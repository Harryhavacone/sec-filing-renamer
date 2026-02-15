# SEC Filing PDF Renamer

Automatically rename SEC filing PDFs (13G/A, 10-K, 10-Q, 8-K, etc.) based on their content, extracting filing date, type, ticker, filer name, and ownership percentage.

## Features

- Extracts filing metadata from PDF content:
  - Filing type (13G/A, 10-K, 10-Q, 8-K, etc.)
  - Filing/event date
  - Stock ticker symbol
  - Filer/reporting person name
  - Ownership percentage (for 13G/13D filings)
- Generates consistent, descriptive filenames: `YYYY-MM-DD_FILING-TYPE_TICKER_FILER-NAME_X-XXPCT.pdf`
- Dry-run mode to preview changes before applying them
- Handles multiple filings by the same entity on the same date

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/sec-filing-renamer.git
cd sec-filing-renamer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or on systems that require it:
```bash
pip install -r requirements.txt --break-system-packages
```

## Usage

### Basic Usage

Rename all PDFs in a folder:
```bash
python src/renamer.py /path/to/your/pdf/folder
```

### Dry Run (Recommended First Step)

Preview changes without renaming:
```bash
python src/renamer.py /path/to/your/pdf/folder --dry-run
```

### Examples

**Preview changes:**
```bash
python src/renamer.py ~/Documents/SEC-Filings --dry-run
```

**Rename files:**
```bash
python src/renamer.py ~/Documents/SEC-Filings
```

## Output Format

Files are renamed with this pattern:

- `2025-06-30_13G-A_RDDT_BAILLIE-GIFFORD-CO_5-01PCT.pdf`
  - Date: June 30, 2025
  - Filing: 13G/A (amendment)
  - Company: Reddit (RDDT)
  - Filer: Baillie Gifford & Co
  - Ownership: 5.01%

- `2025-08-16_13D-A_RDDT_STEVEN-HUFFMAN_30-7PCT.pdf`
  - Date: August 16, 2025
  - Filing: 13D/A (amendment)
  - Company: Reddit (RDDT)
  - Filer: Steven Huffman
  - Ownership: 30.7%

The ownership percentage is particularly useful for 13G/13D filings where the same filer may file multiple times on the same date (e.g., when crossing ownership thresholds).

## Supported Filing Types

- 10-K, 10-Q, 8-K, 20-F
- 13D, 13G, 13F, 13D/A, 13G/A
- S-1, S-3, S-4, S-8
- DEF 14A, DEFA14A
- SC 13D, SC 13G
- 6-K, 424B5, FWP

## How It Works

1. Reads the first few pages of each PDF
2. Extracts metadata using pattern matching:
   - Filing type from document headers
   - Filing/event date from various date fields
   - Ticker symbol from issuer information
   - Filer name from "Reporting Persons" section
   - Ownership percentage from disclosure rows
3. Constructs descriptive filename from extracted data
4. Renames files (or shows preview in dry-run mode)

## Project Structure

```
sec-filing-renamer/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Files to exclude from Git
├── src/
│   └── renamer.py           # Main script
└── LICENSE                  # License file (optional)
```

## Tips

- **Always run with `--dry-run` first** to preview changes
- The script only reads the first 5 pages of each PDF for speed
- Keep backups of important files before running
- Files that cannot be processed will be skipped and reported

## Troubleshooting

**"Could not find date" or "Could not find filing type"**
- The PDF format may be unusual or text extraction failed
- Some scanned PDFs may need OCR before processing

**"File already exists"**
- Multiple files would have the same name
- Review the dry-run output to see which files conflict
- This is normal for test files or duplicate downloads

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

## License

MIT License - feel free to use and modify for your own purposes.
