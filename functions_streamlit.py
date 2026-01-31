import streamlit as st
import io
import pandas as pd

def download_excel_button(excel_data):
    st.download_button(
    label="Download Formatted Excel",
    data=excel_data,
    file_name="List_of_Top_References.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)