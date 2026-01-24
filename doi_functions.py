
from collections import Counter
import re


def parse_doi(filename, target_tags = [], nontarget_tags = []):
    """
    Parse a plaintext file and extract paper references.
    
    Args:
        filename: Path to the plaintext file to parse
        target_tags: List of tags to filter references. Only references containing all specified tags will be included.
    
    Returns:
        A list of tuples (title, doi) of all references found in the file
    """
    list_of_references = []
    
    # Updated: Matches any newline followed by a quote (start of a new note)
    card_separator = r'\n(?=")' 
    
    # DOI Pattern: Handles nested parentheses within the DOI string
    # Group 1: Title
    # Group 2: DOI
    doi_pattern = r"<b>Reference(?:\s*\d+)?:\s*<\/b>\s*((?:(?!<b>Reference).)+?)\s*\(DOI:\s*(10\.\d{4,9}/(?:[^)]|\([^)]*\))+)\)"
   
    # Pattern for Tags
    tag_pattern = r"<strong>\s*Tags:\s*<\/strong>\s*(.+?)(?=\s*<hr>|$)"

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            cards = re.split(card_separator, content)

        for card in cards:
            # Use finditer to loop through every match found in the content
            for match in re.finditer(doi_pattern, card):
                tag_match = re.search(tag_pattern, card, flags=re.DOTALL)
                raw_tags = tag_match.group(1).strip() if tag_match else ""
                
                if target_tags == [] and nontarget_tags == []:
                    list_of_references.append((match.group(1).strip(), match.group(2).strip()))
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
                        list_of_references.append((match.group(1).strip(), match.group(2).strip()))


        # Display results for verification
        if not list_of_references:
            print("No references found.")

        # Remove Synfacts references (which are duplicated with the original paper) and buggy DOIs
        for ref in list_of_references:
            if "Synfacts" in ref[0] or "10.1002/(SICI" in ref[1]:
                list_of_references.remove(ref)

        return list_of_references


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")
    


def map_doi_to_title(list_of_references):
    """
    Converts a list of (title, doi) tuples into a dictionary of {doi: title}.
    Duplicates are automatically handled (the last title encountered for a DOI is kept).
    """
    doi_dict = {}
    # Using a dictionary comprehension to swap (title, doi) -> {doi: title}
    for item in list_of_references:
        doi_dict[item[1]] = item[0]
    
    return doi_dict


def get_list_of_papers(list_of_references):
    """
    Convert a list of (Title, DOI) tuples to a sorted list of (DOI, count) tuples.
    
    Args:
        list_of_references: A list of tuples (title, doi) of references
    
    Returns:
        A list of tuples containing (DOI string, count) sorted by frequency in descending order
    """
    string_list = []
    for tup in list_of_references:
        string_list.append(tup[1])

    if not string_list:
        return []
    
    if len(list_of_references) < 1:
        return []
    
    # Count occurrences of each string
    counter = Counter(string_list)
    
    # Get the top n most common strings
    sorted_references_list = counter.most_common(len(set(string_list)))
    
    return sorted_references_list


def get_range_of_papers(ref_range, sorted_references_list, dict_of_references):
    """
    Find the nth to mth most frequently occurring DOI's from a list of (Title, count) tuples.
    
    Args:
        ref_range: (start, end) tuple of occurrences to return
        sorted_references list: A list of tuples containing (DOI string, count) sorted by frequency in descending order
        dict_of_references: A dictionary mapping DOI strings to paper titles

    Returns:
        A list of tuples containing (DOI string, count) sorted by frequency in descending order
    """
    message = ""
    for rank in range(ref_range[0], ref_range[1]+1):
        if rank > len(sorted_references_list):
            print(f"Warning: Requested range {ref_range} exceeds available references ({len(sorted_references_list)}). Adjusting end to {len(sorted_references_list)}.")
            ref_range = (ref_range[0], len(sorted_references_list))
            break
    
        title = dict_of_references.get(sorted_references_list[rank][0], "Title not found")
        print(f"{rank}. {title} - DOI: {sorted_references_list[rank][0]} - Count: {sorted_references_list[rank][1]}")
        message += f"{rank}. {title} - DOI: {sorted_references_list[rank][0]} - Count: {sorted_references_list[rank][1]}\n"
    
    return message