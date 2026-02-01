from functions_tag_charts import parse_tags, get_tag_counts, tag_dict_organiser
from functions_core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df

import os
import streamlit as st

"""
This is a space to run the program on the command line without using the Streamlit GUI
(e.g., for testing and debugging).
"""


filename = 'All_Decks_Cards.txt'
range_of_papers = (1,20)
range_of_textbooks = (10,25)
range_of_notes = (20,50)


target_tags = ["Typo"]
nontarget_tags = ["Review"]

generate_paper_frequencies(filename, range_of_papers, target_tags, nontarget_tags)

#get_textbooks_by_note_range(filename, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags)
#get_papers_by_note_range(filename, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags)



#generate_textbook_frequencies(filename, range_of_textbooks, target_tags, nontarget_tags)

"""
tag_list = parse_tags('All_Decks_Cards.txt')
tag_counts = get_tag_counts(tag_list)
print(tag_counts)
"""
