from stats_functions import parse_tags, get_tag_counts, tag_dict_organiser
from core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range

import os
import streamlit as st


# Streamlit App
st.title("Anki Reference Parser")

# Input fields for user
st.sidebar.header("Input Parameters")
path = st.sidebar.text_input("Enter the file path:", r'"/home/timot/workspace/github.com/Anki_Ref_Stats"')
filename = st.sidebar.text_input("Enter the plaintext file name (without extension):", 'All_Decks_Cards.txt')
full_path = os.path.join(path.strip('"'), filename)

range_of_references = st.sidebar.text_input("Enter the range of references (by occurrence): ", "1, 20").split(",")
range_of_references = (int(range_of_references[0]), int(range_of_references[1]))

range_of_notes = st.sidebar.text_input("Enter the range of notes for filtering textbooks/papers: ", "10, 30").split(",")
range_of_notes = (int(range_of_notes[0]), int(range_of_notes[1]))

target_tags = st.sidebar.text_input("Enter the tags for matching: ", "Review").split(",")
if target_tags == ['']:
    target_tags = []

nontarget_tags = st.sidebar.text_input("Enter the tags for exclusion: ", "").split(",")
if nontarget_tags == ['']:
    nontarget_tags = []

# Buttons to trigger functions
if st.sidebar.button("Generate Paper Frequencies"):
    st.subheader("Top Paper Frequencies")
    st.write(generate_paper_frequencies(full_path, range_of_references, target_tags=target_tags, nontarget_tags=nontarget_tags))

if st.sidebar.button("Generate Textbook Frequencies"):
    st.subheader("Top Textbook Frequencies")
    st.write(generate_textbook_frequencies(full_path, range_of_references, target_tags=target_tags, nontarget_tags=nontarget_tags))

if st.sidebar.button("Get Textbooks by Note Range"):
    st.subheader("Textbooks by Note Range")
    st.write(get_textbooks_by_note_range(full_path, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags))

if st.sidebar.button("Get Papers by Note Range"):
    st.subheader("Papers by Note Range")
    st.write(get_papers_by_note_range(full_path, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags))

