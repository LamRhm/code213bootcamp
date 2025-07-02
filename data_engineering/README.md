
# 🛠️ Employee Data Pipeline with GCP, Streamlit, and Looker Studio

This project demonstrates a complete **data engineering pipeline** using Google Cloud Platform (GCP) services. It allows users to upload data via a **Streamlit UI**, stores the data in **Google Cloud Storage**, processes and cleans it via a **Cloud Run** service which loads it into **BigQuery**, and visualizes insights in **Looker Studio**.

---

## 📌 Project Overview

- Upload raw employee data using a simple Streamlit interface.
- Authenticate and save data to Google Cloud Storage.
- Trigger a Cloud Run function to:
  - Load data from Cloud Storage to BigQuery.
  - Clean and transform data.
  - Create two analytics tables.
- Connect BigQuery to Looker Studio to build a dashboard displaying performance and insights from employee data.

---

## 🚀 Technologies Used

- [Streamlit](https://streamlit.io/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Google Cloud Run](https://cloud.google.com/run)
- [Google BigQuery](https://cloud.google.com/bigquery)
- [Looker Studio](https://lookerstudio.google.com/)
- Python, Pandas, SQL

---

## 🔧 Prerequisites

- A Google Cloud Platform (GCP) account.
- Enable the following GCP APIs:
  - Cloud Storage
  - BigQuery
  - Cloud Run
- Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- Set the following environment variables:

```bash
export GCP_PROJECT='your-gcp-project-id'
export GCS_BUCKET='your-bucket-name'
export BQ_DATASET='your-bigquery-dataset'
```

---

## 📝 How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/employee-data-pipeline.git
cd employee-data-pipeline
```

### 2. Launch the Streamlit App

```bash
streamlit run app.py
```

The Streamlit app will prompt you to upload a file and authenticate using PyDrive.

### 3. Create GCP Resources

- Create a Cloud Storage bucket:
```bash
gsutil mb -p $GCP_PROJECT gs://$GCS_BUCKET/
```

- Create a BigQuery dataset:
```bash
bq mk --dataset $GCP_PROJECT:$BQ_DATASET
```

### 4. Deploy Cloud Run

Your Cloud Run function (e.g., `load_to_bq.py`) should:
- Authenticate with GCP using a service account.
- Load the uploaded file from Cloud Storage.
- Clean and transform the data.
- Create `table_1` and `table_2` in BigQuery.

Deploy with:

```bash
gcloud run deploy load-to-bq   --source .   --entry-point main   --runtime python310   --set-env-vars GCS_BUCKET=$GCS_BUCKET,BQ_DATASET=$BQ_DATASET   --project $GCP_PROJECT   --region us-central1   --allow-unauthenticated
```

### 5. Connect to Looker Studio

- Go to [Looker Studio](https://lookerstudio.google.com/)
- Connect your BigQuery tables `table_1` and `table_2`.
- Build visual dashboards for insights and employee performance.

---

## 🧱 Pipeline Architecture

```plaintext
[Streamlit App] → [Cloud Storage] → [Cloud Run] → [BigQuery] → [Looker Studio]
```

Each stage is modular and can be extended to include data versioning, monitoring, or real-time processing.

---

## ✅ Features

- Intuitive interface for data upload
- GCP-integrated secure file storage
- Scalable data transformation with Cloud Run
- Structured reporting and dashboards with Looker Studio
- End-to-end pipeline automation

---

## 📁 Sample Code: Upload with Streamlit

```python
import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

@st.cache_resource
def init_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

drive = init_drive()

st.title('📁 TechTrapture Data Upload')
uploaded_file = st.file_uploader("Upload a file", type=['csv', 'txt', 'json', 'xlsx'])

if uploaded_file and st.button("Upload"):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_drive = drive.CreateFile({'title': uploaded_file.name})
    file_drive.SetContentFile(uploaded_file.name)
    file_drive.Upload()
    st.success(f"✅ File `{uploaded_file.name}` uploaded successfully.")
    os.remove(uploaded_file.name)
```

---

## 📊 Sample Dashboard Output

Check the [Looker Studio Dashboard](#) to explore insights like:
- Employee Attrition
- Salary Distribution
- Departmental Performance

---

## 🙌 Credits

Made with ❤️ by [Your Name]

---

## 📄 License

MIT License
