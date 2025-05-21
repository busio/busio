"""Entry point for the scanned notices parser."""

import argparse


def parse_notices(input_path: str) -> None:
    """Placeholder function for parsing scanned notice documents.

    Args:
        input_path: Path to the file or directory containing notices.
    """
    # TODO: Implement parsing logic using pytesseract and pdfplumber
    print(f"Parsing notices from {input_path}")


def main() -> None:
    """Command-line interface for the parser."""
    parser = argparse.ArgumentParser(description="Parse scanned notice documents")
    parser.add_argument("path", help="Path to notice file or directory")
    args = parser.parse_args()

    parse_notices(args.path)


if __name__ == "__main__":
    main()
