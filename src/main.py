"""Entry point for the scanned notices parser."""

import argparse
import os

from .letter_splitter import split_letters


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
    args = parser.parse_args()

    parse_notices(args.path, args.output)


if __name__ == "__main__":
    main()
