import pytest
from src.main import remove_header_blocks, remove_footer_blocks, delete_lines_before_3_1

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
