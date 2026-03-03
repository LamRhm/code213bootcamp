import streamlit as st
from google.cloud import storage
from datetime import datetime
import os

#google cloud storage setup
bucket_name='techtrapture-data-bucket'

#create a function to upload files to gcs
def upload_to_gcs(file,filename):
    client=storage.client()
    bucket=client.bucket(bucket_name)
    blob=bucket.blob(f"uploads/{filename}")
    blob.upload_from_file(file)
    return f"file {filename} uploaded to bucket {bucket_name}"

#streamlit app
st.set_page_config(page_title='TechTrapture Upload', layout='centered')
st.title('📁 TechTrapture Data Upload')
st.markdown("Upload your file to google cloud strorage.")
uploaded_file=st.file_uploader("Choose a file", type=['csv','txt','json','xlsx'])
if uploaded_file is None:
    if st.button("Upload to GCS"):
        with uploaded_file:
            result=upload_to_gcs(uploaded_file,uploaded_file.name)
            st.success(result)
            


