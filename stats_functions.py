from collections import Counter
import re

journal_list = []

def parse_tags(filename):
    """
    Parse a plaintext file and extract matches for tags.
    
    Args:
        filename: Path to the plaintext file to parse
    
    Returns:
        A list of of all tags (including duplicates) found in the file
    """
    list_of_tags = []
    # Matches the Tags header specifically
    header_pattern = r"<strong>\s*Tags:\s*<\/strong>"

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # We iterate line by line for maximum simplicity and memory efficiency
            lines = file.readlines()
            
            for i in range(len(lines)):
                # If we find the "Tags:" header...
                if re.search(header_pattern, lines[i]):
                    # ...check if there is a next line available
                    if i + 1 < len(lines):
                        tag_line = lines[i+1].strip()
                        
                        # 1. Strip any unexpected HTML tags (safety measure)
                        clean_line = re.sub(r'<[^>]+>', '', tag_line)
                        
                        # 2. Split by whitespace to get individual tags
                        # This handles "Complex HTE" -> ["Complex", "HTE"]
                        # It also handles "Journal::ACS::OrganicLetters" as one tag
                        clean_line = clean_line.replace('"', "")
                        individual_tags = clean_line.split()
                        
                        # 3. Add to our master list
                        list_of_tags.extend(individual_tags)
          
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
        list_of_tags: A list of tags (strings) to analyse
        n: Number of top occurrences to return
    
    Returns:
        A dict containing tag-count key-value pairs sorted by frequency in descending order
    """
    dict_of_tags = {}
    if not list_of_tags:
        return []
    
    if len(list_of_tags) < 1:
        return []
    
    # Count occurrences of each string
    counter = Counter(list_of_tags)
    
    # Get the top n most common strings
    top_n = counter.most_common(len(list_of_tags))

    for tag, count in top_n:
        dict_of_tags[tag] = count
    
    return dict_of_tags


def tag_dict_organiser(dict_of_tags):
    all_journal_tags = {}
    journal_parent_tags = {}
    journal_terminal_tags = {}
    list_of_parent_journals = ["Journal::ACS", "Journal::Elsevier", "Journal::Wiley", "Journal::SpringerNat", "Journal::Thieme"]

    for tag in dict_of_tags:
        if "Journal::" in tag:
            all_journal_tags[tag] = dict_of_tags[tag]

    for tag in all_journal_tags:
        if tag in list_of_parent_journals:
            continue
        else:
            journal_terminal_tags[tag] = all_journal_tags[tag]
                
    for tag in all_journal_tags:
        if tag in list_of_parent_journals:
            journal_parent_tags[tag] = all_journal_tags[tag]

    print(all_journal_tags)
    print(journal_parent_tags)
    print(journal_terminal_tags)

    return all_journal_tags, journal_parent_tags, journal_terminal_tags