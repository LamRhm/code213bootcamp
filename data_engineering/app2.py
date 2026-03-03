import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import os

# Authenticate and create the PyDrive client
@st.cache_resource
def init_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Opens your browser for authentication
    return GoogleDrive(gauth)

drive = init_drive()

# Streamlit app
st.set_page_config(page_title='TechTrapture Upload', layout='centered')
st.title('📁 TechTrapture Data Upload')
st.markdown("Upload your file to **Google Drive**.")

uploaded_file = st.file_uploader("Choose a file", type=['csv', 'txt', 'json', 'xlsx'])

if uploaded_file and st.button("Upload to Google Drive"):
    # Save uploaded file to a temporary location
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Upload to Google Drive
    file_drive = drive.CreateFile({'title': uploaded_file.name})
    file_drive.SetContentFile(uploaded_file.name)
    file_drive.Upload()

    st.success(f"✅ File `{uploaded_file.name}` uploaded to your Google Drive successfully.")

    # Optionally delete temp file
    os.remove(uploaded_file.name)
