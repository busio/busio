# Scanned Notice Parser

This project aims to provide tools for parsing scanned notice documents from PDF or image sources. The parser will eventually extract relevant information using OCR and text processing libraries.

## Setup

1. Clone the repository.
2. Install dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script with the path to the merged PDF containing multiple IRS letters. The script will OCR each page, analyze the text, and split the PDF into individual letters named using the date, taxpayer name, and notice type.

```bash
python -m src.main merged_notices.pdf output_dir
```

Each resulting file will be named in the format `YYMMDD Taxpayer Name - IRSNOTICE.pdf`.
