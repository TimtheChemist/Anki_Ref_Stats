
from collections import Counter
import re


def parse_textbook(filename, target_tags = []):
    """
    Parse a plaintext file and extract matches for a given regex pattern.
    
    Args:
        filename: Path to the plaintext file to parse
        target_tags: List of tags to filter references. Only references containing all specified tags will be included.
    
    Returns:
        A list of tuples (title, doi) of all references found in the file
    """
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = r"<b>Reference(?:\s*\d+)?:\s*<\/b>\s*(.+?)\s*\|\s*Page\s*(\d+)(?:(?!<b>Reference)[\s\S])*?<strong>\s*Tags:\s*<\/strong>\s*(.+?)(?=\s*<hr>|$)"

        list_of_references = []

        # Use finditer to loop through every match found in the content
        for match in re.finditer(pattern, content):
            raw_tags = match.group(3).strip()
            if target_tags == []:
                continue
            
            is_all_tags_present = True
            for tag in target_tags:
                if tag not in raw_tags:
                    is_all_tags_present = False
                    break

            if is_all_tags_present:
                list_of_references.append(match.group(1).strip())


        # Display results for verification
        if not list_of_references:
            print("No references found.")
        else:
            for entry in list_of_references:
                print(f"Title: {entry}")

        return list_of_references


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")
    


def get_top_n_textbooks(list_of_textbooks, n):
    """
    Find the top n most frequently occurring DOI's from a list of (Title, DOI) tuples.
    
    Args:
        string_list: A list of strings to analyse
        n: Number of top occurrences to return
    
    Returns:
        A list of tuples containing (string, count) sorted by frequency in descending order
    """

    if not list_of_textbooks:
        return []
    
    if n < 1:
        return []
    
    # Count occurrences of each string
    counter = Counter(list_of_textbooks)
    
    # Get the top n most common strings
    top_n = counter.most_common(n)
    
    return top_n
