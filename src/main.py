import pypdfium2 as pdfium
import logging
from pathlib import Path

def is_integer(s: str) -> bool:
    """Check if string represents an integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False

def remove_header_blocks(text: str) -> str:
    """Remove header blocks from the text.
    Header blocks contain:
    - Page number (integer)
    - © ISO/IEC 2017 – All rights reserved
    - © IEEE 2017 – All rights reserved
    """
    logging.info("Starting header block removal")
    result = []
    
    # カウンター初期化
    page_numbers_removed = 0
    iso_copyright_removed = 0
    ieee_copyright_removed = 0
    
    for line in text.split('\n'):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            result.append(line)
            continue
            
        # Check for page number
        if is_integer(line):
            logging.info(f"Removed page number: {line}")
            page_numbers_removed += 1
            continue
            
        # Check for copyright lines
        if line.startswith("© ISO/IEC 2017"):
            logging.info(f"Removed ISO/IEC copyright line: {line}")
            iso_copyright_removed += 1
            continue
        if line.startswith("© IEEE 2017"):
            logging.info(f"Removed IEEE copyright line: {line}")
            ieee_copyright_removed += 1
            continue
            
        result.append(line)
    
    # サマリー出力
    total_pages = page_numbers_removed
    total_removed = page_numbers_removed + iso_copyright_removed + ieee_copyright_removed
    print(f"\nHeader Block Removal Summary:")
    print(f"Total pages processed: {total_pages}")
    print(f"Total lines removed: {total_removed}")
    print(f"  - Page numbers: {page_numbers_removed}")
    print(f"  - ISO/IEC copyright: {iso_copyright_removed}")
    print(f"  - IEEE copyright: {ieee_copyright_removed}\n")
    
    logging.info(f"Completed header block removal - {total_removed} lines removed from {total_pages} pages")
    return '\n'.join(result)


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text from PDF file using pypdfium2."""
    pdf = pdfium.PdfDocument(pdf_path)
    text_parts = []

    for page_number in range(6, len(pdf) - 12):  # Skip first 6 pages (cover and TOC) and last 12 pages (annexes)
        page = pdf.get_page(page_number)
        text_page = page.get_textpage()
        text = text_page.get_text_range()
        text_parts.append(text)

    return "\n".join(text_parts)


def main():
    """Main function to extract text from ISO 24765 PDF."""
    # Setup logging
    log_path = Path(__file__).parent.parent / "data" / "process.log"
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    pdf_path = Path(__file__).parent.parent / "data" / "input.pdf"
    text = extract_text_from_pdf(pdf_path)
    text = remove_header_blocks(text)
    output_path = Path(__file__).parent.parent / "data" / "output.txt"
    output_path.write_text(text, encoding='utf-8')
    
    logging.info("Text processing completed")


if __name__ == "__main__":
    main()
