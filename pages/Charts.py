from functions_tag_charts import parse_tags, get_tag_counts, tag_dict_organiser, generate_pie_chart, generate_bar_chart
from functions_core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df

import os
import streamlit as st
import plotly.express as px

# Streamlit App
st.title("Analyse Tag Distribution")

# Create the GUI uploader
file_input = st.file_uploader("Choose a plaintext file", type=["txt", "md"])
st.sidebar.header("Input Parameters")

if file_input is not None:
    st.success("File uploaded successfully!")

    # Remove default values in file path input fields
    filename = st.sidebar.text_input("Enter the plaintext file name (without extension):")
    path = st.sidebar.text_input("Enter the file path:")

else:
    # Add default values for file path input fields
    path = st.sidebar.text_input("Enter the file path:", r'"/home/timot/workspace/github.com/Anki_Ref_Stats"')
    filename = st.sidebar.text_input("Enter the plaintext file name (without extension):", 'All_Decks_Cards')

if not (path == "" or filename == ""):
    file_input = os.path.join(path.strip('"'), filename + ".txt")

# Other input fields for user
number_of_tags = st.sidebar.text_input("Enter the max number of tags to view: ", "10")
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
    pie_chart = generate_pie_chart(file_input, tags=target_tags, number=number_of_tags)
    st.plotly_chart(pie_chart, use_container_width=True)


if st.sidebar.button("Generate Bar Chart"):
    st.subheader(f"Showing distribution of Tags")
    bar_chart = generate_bar_chart(file_input, tags=target_tags, number=number_of_tags)
    st.plotly_chart(bar_chart, use_container_width=True)