import pypdfium2 as pdfium # type: ignore
from pathlib import Path

def is_integer(s: str) -> bool:
    """Check if string represents an integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False

def remove_footer_blocks(text: str) -> str:
    """Remove footer blocks from the text.
    Footer blocks contain:
    - Licensed to ...
    - ISO Store Order: ...
    - Single user licence only, ...
    - ISO/IEC/IEEE 24765:2017(E)
    """
    result = []
    
    # カウンター初期化
    licensed_to_removed = 0
    iso_order_removed = 0
    single_user_removed = 0
    standard_ref_removed = 0
    
    for line in text.split('\n'):
        line = line.strip()
        
        # Skip empty lines
        if not line:
            result.append(line)
            continue
            
        # Check for footer lines
        if line.startswith("Licensed to "):
            licensed_to_removed += 1
            continue
        if line.startswith("ISO Store Order: "):
            iso_order_removed += 1
            continue
        if line.startswith("Single user licence only, "):
            single_user_removed += 1
            continue
        if line == "ISO/IEC/IEEE 24765:2017(E)":
            standard_ref_removed += 1
            continue
            
        result.append(line)
    
    # サマリー出力
    total_removed = licensed_to_removed + iso_order_removed + single_user_removed + standard_ref_removed
    print(f"\nFooter Block Removal Summary:")
    print(f"Total lines removed: {total_removed}")
    print(f"  - Licensed to lines: {licensed_to_removed}")
    print(f"  - ISO Store Order lines: {iso_order_removed}")
    print(f"  - Single user licence lines: {single_user_removed}")
    print(f"  - Standard reference lines: {standard_ref_removed}\n")
    
    return '\n'.join(result)

def remove_header_blocks(text: str) -> str:
    """Remove header blocks from the text.
    Header blocks contain:
    - Page number (integer)
    - © ISO/IEC 2017 – All rights reserved
    - © IEEE 2017 – All rights reserved
    """
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
            page_numbers_removed += 1
            continue
            
        # Check for copyright lines
        if line.startswith("© ISO/IEC 2017"):
            iso_copyright_removed += 1
            continue
        if line.startswith("© IEEE 2017"):
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
    
    return '\n'.join(result)

def delete_figure_lines(text: str) -> str:
    """Delete all lines that start with 'Figure ' and log the number of deleted lines."""
    lines = text.split('\n')
    result = []
    figure_lines_removed = 0
    
    for line in lines:
        line = line.strip()
        if line.startswith("Figure "):
            figure_lines_removed += 1
            continue
        result.append(line)
    
    print(f"\nDeleted {figure_lines_removed} figure reference lines")
    
    return '\n'.join(result)

def delete_lines_before_3_1(text: str) -> str:
    """Delete all lines before the line containing '3.1' and log the number of deleted lines."""
    lines = text.split('\n')
    found_index = -1
    
    for i, line in enumerate(lines):
        if "3.1" in line:
            found_index = i
            break
    
    if found_index == -1:
        print("\nNo line containing '3.1' found. No lines deleted.")
        return text
    
    deleted_lines = found_index
    print(f"\nDeleted {deleted_lines} lines before '3.1'")
    
    return '\n'.join(lines[found_index:])

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
