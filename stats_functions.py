from collections import Counter
import re

journal_list = []

def parse_tags(filename):
    """
    Parse a plaintext file and extract matches for textbook references.
    
    Args:
        filename: Path to the plaintext file to parse
        target_tags: List of tags to filter references. Only references containing all specified tags will be included.
    
    Returns:
        A list of of all references (including duplicates) found in the file
    """
    list_of_tags = []
    note_separator = r'\n(?=")' 
    tag_pattern = r"<strong>\s*Tags:\s*<\/strong>\s*(.+?)(?=\s*<hr>|$)"

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        notes = re.split(note_separator, content)
        
        for note in notes:
            clean_note = note.replace('""', '"').replace('\xa0', ' ')
            
            # 1. Capture the entire block of tags
            tag_match = re.search(tag_pattern, clean_note, flags=re.DOTALL)
            
            if tag_match:
                # This is the "Combined" string: "Chemistry Economics Economics::Microeconomics"
                raw_tags_block = tag_match.group(1).strip()
                
                # 2. Split the block by whitespace into a list of individual tags
                # Result: ["Chemistry", "Economics", "Economics::Microeconomics"]
                individual_tags = raw_tags_block.split()
                
                # 3. Use .extend() to add each tag individually to your master list
                list_of_tags.extend(individual_tags)
          
        print(list_of_tags)
        print(f"Total tag instances found: {len(list_of_tags)}")
        print(f"Unique tags found: {len(set(list_of_tags))}")
        return list_of_tags

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")


def get_tag_counts(list_of_tags):
    """
    Find the top n most frequently occurring textbooks from a list.
    
    Args:
        list_of_textbooks: A list of textbooks (strings) to analyse
        n: Number of top occurrences to return
    
    Returns:
        A list of tuples containing (string, count) sorted by frequency in descending order
    """

    if not list_of_tags:
        return []
    
    if len(list_of_tags) < 1:
        return []
    
    # Count occurrences of each string
    counter = Counter(list_of_tags)
    
    # Get the top n most common strings
    top_n = counter.most_common(len(list_of_tags))
    
    return top_n