
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
    Find the top n most frequently occurring textbooks from a list.
    
    Args:
        list_of_textbooks: A list of textbooks (strings) to analyse
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


def get_textbook_title(top_references_list):
    rank = 0
    for tup in top_references_list:
        rank += 1
        print(f"{rank}. {tup[0]} - Count: {tup[1]}")