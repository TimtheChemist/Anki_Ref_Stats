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
    list_of_references = []
    
    # Updated: Matches any newline followed by a quote (start of a new note)
    card_separator = r'\n(?=")' 
    
    # Pattern for Title and Page
    pattern = r"<b>Reference(?:\s*\d+)?:\s*<\/b>\s*(.+?)\s*\|\s*Page\s*(\d+)"
    
    # Pattern for Tags
    tag_pattern = r"<strong>\s*Tags:\s*<\/strong>\s*(.+?)(?=\s*<hr>|$)"

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            cards = re.split(card_separator, content)

        # Use finditer to loop through every match found in the content
        for card in cards:
            for match in re.finditer(pattern, card):
                tag_match = re.search(tag_pattern, card, flags=re.DOTALL)
                raw_tags = tag_match.group(1).strip() if tag_match else ""

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

        return list_of_references


    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")
    

def get_list_of_textbooks(list_of_textbooks):
    """
    Convert a list of textbook title strings to a sorted list of (title, count) tuples.
    
    Args:
        list_of_textbooks: A list of textbook titles (strings) to analyse
    
    Returns:
        A list of tuples containing (string, count) sorted by frequency in descending order
    """

    if not list_of_textbooks:
        return []
    
    if len(list_of_textbooks) < 1:
        return []
    
    # Count occurrences of each string
    counter = Counter(list_of_textbooks)
    
    # Get the top n most common strings
    sorted_list_of_textbooks = counter.most_common(len(set(list_of_textbooks)))
    
    return sorted_list_of_textbooks


def get_range_of_textbooks(ref_range, sorted_list_of_textbooks):
    """
    Find the nth to mth most frequently occurring textbooks from a list of (Title, count) tuples.
    
    Args:
        ref_range: (start, end) tuple of occurrences to return
        sorted_list_oftextbooks: A list of tuples containing (textbook title, count) sorted by frequency in descending order

    Returns:
        A list of tuples containing (DOI string, count) sorted by frequency in descending order
    """
    message = ""
    end_range = ref_range[1]

    if len(sorted_list_of_textbooks) == 0:
        return "No references found matching the specified criteria."

    if len(sorted_list_of_textbooks) < ref_range[1]:
        end_range = len(sorted_list_of_textbooks)
        print(f"Warning: Requested start {ref_range[0]} exceeds available references ({len(sorted_list_of_textbooks)}). Adjusting start to {len(sorted_list_of_textbooks)}.")

    for rank in range(ref_range[0]-1, end_range):
        print(f"{rank+1}. {sorted_list_of_textbooks[rank][0]} ({sorted_list_of_textbooks[rank][1]} notes)")
        message += f"{rank+1}. {sorted_list_of_textbooks[rank][0]} ({sorted_list_of_textbooks[rank][1]} notes)\n"
    
    return message
