"""Entry point for the scanned notices parser."""

import argparse
import logging

from .letter_splitter import analyze_pdf, split_letters


def parse_notices(input_path: str, output_dir: str) -> None:
    """Parse scanned notices and split them into individual letters."""

    created = split_letters(input_path, output_dir)
    for fpath in created:
        print(f"Created {fpath}")

def main() -> None:
    """Command-line interface for the parser."""
    parser = argparse.ArgumentParser(description="Parse scanned notice documents")
    parser.add_argument("path", help="Path to merged notice PDF")
    parser.add_argument(
        "output",
        help="Directory where individual letters will be written",
        default="output",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug messages",
    )
    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Output OCR text for each page and exit",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(message)s")

    if args.analyze:
        analyze_pdf(args.path)
        return

    parse_notices(args.path, args.output)


if __name__ == "__main__":
    main()
