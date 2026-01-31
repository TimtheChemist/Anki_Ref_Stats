from functions_doi import parse_doi, get_list_of_papers, map_doi_to_title, get_range_of_papers
from functions_textbook import parse_textbook, get_list_of_textbooks, get_range_of_textbooks
import re
import io
import pandas as pd
import streamlit as st

def generate_paper_frequencies(filename, ref_range, target_tags=[], nontarget_tags=[]):
    """
    Finds the top n most frequently occurring DOI's from a file, filtered by target and nontarget tags.
    
    Args:
        filename: Path to the file to be parsed
        ref_range: (start, end) tuple of occurrences to return
        target_tags: List of tags that must be present in a reference
        nontarget_tags: List of tags that must not be present in a reference
    
    Returns:
        Returns the top n to m DOI's with their corresponding titles and counts
    """
    list_of_paper_references = parse_doi(filename, target_tags = target_tags, nontarget_tags = nontarget_tags)
    if list_of_paper_references == None:
        return ""
    
    doi_to_title_dict = map_doi_to_title(list_of_paper_references)

    full_reference_list = get_list_of_papers(list_of_paper_references)

    return get_range_of_papers(ref_range, full_reference_list, doi_to_title_dict)


def convert_string_to_df(input_string):
    if not input_string or input_string.strip() == "":
        return pd.DataFrame()  # Return an EMPTY DataFrame instead of None

    rows = []
    df = pd.DataFrame()
    lines = [line.strip() for line in input_string.strip().split('\n') if line.strip()]
    
    is_paper = True

    if " - DOI: " not in lines[0]:
        is_paper = False

    if is_paper:
        for line in lines:
            try:
                # 1. Extract the number at the start (e.g., "37")
                # Splits at the first "." and takes the first part
                no_part, rest = line.split('.', 1)
                
                # 2. Extract the Title and everything after
                # Splits at " - DOI: "
                title, doi_and_notes = rest.split(' - DOI: ', 1)
                
                # 3. Separate the DOI from the notes
                # Splits at " (" to isolate the DOI from the "(22 notes)" part
                doi, notes_part = doi_and_notes.split(' (', 1)
                
                # 4. Extract just the number from the notes (e.g., "22")
                notes_written = notes_part.replace(' notes)', '').strip()
                
                rows.append({
                    "No.": no_part.strip(),
                    "Notes": notes_written,
                    "Title": title.strip(),
                    "DOI": doi.strip()
                })

                # Create DataFrame from list of dictionaries
                df = pd.DataFrame(rows)

                # Ensure the columns are in your exact requested order
                df = df[["No.", "Notes", "Title", "DOI"]]
                if not rows:
                    return pd.DataFrame()

            except ValueError:
                # Skip lines that don't match the expected "Number. Title - DOI: DOI (notes)" format
                continue
    
    else:
        for line in lines:
            try:
                # 1. Extract the number at the start (e.g., "37")
                # Splits at the first "." and takes the first part
                no_part, rest = line.split('.', 1)
                
                # 2. Extract the Title and everything after
                # Splits at " - DOI: "
                title, notes_part = rest.rsplit(' (', 1)
                
                # 3. Extract just the number from the notes (e.g., "22")
                notes_written = notes_part.replace(' notes)', '').strip()
                
                rows.append({
                    "No.": no_part.strip(),
                    "Notes": notes_written,
                    "Title": title.strip(),
                })

                # Create DataFrame from list of dictionaries
                df = pd.DataFrame(rows)

                # Ensure the columns are in your exact requested order
                df = df[["No.", "Notes", "Title"]]
                if not rows:
                    return pd.DataFrame()

            except ValueError:
                # Skip lines that don't match the expected "Number. Title - DOI: DOI (notes)" format
                continue

    
    return df


