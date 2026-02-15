#!/usr/bin/env python3
"""
SEC Filing PDF Renamer

This script renames SEC filing PDFs (like 13G/A, 10-Q, 10-K, 8-K, etc.) based on their content.
It extracts the filing date, document type, ticker, filer name, and ownership percentage, 
then renames files in the format:
YYYY-MM-DD_FILING-TYPE_TICKER_FILER-NAME_X-XXPCT.pdf

Usage:
    python rename_earnings_pdfs.py /path/to/folder
    python rename_earnings_pdfs.py /path/to/folder --dry-run
"""

import os
import sys
import re
from pathlib import Path
import pdfplumber
from datetime import datetime

# Common SEC filing types (amendments first to match before base forms)
FILING_TYPES = [
    '13D/A', '13G/A',  # Amendments first
    '10-K', '10-Q', '8-K', '20-F',
    '13D', '13G', '13F',
    'S-1', 'S-3', 'S-4', 'S-8',
    'DEF 14A', 'DEFA14A', 'SC 13D', 'SC 13G',
    '6-K', '424B5', 'FWP'
]

def extract_text_from_pdf(pdf_path, max_pages=5):
    """Extract text from the first few pages of a PDF."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Only read first few pages to speed up processing
            for page in pdf.pages[:max_pages]:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""
    return text

def find_filing_type(text):
    """Find the SEC filing type in the document text."""
    # Look for filing type patterns
    for filing_type in FILING_TYPES:
        # Escape special characters in filing type
        pattern = re.escape(filing_type)
        # Look for patterns like "FORM 10-K", "Form: 10-Q", "SCHEDULE 13G/A" etc.
        if re.search(rf'(?:FORM|Form|TYPE|SCHEDULE|Schedule)[\s:]*{pattern}\b', text, re.IGNORECASE):
            return filing_type
    
    # Also check for standalone mentions (be more careful with this)
    for filing_type in FILING_TYPES:
        pattern = re.escape(filing_type)
        # Make sure we're not matching partial words
        if re.search(rf'\b{pattern}\b', text):
            return filing_type
    
    return None

def find_filing_date(text):
    """Find the filing date or event date in the document."""
    # Common date patterns in SEC filings
    date_patterns = [
        # Standalone date like "06/30/2025" near top of document
        r'\b(\d{2}/\d{2}/\d{4})\b',
        # "EVENT DATE: June 30, 2025"
        r'EVENT DATE[:\s]*([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
        # "FILED AS OF DATE: 06/30/2025"
        r'FILED AS OF DATE[:\s]*(\d{1,2}/\d{1,2}/\d{4})',
        # "CONFORMED PERIOD OF REPORT: 20250630"
        r'CONFORMED PERIOD OF REPORT[:\s]*(\d{8})',
        # "For the fiscal year ended December 31, 2024"
        r'[Ff]or the (?:fiscal|quarterly) (?:year|period) ended[:\s]*([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
        # "Date: June 30, 2025"
        r'Date[:\s]*([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
        # Date in parentheses like "(Date of Event Which Requires Filing of this Statement)"
        r'\(Date of Event[^)]*\)\s*\n\s*(\d{2}/\d{2}/\d{4})',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            date_str = match.group(1).strip()
            # Try to parse the date
            date_obj = parse_date(date_str)
            if date_obj:
                return date_obj
    
    return None

def parse_date(date_str):
    """Parse various date formats into a datetime object."""
    date_formats = [
        '%B %d, %Y',   # June 30, 2025
        '%B %d %Y',    # June 30 2025
        '%m/%d/%Y',    # 06/30/2025
        '%Y%m%d',      # 20250630
        '%d-%b-%Y',    # 30-Jun-2025
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None

def find_ticker(text):
    """Find the stock ticker symbol in the document."""
    # Look for ticker patterns
    patterns = [
        # Company name followed by potential ticker info
        r'Reddit,?\s+Inc\.',  # Just identify it's Reddit
        r'TRADING SYMBOL[:\s]*([A-Z]{1,5})\b',
        r'TICKER[:\s]*([A-Z]{1,5})\b',
        r'SYMBOL[:\s]*([A-Z]{1,5})\b',
        # Common in 13D/13G filings
        r'CUSIP NO\.\s*\d+\s*([A-Z]{1,5})\b',
    ]
    
    # Special case: if we see Reddit Inc, return RDDT
    if re.search(r'Reddit,?\s+Inc\.', text, re.IGNORECASE):
        return 'RDDT'
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            ticker = match.group(1).upper()
            # Filter out common false positives
            if ticker not in ['INC', 'CO', 'LLC', 'LP', 'LTD']:
                return ticker
    
    return None

def find_filer_name(text):
    """Find the name of the reporting person/filer."""
    # Look for "Names of Reporting Persons" section
    patterns = [
        # Standard 13G/13D format - capture text after the label, before next field
        r'Names? of Reporting Persons?\s*\n\s*([A-Z][A-Z\s&,\.]+?)(?:\n\d|\nCheck|$)',
        # When name appears after row number "1"
        r'Names? of Reporting Persons?\s*\n\s*\d+\s*\n\s*([A-Z][A-Z\s&,\.]+?)(?:\n|$)',
        # Name of reporting person (singular, often in 13D)
        r'Name of reporting person\s*\n\s*\d*\s*\n?\s*([A-Z][A-Za-z\s]+?)(?:\n\d|\nCheck|$)',
        # Alternative format
        r'Name of person filing:\s*\n?\s*([A-Z][A-Z\s&,\.]+?)(?:\n|$)',
        # Item 2(a) format
        r'Item 2\.\s*\(a\)\s*Name of person filing:\s*\n?\s*([^\n]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            name = match.group(1).strip()
            # Clean up the name
            name = name.replace('\n', ' ').strip()
            # Remove common legal suffixes but keep & CO
            name = re.sub(r'\s+(LLC|LP|LLP|LTD|LIMITED|INC|INCORPORATED|CORP|CORPORATION)\.?$', '', name, flags=re.IGNORECASE)
            # Remove extra spaces
            name = re.sub(r'\s+', ' ', name).strip()
            
            # Limit length and abbreviate if needed
            if len(name) > 30:
                # Try to get first few words
                words = name.split()
                if len(words) > 2:
                    # Take first 2-3 words
                    name = ' '.join(words[:2])
            
            return name if name else None
    
    return None

def find_ownership_percentage(text):
    """Find the ownership percentage from the filing."""
    # Look for percentage patterns in 13G/13D filings
    patterns = [
        # Multi-line format: "Percent of class represented by amount in row (9)" followed by row number, then percentage
        r'Percent of class represented by amount in (?:row|Row)\s*\([^)]+\)\s*\n\s*\d+\s*\n\s*(\d+\.?\d*)\s*%',
        # Single line: "Percent of class represented by amount in row (9) 5.5 %"
        r'Percent of class represented by amount in (?:row|Row)[^0-9]*(\d+\.?\d*)\s*%',
        # "Percent of class: 5.01 %"
        r'Percent of class[:\s]*(\d+\.?\d*)\s*%',
        # Item 4(b) format
        r'Item 4\.[^(]*\(b\)[^:]*:\s*(\d+\.?\d*)\s*%',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            percentage = match.group(1).strip()
            return percentage
    
    return None

def clean_filename_part(text):
    """Clean a text string to be safe for use in filenames."""
    # Replace spaces and & with hyphens (don't spell out 'and')
    text = text.replace(' & ', '-')
    text = text.replace(' ', '-')
    text = text.replace('&', '-')
    # Remove periods
    text = text.replace('.', '')
    # Remove or replace unsafe characters
    text = re.sub(r'[^\w\-]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    # Convert to uppercase for consistency
    text = text.upper()
    return text

def generate_new_filename(pdf_path, dry_run=False):
    """Generate a new filename based on PDF content."""
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print(f"⚠️  Could not extract text from {pdf_path.name}")
        return None
    
    # Extract metadata
    filing_type = find_filing_type(text)
    filing_date = find_filing_date(text)
    ticker = find_ticker(text)
    filer = find_filer_name(text)
    ownership_pct = find_ownership_percentage(text)
    
    # Build new filename
    parts = []
    
    if filing_date:
        parts.append(filing_date.strftime('%Y-%m-%d'))
    else:
        print(f"⚠️  Could not find date in {pdf_path.name}")
        return None
    
    if filing_type:
        # Clean up filing type for filename (remove slashes, spaces)
        clean_type = filing_type.replace('/', '-').replace(' ', '-')
        parts.append(clean_type)
    else:
        print(f"⚠️  Could not find filing type in {pdf_path.name}")
        return None
    
    if ticker:
        parts.append(ticker)
    
    # Add filer name if found
    if filer:
        clean_filer = clean_filename_part(filer)
        parts.append(clean_filer)
    
    # Add ownership percentage if found
    if ownership_pct:
        # Format: 5.01 -> 5-01PCT
        pct_clean = ownership_pct.replace('.', '-')
        parts.append(f"{pct_clean}PCT")
    
    new_name = '_'.join(parts) + '.pdf'
    
    return new_name

def rename_pdfs_in_folder(folder_path, dry_run=False):
    """Rename all PDF files in the specified folder."""
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        print(f"Error: {folder_path} is not a valid directory")
        return
    
    # Find all PDF files
    pdf_files = list(folder.glob('*.pdf'))
    
    if not pdf_files:
        print(f"No PDF files found in {folder_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    print(f"{'DRY RUN - ' if dry_run else ''}Processing...\n")
    
    renamed_count = 0
    skipped_count = 0
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        
        new_name = generate_new_filename(pdf_file, dry_run)
        
        if new_name:
            new_path = pdf_file.parent / new_name
            
            # Check if file already exists
            if new_path.exists() and new_path != pdf_file:
                print(f"⚠️  File already exists: {new_name}")
                skipped_count += 1
            else:
                if dry_run:
                    print(f"✓  Would rename to: {new_name}")
                else:
                    pdf_file.rename(new_path)
                    print(f"✓  Renamed to: {new_name}")
                renamed_count += 1
        else:
            skipped_count += 1
        
        print()
    
    print(f"\n{'DRY RUN ' if dry_run else ''}Summary:")
    print(f"  Renamed: {renamed_count}")
    print(f"  Skipped: {skipped_count}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    folder_path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    if dry_run:
        print("=== DRY RUN MODE - No files will be renamed ===\n")
    
    rename_pdfs_in_folder(folder_path, dry_run)

if __name__ == '__main__':
    main()
