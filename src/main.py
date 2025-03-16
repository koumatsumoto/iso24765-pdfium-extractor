from pathlib import Path
from .pdf_processor import (
    extract_text_from_pdf, remove_header_blocks, remove_footer_blocks,
    delete_lines_before_3_1, delete_figure_lines
)
from .data_extractor import extract_words_and_descriptions, save_as_json, save_as_csv

def main():
    """Main function to extract text from ISO 24765 PDF."""
    # PDF からテキスト抽出してテキストファイル保存
    pdf_path = Path(__file__).parent.parent / "data" / "input.pdf"
    text = extract_text_from_pdf(pdf_path)
    text = remove_header_blocks(text)
    text = remove_footer_blocks(text)
    text = delete_lines_before_3_1(text)
    text = delete_figure_lines(text)
    
    output_txt_path = Path(__file__).parent.parent / "data" / "output.txt"
    output_txt_path.write_text(text, encoding='utf-8')
    
    # 単語と説明を抽出して JSON として保存
    words_and_descriptions = extract_words_and_descriptions(text)
    output_json_path = Path(__file__).parent.parent / "data" / "output.json"
    save_as_json(words_and_descriptions, output_json_path)
    
    # CSV として保存
    output_csv_path = Path(__file__).parent.parent / "data" / "output.csv"
    save_as_csv(words_and_descriptions, output_csv_path)

if __name__ == "__main__":
    main()
