from collections import Counter
import re
import streamlit as st
import plotly.express as px
import pandas as pd

def parse_tags(file_input):
    """
    Parse a plaintext file and extract matches for tags.
    
    Args:
        file_input: Path to the plaintext file to parse or a file object
    
    Returns:
        A list of of all tags (including duplicates) found in the file
    """
    list_of_tags = []
    # Matches the Tags header specifically
    header_pattern = r"<strong>\s*Tags:\s*<\/strong>"

    try:
         # If it's a path, open it; if it's an uploaded file, just read it
        if isinstance(file_input, str):
            with open(file_input, 'r', encoding='utf-8') as file:
                lines = file.readlines()
        else:
            # We read the bytes, decode to string, then split into lines
            content = file_input.getvalue().decode("utf-8")
            lines = content.splitlines()

            
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
    Find the top n most frequently occurring tags from a list of a tags.
    
    Args:
        list_of_tags: A list of tags (strings) to analyse
    
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


def tag_dict_organiser(file_input):
    tag_list = parse_tags(file_input)
    tag_counts_dict = get_tag_counts(tag_list)

    all_journal_tags = {}
    journal_parent_tags = {}
    journal_terminal_tags = {}
    list_of_parent_journals = ["Journal::ACS", "Journal::Elsevier", "Journal::Wiley", "Journal::SpringerNat", "Journal::Thieme"]

    for tag in tag_counts_dict:
        if "Journal::" in tag:
            all_journal_tags[tag] = tag_counts_dict[tag]

    for tag in all_journal_tags:
        if tag in list_of_parent_journals:
            continue
        else:
            journal_terminal_tags[tag] = all_journal_tags[tag]
                
    for tag in all_journal_tags:
        if tag in list_of_parent_journals:
            journal_parent_tags[tag] = all_journal_tags[tag]

  
    string_of_terminal_journals = ",".join(journal_terminal_tags.keys())

    return string_of_terminal_journals


def generate_pie_chart(file_input, tags=[], number=""):
    """
    Generate a pie chart of tag distribution from the given file.
    
    Args:
        file_input: Path to the plaintext file to parse or a file object
        tags: List of tags to include in the pie chart. If empty, include all tags.
        number: Maximum number of tags to display. If empty, display all tags.

    Returns:
        A plotly pie chart of tag distribution 
    """
    tag_list = parse_tags(file_input)
    tag_counts_dict = get_tag_counts(tag_list)

    if tags:
        # Convert your target tags to lowercase once for efficiency
        tags = {t.lower() for t in tags}
        # Filter the tag_counts_dict to include only specified tags
        tag_counts_dict = {tag: count for tag, count in tag_counts_dict.items() if tag.lower() in tags}
    
    if isinstance(number, int):
        tag_counts_dict = dict(Counter(tag_counts_dict).most_common(number))

    df = pd.DataFrame.from_dict(tag_counts_dict, orient='index', columns=['No. of Notes'])
    df = df.reset_index().rename(columns={'index': 'Tag'})

    # Create the pie chart
    pie_chart = px.pie(df, values='No. of Notes', names='Tag', title='Tag Distribution in Anki Note Collection')
    
    return pie_chart


def generate_bar_chart(file_input, tags=[], number=""):
    """
    Generate a bar chart of tag distribution from the given file.
    
    Args:
        file_input: Path to the plaintext file to parse or a file object
        tags: List of tags to include in the bar chart. If empty, include all tags.
        number: Maximum number of tags to display. If empty, display all tags.

    Returns:
        A plotly bar chart of tag distribution 
    """
    tag_list = parse_tags(file_input)
    tag_counts_dict = get_tag_counts(tag_list)

    if tags:
        # Convert your target tags to lowercase once for efficiency
        tags = {t.lower() for t in tags}
        # Filter the tag_counts_dict to include only specified tags
        tag_counts_dict = {tag: count for tag, count in tag_counts_dict.items() if tag.lower() in tags}
    
    if isinstance(number, int):
        tag_counts_dict = dict(Counter(tag_counts_dict).most_common(number))

    df = pd.DataFrame.from_dict(tag_counts_dict, orient='index', columns=['No. of Notes'])
    df = df.reset_index().rename(columns={'index': 'Tag'})

    # Create the bar chart
    bar_chart = px.bar(
        df, 
        x='Tag', 
        y='No. of Notes', 
        title='Tag Distribution in Anki Note Collection',
        labels={'No. of Notes': 'Number of Notes', 'Tag': 'Category'},
        color='No. of Notes', # Optional: adds a color gradient
        color_continuous_scale=px.colors.sequential.Viridis
    )
    
    return bar_chart