import pandas as pd
import os
from io import BytesIO
import streamlit as st

# Set up Streamlit page with a modern look
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.markdown("""
    <style>
        .stApp {
            background-color: #f7f7f7;
        }
        .main-title {
            text-align: center;
            font-size: 2.5rem;
            color: #333;
        }
        .upload-section {
            border: 2px dashed #4a90e2;
            padding: 20px;
            border-radius: 10px;
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>📂 Data Sweeper</h1>", unsafe_allow_html=True)
st.write("Transform your CSV and Excel files with built-in data cleaning and visualization!")

# File Uploader
st.markdown("### Upload your files (CSV or Excel):")
uploaded_files = st.file_uploader("Drag & Drop or Browse", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        try:
            df = pd.read_csv(file) if file_ext == ".csv" else pd.read_excel(file)
        except Exception as e:
            st.error(f"Error loading {file.name}: {e}")
            continue

        # Display File Info
        with st.expander(f"📄 **{file.name} - {file.size / 1024:.2f} KB**"):
            st.dataframe(df.head(), use_container_width=True)

            # Data Cleaning
            st.subheader("🧹 Data Cleaning")
            remove_duplicates = st.checkbox("Remove Duplicates", key=f"dup_{file.name}")
            fill_missing = st.checkbox("Fill Missing Values", key=f"fill_{file.name}")
            
            if st.button("Apply Cleaning", key=f"clean_{file.name}"):
                if remove_duplicates:
                    df.drop_duplicates(inplace=True)
                if fill_missing:
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("Data Cleaning Applied!")

            # Column Selection
            st.subheader("🎯 Select Columns to Keep")
            selected_columns = st.multiselect("Choose Columns", df.columns, default=df.columns, key=f"cols_{file.name}")
            df = df[selected_columns]

            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox("Show Numeric Data Chart", key=f"chart_{file.name}"):
                st.bar_chart(df.select_dtypes(include=["number"]))

            # File Conversion
            st.subheader("🔄 Convert File Format")
            conversion_type = st.radio("Convert to:", ("CSV", "Excel"), key=f"convert_{file.name}")
            if st.button("Convert & Download", key=f"download_{file.name}"):
                buffer = BytesIO()
                file_name = file.name.replace(file_ext, ".csv" if conversion_type == "CSV" else ".xlsx")
                mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False)
                
                buffer.seek(0)
                st.download_button(
                    label=f"📥 Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("✅ Processing Complete!") if uploaded_files else None
