from functions_stats import parse_tags, get_tag_counts, tag_dict_organiser, generate_pie_chart, generate_bar_chart
from functions_core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df

import os
import streamlit as st
import plotly.express as px

# Streamlit App
st.title("Analyse Tag Distribution")

# Input fields for user
st.sidebar.header("Input Parameters")
path = st.sidebar.text_input("Enter the file path:", r'"/home/timot/workspace/github.com/Anki_Ref_Stats"')
filename = st.sidebar.text_input("Enter the plaintext file name (without extension):", 'All_Decks_Cards')
full_path = os.path.join(path.strip('"'), filename + ".txt")

number_of_tags = st.sidebar.text_input("Enter the desired number of tags to view: ", "10")
try: 
    number_of_tags = int(number_of_tags)
except:
    number_of_tags = ""

target_tags = st.sidebar.text_input("Enter tags to include in pie chart: ", "Review,Mechanism,Photochemistry").split(",")
if target_tags == ['']:
    target_tags = []


# Display in Streamlit
if st.sidebar.button("Generate Pie Chart"):
    st.subheader(f"Showing distribution of Tags")
    pie_chart = generate_pie_chart(full_path, tags=target_tags, number=number_of_tags)
    st.plotly_chart(pie_chart, use_container_width=True)


if st.sidebar.button("Generate Bar Chart"):
    st.subheader(f"Showing distribution of Tags")
    bar_chart = generate_bar_chart(full_path, tags=target_tags, number=number_of_tags)
    st.plotly_chart(bar_chart, use_container_width=True)