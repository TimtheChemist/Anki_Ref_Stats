from functions_core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df, convert_df_to_excel
from functions_streamlit import download_excel_button, run_safe_analysis, parse_range
import os
import streamlit as st


# Streamlit App
st.title("Anki Reference Parser")

# Create the GUI uploader
file_input = st.file_uploader("Choose a plaintext file", type=["txt", "md"])
st.sidebar.header("Input Parameters")

# Initialise session state for text inputs
defaults = {
    "path": r'"/home/timot/workspace/github.com/Anki_Ref_Stats"',
    "filename": 'All_Decks_Cards',
    "range_of_references": '1,20',
    "range_of_notes": '1,100',
    "target_tags": "",
    "nontarget_tags": ""
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

path = st.sidebar.text_input("Enter the file path:", value=st.session_state.path)
filename = st.sidebar.text_input("Enter the plaintext file name:", value=st.session_state.filename)

# Resolve file input logic
if file_input is not None:
    st.success("File uploaded successfully!")
    
else:
    file_input = os.path.join(path.strip('"'), filename + ".txt") if path and filename else None


# Other input fields for user
range_of_references = st.sidebar.text_input("Enter the range of references (e.g., enter '1, 20' if you want to see the 1st to 20th most frequently cited references): ", value=st.session_state.range_of_references, key = "range_of_references")
range_of_references = parse_range(range_of_references)

range_of_notes = st.sidebar.text_input("Enter the range of notes for filtering references (e.g., enter '10, 30' if you want to see all references that may be found in 10 to 30 notes): ", value=st.session_state.range_of_notes, key = "range_of_notes")
range_of_notes = parse_range(range_of_notes)

raw_target_tags = st.sidebar.text_input("Enter tags:", value=st.session_state.target_tags, key = "target_tags")
target_tags = [t.strip() for t in raw_target_tags.split(",") if t.strip()]

raw_nontarget_tags = st.sidebar.text_input("Enter tags:", value=st.session_state.nontarget_tags, key = "nontarget_tags")
nontarget_tags = [t.strip() for t in raw_nontarget_tags.split(",") if t.strip()]


# Buttons to trigger functions
if st.sidebar.button("Clear Fields"):
    st.session_state.path = ""
    st.session_state.filename = ""
    st.session_state.target_tags = ""
    st.session_state.nontarget_tags = ""
    st.session_state.range_of_references = ""
    st.session_state.range_of_notes = ""
    st.rerun()

if st.sidebar.button("Generate Paper Frequencies"):
    df = run_safe_analysis(generate_paper_frequencies, file_input, range_of_references, target_tags, nontarget_tags)
    
    if df is not None:
        st.subheader(f"Top {range_of_references[0]} to {range_of_references[1]} Papers")
        st.dataframe(df, hide_index=True)
        download_excel_button(convert_df_to_excel(df))


if st.sidebar.button("Generate Textbook Frequencies"):
    df = run_safe_analysis(generate_textbook_frequencies, file_input, range_of_references, target_tags, nontarget_tags)
    
    if df is not None:
        st.subheader(f"Top {range_of_references[0]} to {range_of_references[1]} Textbooks")
        st.dataframe(df, hide_index=True)
        download_excel_button(convert_df_to_excel(df))


if st.sidebar.button("Get Papers by Note Range"):
    df = run_safe_analysis(get_papers_by_note_range, file_input, range_of_notes, target_tags, nontarget_tags)
    
    if df is not None:
        label = f"Papers in exactly {range_of_notes[0]} notes" if range_of_notes[0] == range_of_notes[1] else f"Papers in {range_of_notes[0]} to {range_of_notes[1]} notes"
        st.subheader(label)
        st.dataframe(df, hide_index=True)
        download_excel_button(convert_df_to_excel(df))


if st.sidebar.button("Get Textbooks by Note Range"):
    df = run_safe_analysis(get_textbooks_by_note_range, file_input, range_of_notes, target_tags, nontarget_tags)
    
    if df is not None:
        label = f"Textbooks in exactly {range_of_notes[0]} notes" if range_of_notes[0] == range_of_notes[1] else f"Textbooks in {range_of_notes[0]} to {range_of_notes[1]} notes"
        st.subheader(label)
        st.dataframe(df, hide_index=True)
        download_excel_button(convert_df_to_excel(df))
