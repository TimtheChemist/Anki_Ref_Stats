from stats_functions import parse_tags, get_tag_counts, tag_dict_organiser
from core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df

import os
import streamlit as st


filename = 'All_Decks_Cards.txt'
range_of_papers = (10,50)
range_of_textbooks = (10,25)
range_of_notes = (20,50)


target_tags = []
nontarget_tags = ["Review"]



#get_textbooks_by_note_range(filename, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags)
#get_papers_by_note_range(filename, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags)



#generate_textbook_frequencies(filename, range_of_textbooks, target_tags, nontarget_tags)


tag_list = parse_tags('All_Decks_Cards.txt')
tag_counts = get_tag_counts(tag_list)
print(tag_counts)

all_journal_tags, journal_parent_tags, journal_terminal_tags = tag_dict_organiser(tag_counts)


