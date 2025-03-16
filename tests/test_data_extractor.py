import pytest
import json
from pathlib import Path
from src.data_extractor import extract_words_and_descriptions, save_as_json

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
