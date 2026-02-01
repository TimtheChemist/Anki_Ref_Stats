import streamlit as st
import io
import pandas as pd
from functions_core import convert_string_to_df
from functions_tag_charts import tag_dict_organiser

def download_excel_button(excel_data):
    st.download_button(
    label="Download Formatted Excel",
    data=excel_data,
    file_name="List_of_Top_References.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

def run_safe_analysis(func, file_input, range_tuple, target_tags, nontarget_tags):
    """
    Centralised runner to validate input, execute parsing, and handle UI feedback.
    """
    # 1. Validate File Input
    if file_input is None:
        st.error("❌ Please upload a file or provide a valid file path first.")
        return None

    # 2. Validate Range Logic
    if not isinstance(range_tuple, tuple) or len(range_tuple) != 2:
        st.error("❌ Invalid range format")
        return None
        
    if range_tuple[0] > range_tuple[1]:
        st.error("❌ The first number in the range must be less than or equal to the second.")
        return None

    # 3. Execute Core Logic
    try:
        with st.spinner("Parsing references..."):
            raw_result = func(file_input, range_tuple, target_tags=target_tags, nontarget_tags=nontarget_tags)
            df = convert_string_to_df(raw_result)

            if df is None or df.empty:
                st.warning("⚠️ No references were found that match the specified criteria.")
                return None
                
            return df
            
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
        return None


def clear_fields_charts():
    st.session_state.path = ""
    st.session_state.filename = ""
    st.session_state.number_of_tags = ""
    st.session_state.target_tags = ""


def populate_journal_tags(file_input):
    if file_input:
        st.session_state.target_tags = tag_dict_organiser(file_input)


def parse_range(input_str):
    """Safely converts 'start, end' string to a tuple of ints."""
    try:
        parts = [int(x.strip()) for x in input_str.split(",")]
        return (parts[0], parts[1])

    except (ValueError, IndexError):
        st.sidebar.error("⚠️ Invalid reference range. Please use 'start, end' format (e.g., 1, 20)")
        return 