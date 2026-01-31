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

# Initialise session state for text inputs
if "path" not in st.session_state:
    st.session_state.path = r'"/home/timot/workspace/github.com/Anki_Ref_Stats"'
if "filename" not in st.session_state:
    st.session_state.filename = 'All_Decks_Cards'
if "number_of_tags" not in st.session_state:
    st.session_state.number_of_tags = "15"
if "target_tags" not in st.session_state:
    st.session_state.target_tags = "Review,Mechanism,Photochemistry"

if file_input is not None:
    st.success("File uploaded successfully!")

    # Remove default values in file path input fields
    filename = st.sidebar.text_input("Enter the plaintext file name (without extension):", st.session_state.filename)
    path = st.sidebar.text_input("Enter the file path:", st.session_state.path)

else:
    # Add default values for file path input fields
    path = st.sidebar.text_input("Enter the file path:", st.session_state.path)
    filename = st.sidebar.text_input("Enter the plaintext file name (without extension):", st.session_state.filename)

if not (path == "" or filename == ""):
    file_input = os.path.join(path.strip('"'), filename + ".txt")

# Other input fields for user
number_of_tags = st.sidebar.text_input("Enter the max number of tags to view: ", st.session_state.number_of_tags)
try: 
    number_of_tags = int(number_of_tags)
except (ValueError, IndexError):
    st.sidebar.error("❌ Invalid tag number. Please enter a valid number.")
    range_of_tags = 20 # Provide a safe fallback default

target_tags = st.sidebar.text_input("Enter tags to include in charts: ", st.session_state.target_tags).split(",")
if target_tags == ['']:
    target_tags = []


# Buttons

if st.sidebar.button("Clear Fields"):
    st.session_state.path = ""
    st.session_state.filename = ""
    st.session_state.number_of_tags = ""
    st.session_state.target_tags = ""
    
if st.sidebar.button("Populate with Journal Tags"):
    st.session_state.target_tags = tag_dict_organiser(file_input)   

if st.sidebar.button("Generate Pie Chart"):
    st.subheader(f"Showing distribution of Tags")
    pie_chart = generate_pie_chart(file_input, tags=target_tags, number=number_of_tags)
    st.plotly_chart(pie_chart, use_container_width=True)

if st.sidebar.button("Generate Bar Chart"):
    st.subheader(f"Showing distribution of Tags")
    bar_chart = generate_bar_chart(file_input, tags=target_tags, number=number_of_tags)
    st.plotly_chart(bar_chart, use_container_width=True)