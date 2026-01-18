
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
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        pattern = r"<b>Reference(?:\s*\d+)?:\s*<\/b>\s*((?:(?!<b>Reference).)+?)\s*\(DOI:\s*(10\.\d{4,9}/(?:[^)]|\([^)]*\))+)\)[\s\S]*?<strong>\s*Tags:\s*<\/strong>\s*(.+?)(?=\s*<hr>|$)"

        list_of_references = []

        # Use finditer to loop through every match found in the content
        for match in re.finditer(pattern, content):
            raw_tags = match.group(3).strip()
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

        return list_of_references


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")
    


def map_doi_to_title(reference_tuples):
    """
    Converts a list of (title, doi) tuples into a dictionary of {doi: title}.
    Duplicates are automatically handled (the last title encountered for a DOI is kept).
    """
    doi_dict = {}
    # Using a dictionary comprehension to swap (title, doi) -> {doi: title}
    for item in reference_tuples:
        doi_dict[item[1]] = item[0]
    
    return doi_dict


def get_top_n_papers(reference_tuples, n):
    """
    Find the top n most frequently occurring DOI's from a list of (Title, DOI) tuples.
    
    Args:
        string_list: A list of strings to analyse
        n: Number of top occurrences to return
    
    Returns:
        A list of tuples containing (string, count) sorted by frequency in descending order
    """
    string_list = []
    for tup in reference_tuples:
        string_list.append(tup[1])

    if not string_list:
        return []
    
    if n < 1:
        return []
    
    # Count occurrences of each string
    counter = Counter(string_list)
    
    # Get the top n most common strings
    top_n = counter.most_common(n)
    
    return top_n


def get_paper_title(top_references_list, dict_of_references):
    rank = 0
    for tup in top_references_list:
        rank += 1
        title = dict_of_references.get(tup[0], "Title not found")
        print(f"{rank}. {title} - DOI: {tup[0]} - Count: {tup[1]}")
