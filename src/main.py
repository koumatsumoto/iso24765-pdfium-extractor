import pypdfium2 as pdfium
from pathlib import Path


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract text from PDF file using pypdfium2."""
    pdf = pdfium.PdfDocument(pdf_path)
    text_parts = []

    for page_number in range(len(pdf)):
        page = pdf.get_page(page_number)
        text_page = page.get_textpage()
        text_parts.append(text_page.get_text_range())

    return "\n".join(text_parts)


def main():
    """Main function to extract text from ISO 24765 PDF."""
    pdf_path = Path(__file__).parent.parent / "data" / "input.pdf"
    text = extract_text_from_pdf(pdf_path)
    output_path = Path(__file__).parent.parent / "data" / "output.txt"
    output_path.write_text(text, encoding='utf-8')


if __name__ == "__main__":
    main()
