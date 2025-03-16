import pytest
import json
from pathlib import Path
from src.main import (
    remove_header_blocks, remove_footer_blocks, delete_lines_before_3_1,
    extract_words_and_descriptions, save_as_json
)

def test_remove_header_blocks():
    sample_text = "1\n© ISO/IEC 2017 – All rights reserved\n    Some content line\n2\n© IEEE 2017 – All rights reserved\n    Another content line\n3\n    More content"
    expected_result = "Some content line\nAnother content line\nMore content"
    result = remove_header_blocks(sample_text)
    assert result == expected_result

def test_remove_header_blocks_with_empty_lines():
    sample_text = "1\n\n© ISO/IEC 2017 – All rights reserved\n\nSome content line\n\n2\n\n© IEEE 2017 – All rights reserved\n\nAnother content line"
    expected_result = "\n\nSome content line\n\n\n\nAnother content line"  # 空行が保持される
    result = remove_header_blocks(sample_text)
    assert result == expected_result

def test_remove_footer_blocks():
    sample_text = "Some content line\nLicensed to Example Corp\nAnother content line\nISO Store Order: 12345\nContent continues\nSingle user licence only, copying prohibited\nFinal content\nISO/IEC/IEEE 24765:2017(E)"
    expected_result = "Some content line\nAnother content line\nContent continues\nFinal content"
    result = remove_footer_blocks(sample_text)
    assert result == expected_result

def test_delete_lines_before_3_1():
    sample_text = "Line 1\nLine 2\n3.1 Definition\nLine 4\nLine 5"
    expected_result = "3.1 Definition\nLine 4\nLine 5"
    result = delete_lines_before_3_1(sample_text)
    assert result == expected_result

def test_delete_lines_before_3_1_no_match():
    sample_text = "Line 1\nLine 2\nLine 3\nLine 4\nLine 5"
    result = delete_lines_before_3_1(sample_text)
    assert result == sample_text  # テキストは変更されない

def test_delete_lines_before_3_1_with_empty_lines():
    sample_text = "Line 1\n\nLine 2\n\n3.1 Definition\n\nLine 4\n\nLine 5"
    expected_result = "3.1 Definition\n\nLine 4\n\nLine 5"
    result = delete_lines_before_3_1(sample_text)
    assert result == expected_result

def test_remove_footer_blocks_with_empty_lines():
    sample_text = "Some content line\n\nLicensed to Example Corp\n\nAnother content line\n\nISO Store Order: 12345\n\nContent continues\n\nSingle user licence only, copying prohibited\n\nFinal content\n\nISO/IEC/IEEE 24765:2017(E)"
    expected_result = "Some content line\n\n\nAnother content line\n\n\nContent continues\n\n\nFinal content\n"  # 空行が保持される
    result = remove_footer_blocks(sample_text)
    assert result == expected_result

def test_extract_words_and_descriptions():
    sample_text = (
        "3.1\nabstraction\nFirst description line\nSecond description line\n\n"
        "3.2\nactivity\nAnother description\n\n"
        "3.3\nalgorithm\nSingle line description"
    )
    expected_result = [
        {
            'word_number': '3.1',
            'word': 'abstraction',
            'description': 'First description line\nSecond description line'
        },
        {
            'word_number': '3.2',
            'word': 'activity',
            'description': 'Another description'
        },
        {
            'word_number': '3.3',
            'word': 'algorithm',
            'description': 'Single line description'
        }
    ]
    result = extract_words_and_descriptions(sample_text)
    assert result == expected_result

def test_extract_words_and_descriptions_empty_text():
    result = extract_words_and_descriptions("")
    assert result == []

def test_extract_words_and_descriptions_no_valid_words():
    sample_text = "Some text\nwithout any\nvalid word numbers"
    result = extract_words_and_descriptions(sample_text)
    assert result == []

def test_save_as_json(tmp_path):
    data = [
        {
            'word_number': '3.1',
            'word': 'test',
            'description': 'Test description'
        }
    ]
    output_path = tmp_path / "test_output.json"
    save_as_json(data, output_path)
    
    # Check if file exists and content is correct
    assert output_path.exists()
    with open(output_path, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data == data
