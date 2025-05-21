# Scanned Notice Parser

This project aims to provide tools for parsing scanned notice documents from PDF or image sources. The parser will eventually extract relevant information using OCR and text processing libraries.

## Setup

1. Clone the repository.
2. Install dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script with the path to a file or directory containing the notices:

```bash
python -m src.main /path/to/notices
```

The current implementation prints the provided path. Future versions will parse the documents with `pytesseract` and `pdfplumber`.
