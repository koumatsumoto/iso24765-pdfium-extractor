# ISO24765 PDF Text Extractor

This tool extracts text from ISO24765 PDF files using pypdfium2.

## Features

- PDF text extraction using pypdfium2
- Support for ISO24765 format

## Installation

```bash

```

## Usage

TBD

## Project Structure

This project is organized into several modules:

### Main Components

- `src/main.py` - Main entry point that orchestrates the extraction process
- `src/pdf_processor.py` - PDF text processing functionality
  - Text extraction from PDF
  - Header/footer block removal
  - Figure line removal
  - Section filtering
- `src/data_extractor.py` - Data extraction and output functionality
  - Word and description extraction
  - JSON output handling

### Tests

- `tests/test_main.py` - Integration tests for the main process
- `tests/test_pdf_processor.py` - Unit tests for PDF processing functions
- `tests/test_data_extractor.py` - Unit tests for data extraction functions

### Processing Flow

1. PDF Text Extraction
   - Extract raw text from PDF using pypdfium2
   - Remove headers (page numbers, copyright notices)
   - Remove footers (license info, document references)
   - Remove figure references
   - Filter content to start from section 3.1

2. Data Extraction
   - Parse the cleaned text to extract words and their descriptions
   - Save the extracted data as structured JSON
