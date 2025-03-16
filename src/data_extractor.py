import csv
import json
import re
from pathlib import Path
from typing import List, Dict

def _process_description_lines(description_lines: List[str]) -> str:
    """Process description lines according to joining rules.
    
    Args:
        description_lines: List of description lines to process
        
    Returns:
        Processed description string with appropriate line joining
    """
    processed_description = ""
    for line in description_lines:
        if any(line.startswith(prefix) for prefix in ["cf. ", "EXAMPLE: ", "Note 1 to entry: "]):
            # Add with newline for special prefixes
            processed_description += f"\n{line}" if processed_description else line
        else:
            # Add with space for normal lines
            processed_description += f" {line}" if processed_description else line
    return processed_description

def extract_words_and_descriptions(text: str) -> List[Dict[str, str]]:
    """Extract words and their descriptions from the text.
    
    The text format should be:
    3.1
    word_name
    description line(s)
    3.2
    word_name
    description line(s)
    ...
    
    Returns:
        List of dictionaries containing 'word_number', 'word', and 'description' keys.
    """
    result = []
    lines = text.split('\n')
    current_word_number = None
    current_word = None
    current_description_lines = []
    
    word_number_pattern = re.compile(r'^3\.\d+$')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if not line:  # Skip empty lines
            i += 1
            continue
            
        if word_number_pattern.match(line):
            # Save previous entry if exists
            if current_word_number and current_word and current_description_lines:
                result.append({
                    'word_number': current_word_number,
                    'word': current_word,
                    'description': _process_description_lines(current_description_lines)
                })
                
            # Start new entry
            current_word_number = line
            current_description_lines = []
            
            # Get word from next line
            i += 1
            if i < len(lines):
                current_word = lines[i].strip()
            i += 1
        else:
            # Add to current description
            if current_word_number and current_word:  # Only add if we have both number and word
                current_description_lines.append(line)
            i += 1
    
    # Add last entry
    if current_word_number and current_word and current_description_lines:
        result.append({
            'word_number': current_word_number,
            'word': current_word,
            'description': _process_description_lines(current_description_lines)
        })
    
    print(f"\nExtracted {len(result)} words")
    return result

def save_as_json(data: List[Dict[str, str]], output_path: Path) -> None:
    """Save data as JSON file.
    
    Args:
        data: List of dictionaries to save
        output_path: Path to save the JSON file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_as_csv(data: List[Dict[str, str]], output_path: Path) -> None:
    """Save data as CSV file.
    
    Args:
        data: List of dictionaries to save
        output_path: Path to save the CSV file
    """
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['word_number', 'word', 'description'])
        writer.writeheader()
        writer.writerows(data)
