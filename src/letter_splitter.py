import logging
import os
import re
from datetime import datetime
from typing import List, Tuple

logger = logging.getLogger(__name__)

import pdfplumber
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter


def _extract_text(page: pdfplumber.page.Page) -> str:
    """Return text from the given page using embedded text if available, otherwise OCR."""
    text = page.extract_text() or ""
    if text.strip():
        logger.debug("Using embedded text")
        return text
    logger.debug("No embedded text found, performing OCR")
    img = page.to_image(resolution=300)
    pil_img: Image.Image = img.original
    return pytesseract.image_to_string(pil_img)


def _parse_info(text: str) -> Tuple[str, str, str]:
    """Extract date, taxpayer name and notice name from page text."""
    # Date formats like MM/DD/YY or "Month DD, YYYY"
    date_str = "000000"
    date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{2,4})", text)
    if not date_match:
        date_match = re.search(
            r"((January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4})",
            text,
        )
    if date_match:
        for fmt in ("%m/%d/%Y", "%m/%d/%y", "%B %d, %Y"):
            try:
                dt = datetime.strptime(date_match.group(1), fmt)
                date_str = dt.strftime("%y%m%d")
                break
            except ValueError:
                continue

    name_match = re.search(r"Dear\s+([^\n,:]+)", text)
    name = name_match.group(1).strip().replace(",", "") if name_match else "Unknown"

    notice_match = re.search(r"(CP\d+|Letter\s*\d+|Notice\s+[A-Z0-9]+)", text, re.I)
    notice = notice_match.group(1).replace(" ", "") if notice_match else "IRSNotice"
    logger.debug("Parsed info - date: %s, name: %s, notice: %s", date_str, name, notice)
    return date_str, name, notice


def _is_new_letter(text: str) -> bool:
    """Return True if the text indicates the start of a new letter."""
    return (
        re.search(r"Internal Revenue Service", text, re.I)
        and re.search(r"\bDear\b", text)
    )


def split_letters(input_pdf: str, output_dir: str) -> List[str]:
    """Split the input PDF into per-taxpayer letters.

    Args:
        input_pdf: Path to the merged PDF file.
        output_dir: Directory where individual letters will be stored.

    Returns:
        List of file paths created.
    """
    os.makedirs(output_dir, exist_ok=True)
    created_files: List[str] = []

    with pdfplumber.open(input_pdf) as pdf:
        reader = PdfReader(input_pdf)
        writer = PdfWriter()
        info = None
        start_idx = 0

        for idx, page in enumerate(pdf.pages):
            logger.debug("Processing page %d", idx + 1)
            text = _extract_text(page)
            if info is None:
                info = _parse_info(text)
                writer.add_page(reader.pages[idx])
                continue

            # detect the start of a new letter
            if _is_new_letter(text):
                # save previous letter
                date_str, name, notice = info
                filename = f"{date_str} {name} - {notice}.pdf"
                out_path = os.path.join(output_dir, filename)
                with open(out_path, "wb") as fh:
                    writer.write(fh)
                created_files.append(out_path)
                logger.debug("Wrote %s", out_path)
                writer = PdfWriter()
                info = _parse_info(text)
            writer.add_page(reader.pages[idx])

        if len(writer.pages) > 0 and info:
            date_str, name, notice = info
            filename = f"{date_str} {name} - {notice}.pdf"
            out_path = os.path.join(output_dir, filename)
            with open(out_path, "wb") as fh:
                writer.write(fh)
            created_files.append(out_path)
            logger.debug("Wrote %s", out_path)

    return created_files


def analyze_pdf(input_pdf: str) -> None:
    """Output OCR text for each page of the input PDF for debugging."""
    with pdfplumber.open(input_pdf) as pdf:
        for idx, page in enumerate(pdf.pages):
            logger.info("Page %d", idx + 1)
            text = _extract_text(page)
            logger.info(text)
            logger.info("-" * 40)

