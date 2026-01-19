from collections import Counter
import re


def parse_textbook(filename, target_tags = [], nontarget_tags = []):
    """
    Parse a plaintext file and extract matches for textbook references.
    
    Args:
        filename: Path to the plaintext file to parse
        target_tags: List of tags to filter references. Only references containing all specified tags will be included.
    
    Returns:
        A list of of all references (including duplicates) found in the file
    """
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = r"<b>Reference(?:\s*\d+)?:\s*<\/b>\s*(.+?)\s*\|\s*Page\s*(\d+)(?:(?!<b>Reference)[\s\S])*?<strong>\s*Tags:\s*<\/strong>\s*(.+?)(?=\s*<hr>|$)"

        list_of_references = []

        # Use finditer to loop through every match found in the content
        for match in re.finditer(pattern, content):
            raw_tags = match.group(3).strip()
            if target_tags == [] and nontarget_tags == []:
                list_of_references.append((match.group(1).strip()))
                continue
            
            is_target_tags_present = True
            is_nontarget_tags_present = False
            for tag in target_tags:
                if tag not in raw_tags:
                    is_target_tags_present = False
                    break
            if is_target_tags_present:
                for tag in nontarget_tags:
                    if tag in raw_tags:
                        is_nontarget_tags_present = True
                        break
                if not is_nontarget_tags_present:
                    list_of_references.append((match.group(1).strip()))