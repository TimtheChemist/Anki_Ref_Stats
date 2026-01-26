from functions_core import generate_paper_frequencies, generate_textbook_frequencies, get_textbooks_by_note_range, get_papers_by_note_range, convert_string_to_df
import os
import streamlit as st


# Streamlit App
st.title("Anki Reference Parser")

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
range_of_references = st.sidebar.text_input("Enter the range of references (e.g., enter '1, 20' if you want to see the 1st to 20th most frequently cited references): ", "1, 20").split(",")
range_of_references = (int(range_of_references[0]), int(range_of_references[1]))

range_of_notes = st.sidebar.text_input("Enter the range of notes for filtering references (e.g., enter '10, 30' if you want to see all references that may be found in 10 to 30 notes): ", "10, 30").split(",")
range_of_notes = (int(range_of_notes[0]), int(range_of_notes[1]))

target_tags = st.sidebar.text_input("Enter the tags for matching: ", "Review").split(",")
if target_tags == ['']:
    target_tags = []

nontarget_tags = st.sidebar.text_input("Enter the tags for exclusion: ", "").split(",")
if nontarget_tags == ['']:
    nontarget_tags = []

# Buttons to trigger functions
if st.sidebar.button("Generate Paper Frequencies"):
    st.subheader(f"Showing the Top {range_of_references[0]} to {range_of_references[1]} Papers")
    reference_df = convert_string_to_df(generate_paper_frequencies(file_input, range_of_references, target_tags=target_tags, nontarget_tags=nontarget_tags))
    st.dataframe(reference_df, hide_index=True)

if st.sidebar.button("Generate Textbook Frequencies"):
    st.subheader(f"Showing the Top {range_of_references[0]} to {range_of_references[1]} Textbooks")
    reference_df = convert_string_to_df(generate_textbook_frequencies(file_input, range_of_references, target_tags=target_tags, nontarget_tags=nontarget_tags))
    st.dataframe(reference_df, hide_index=True)

if st.sidebar.button("Get Papers by Note Range"):
    if range_of_notes[0] > range_of_notes[1]:
        st.error("Error: The first number in the range must be less than or equal to the second number.")

    elif range_of_notes[0] == range_of_notes[1]:
        st.subheader(f"Showing papers that appear in exactly {range_of_notes[0]} notes")
        reference_df = convert_string_to_df(get_papers_by_note_range(file_input, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags))
        st.dataframe(reference_df, hide_index=True)

    else:
        st.subheader(f"Showing papers that appear in {range_of_notes[0]} to {range_of_notes[1]} notes")
        reference_df = convert_string_to_df(get_papers_by_note_range(file_input, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags))
        st.dataframe(reference_df, hide_index=True)

if st.sidebar.button("Get Textbooks by Note Range"):
    if range_of_notes[0] > range_of_notes[1]:
        st.error("Error: The first number in the range must be less than or equal to the second number.")
    
    elif range_of_notes[0] == range_of_notes[1]:
        st.subheader(f"Showing textbooks that appear in exactly {range_of_notes[0]} notes")
        reference_df = convert_string_to_df(get_textbooks_by_note_range(file_input, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags))
        st.dataframe(reference_df, hide_index=True)

    else:
        st.subheader(f"Showing textbooks that appear in {range_of_notes[0]} to {range_of_notes[1]} notes")
        reference_df = convert_string_to_df(get_textbooks_by_note_range(file_input, range_of_notes, target_tags=target_tags, nontarget_tags=nontarget_tags))
        st.dataframe(reference_df, hide_index=True)
