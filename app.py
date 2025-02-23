import streamlit as st
import pandas as pd
import os
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="Data Sweeper 🧹",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to encode the background image
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded_img = base64.b64encode(f.read()).decode()
    bg_css = f"""
    <style>
        .stApp {{
            background: url('data:image/jpg;base64,{encoded_img}') no-repeat center center fixed;
            background-size: cover;
        }}
        
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        h1{{
            text-align: left;
            color: #222;
            font-weight: bold;
            font-size: 16px;
            font-family: Arial, Helvetica, sans-serif;
            padding-left: 10px;
            padding-top: 10px;
        }}
        h2,h3{{
            text-align: left;
            color:white;
            font-size: 14px;
            font-weight: semibold;
            font-family: Arial, Helvetica, sans-serif;
        }}
        .stButton>button {{
            background: hsl(218, 67%, 26%);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            transition: 0.3s;
            hover:#315797;
    
        }}
        .stButton>button:hover {{
            background:hsl(218, 67%, 26%);
        }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Apply the background image
set_background("growth.jpg")

# Content layout
st.markdown('<div class="content-container">', unsafe_allow_html=True)

st.title("Data Sweeper🧹")
st.subheader("Clean • Convert • Visualize")

uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("❌ Unsupported file format")
            continue

        st.write(f"**📄 File:** {file.name}")
        st.write(f"**📊 Size:** {file.size/1024:.2f} KB")

        st.subheader("Preview")
        st.dataframe(df.head())

        st.subheader("Data Cleaning Options ♻️")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🔄 Remove Duplicates"):
                    df = df.drop_duplicates()
                    st.success("✅ Duplicates removed!")
            with col2:
                if st.button(f"📊 Fill Missing Values"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled!")

            st.subheader("Data Visualization 📊")
            if st.checkbox(f"Show Visualization for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    col_to_plot = st.selectbox("Select column to visualize", numeric_cols)
                    st.bar_chart(df[col_to_plot])
                else:
                    st.warning("No numeric columns available for visualization")

            st.subheader("Select Columns to Convert")
            columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            st.subheader("Conversion Options 🔄")
            conversion_type = st.radio(f"Select Conversion {file.name} to:", ["CSV", "Excel"], key=file.name)

            if st.button("Convert"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                else:
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"Download {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                st.success("✅ File converted!")
else:
    st.subheader("👋 Welcome to Data Sweeper!")
    st.write("Upload a CSV or Excel file to get started.")

st.markdown('</div>', unsafe_allow_html=True)
