from functions_tag_charts import parse_tags, get_tag_counts, tag_dict_organiser, generate_pie_chart, generate_bar_chart
from functions_core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df
from functions_streamlit import clear_fields_charts, populate_journal_tags

import os
import streamlit as st
import plotly.express as px

# Streamlit App
st.title("Analyse Tag Distribution")

# Create the GUI uploader
file_input = st.file_uploader("Choose a plaintext file", type=["txt", "md"])
st.sidebar.header("Input Parameters")

# Initialise session state for text inputs
defaults = {
    "path": r'"/home/timot/workspace/github.com/Anki_Ref_Stats"',
    "filename": 'All_Decks_Cards',
    "number_of_tags": "15",
    "target_tags": "Review,Mechanism,Photochemistry"
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

if file_input is not None:
    st.success("File uploaded successfully!")


path = st.sidebar.text_input("Enter the file path:", value=st.session_state.path)
filename = st.sidebar.text_input("Enter the plaintext file name:", value=st.session_state.filename)


# Logic to decide which file to use
if file_input is not None:
    file_input = file_input 
else:
    file_input = os.path.join(path.strip('"'), filename + ".txt") if path and filename else None
    if file_input:
        if os.path.exists(file_input):
            st.sidebar.success("✅ File found on disk.")
        else:
            st.sidebar.error("❌ File not found. Check path/filename.")
            file_input = None # Prevent analysis buttons from running

# Other input fields for user
number_of_tags = st.sidebar.text_input("Enter the max number of tags to view: ", st.session_state.number_of_tags)
try: 
    number_of_tags = int(number_of_tags)
except (ValueError, IndexError):
    st.sidebar.error("❌ Invalid tag number. Please enter a valid number.")
    range_of_tags = 20 # Provide a safe fallback default

raw_tags = st.sidebar.text_input("Enter tags:", value=st.session_state.target_tags)
target_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]


# Buttons

st.sidebar.button("Clear Fields", on_click=clear_fields_charts)
    
st.sidebar.button("Populate with Journal Tags", on_click=populate_journal_tags, args=(file_input,))

if st.sidebar.button("Generate Pie Chart"):
    if not file_input:
        st.error("Please provide a file first.")
    else:
        st.subheader("Tag Distribution (Pie Chart)")
        fig = generate_pie_chart(file_input, tags=target_tags, number=number_of_tags)
        st.plotly_chart(fig, use_container_width=True)

if st.sidebar.button("Generate Bar Chart"):
    if not file_input:
        st.error("Please provide a file first.")
    else:
        st.subheader(f"Tag Distribution (Bar Chart)")
        bar_chart = generate_bar_chart(file_input, tags=target_tags, number=number_of_tags)
        st.plotly_chart(bar_chart, use_container_width=True)