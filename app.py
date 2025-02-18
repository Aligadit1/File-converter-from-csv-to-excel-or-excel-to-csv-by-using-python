# imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# set up our app
st.set_page_config(page_title="Data Sweeper",layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel format with built-incdata cleaning an visualization")
uploaded_files =st.file_uploader("Upload your CSV or Excel files:", type=["csv","xlsx"],accept_multiple_files=True)

# function to convert CSV to Excel
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name) [-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format:{file_ext} , Please upload a CSV or Excel file.")
            continue

        # Info About the file 
        st.write(f"File name: {file.name}")
        st.write(f"File size: {file.size/1024}")

        # shows 5 rows of our df
        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())
        
        # Options for data cleaning
        st.subheader("Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1 , col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicate from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled with mean!")

        # choose specific column to keep or conver
        st.subheader("Select columns to Convert")
        columns = st.multiselect(f"choose columns for {file.name}",df.columns , default=df.columns)
        df = df[columns]

        # data visualization
        st.subheader("data viusalization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:,:2])

        # convert the file CSV to Excel
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:",['CSV','XLSX'],key=file.name)
        if st.button(f"convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type = "text/csv"
            elif conversion_type == "XLSX":
                df.to_excel(buffer,index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0) 
            
            # Downlaod button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )   

            st.success("All file formated successfully")