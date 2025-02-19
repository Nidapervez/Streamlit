import pandas as pd
import os
from io import BytesIO
import streamlit as st

# Set up Streamlit page
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")

st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File Uploader
uploaded_files = st.file_uploader(
    "Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format!")
            continue

        # Display file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show data preview
        st.write("### Preview the Data")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values Filled!")

        # Choose Specific Columns
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]))

        # Conversion Options
        st.subheader("File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ("CSV", "Excel"), key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

st.success("✅ All files processed successfully!") if uploaded_files else None 