def generate_textbook_frequencies(filename, ref_range, target_tags=[], nontarget_tags=[]):
    """
    Finds the top n most frequently occurring textbook titles from a file, filtered by target and nontarget tags.
    
    Args:
        filename: Path to the file to be parsed
        ref_range: (start, end) tuple of occurrences to return
        target_tags: List of tags that must be present in a reference
        nontarget_tags: List of tags that must not be present in a reference
    
    Returns:
        Returns (and prints) the top n to m textbooks with their corresponding counts
    """
    list_of_textbook_references = parse_textbook(filename, target_tags = target_tags, nontarget_tags = nontarget_tags)

    full_textbook_list = get_list_of_textbooks(list_of_textbook_references)
    return get_range_of_textbooks(ref_range, full_textbook_list)



def get_textbooks_by_note_range(filename, range_of_notes, target_tags=[], nontarget_tags=[]):
    """
    Find all textbooks with n to m notes from a list of (Title, count) tuples.
    
    Args:
        filename: Path to the file to be parsed
        range_of_notes: (min, max) tuple of number of notes to filter textbooks
        target_tags: List of tags that must be present in a reference
        nontarget_tags: List of tags that must not be present in a reference

    Returns:
        Returns (and prints) all textbooks with note counts within the specified range
    """
    try:
        list_of_textbook_references = parse_textbook(filename, target_tags = target_tags, nontarget_tags = nontarget_tags)
        full_textbook_list = get_list_of_textbooks(list_of_textbook_references)

        message = ""
        for rank in range(0, len(full_textbook_list)):
            if full_textbook_list[rank][1] >= range_of_notes[0] and full_textbook_list[rank][1] <= range_of_notes[1]:
                print(f"{rank+1}. {full_textbook_list[rank][0]} ({full_textbook_list[rank][1]} notes)")
                message += f"{rank+1}. {full_textbook_list[rank][0]} ({full_textbook_list[rank][1]} notes)\n"
        
        return message

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")



def get_papers_by_note_range(filename, range_of_notes, target_tags=[], nontarget_tags=[]):
    """
    Find all textbooks with n to m notes from a list of (Title, count) tuples.
    
    Args:
        filename: Path to the file to be parsed
        range_of_notes: (min, max) tuple of number of notes to filter papers
        target_tags: List of tags that must be present in a reference
        nontarget_tags: List of tags that must not be present in a reference

    Returns:
        Returns (and prints) all papers with note counts within the specified range
    """
    try:
        list_of_paper_references = parse_doi(filename, target_tags = target_tags, nontarget_tags = nontarget_tags)
        full_paper_list = get_list_of_papers(list_of_paper_references)

        dict_of_references = map_doi_to_title(list_of_paper_references)

        message = ""
        for rank in range(0, len(full_paper_list)):
            if full_paper_list[rank][1] >= range_of_notes[0] and full_paper_list[rank][1] <= range_of_notes[1]:
                title = dict_of_references.get(full_paper_list[rank][0], "Title not found")
                print(f"{rank+1}. {title} - DOI: {full_paper_list[rank][0]} ({full_paper_list[rank][1]} notes)")
                message += f"{rank+1}. {title} - DOI: {full_paper_list[rank][0]} ({full_paper_list[rank][1]} notes)\n"
        
        return message

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except re.error as e:
        print(f"Error: Invalid regex pattern - {e}")
    except Exception as e:
        print(f"Error reading file: {e}")


def convert_df_to_excel(df):

    output = io.BytesIO()
    # Use XlsxWriter as the engine
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Anki_Stats')
        
        # Access the xlsxwriter workbook and worksheet objects
        workbook  = writer.book
        worksheet = writer.sheets['Anki_Stats']

        # Define a format (Bold, Background Color, Border)
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter', # Vertically centered
            'align': 'center',  # Horizontally centered
            'fg_color': '#FFBF00',
            'border': 1
        })

        # Apply the format to the headers manually
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Set column widths
        worksheet.set_column('A:A', 5)
        worksheet.set_column('C:C', 5)
        worksheet.set_column('C:C', 110)
        worksheet.set_column('D:D', 25)

        # Create the format for the data cells of Columns A and B
        center_data_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter'
        })

        # Apply the above format to Columns A and B
        # Syntax: set_column(first_col, last_col, width, cell_format)
        # Pass None for width if you want to keep the default width.
        worksheet.set_column('A:B', None, center_data_format)

    return output.getvalue()
