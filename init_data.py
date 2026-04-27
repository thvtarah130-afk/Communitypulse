import requests
import os

API_URL = "http://localhost:8000"
DATA_DIR = "C:/Users/thvta/.gemini/antigravity/scratch/community_insight/data"

def upload_issues():
    file_path = os.path.join(DATA_DIR, "sample_issues.csv")
    with open(file_path, "rb") as f:
        files = {"file": ("sample_issues.csv", f, "text/csv")}
        res = requests.post(f"{API_URL}/upload-data", files=files)
        print(f"Issues upload: {res.status_code} - {res.json()}")

def upload_volunteers():
    file_path = os.path.join(DATA_DIR, "sample_volunteers.csv")
    import pandas as pd
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        payload = row.to_dict()
        res = requests.post(f"{API_URL}/add-volunteer", json=payload)
        # print(f"Volunteer {payload['name']} upload: {res.status_code}")

if __name__ == "__main__":
    try:
        upload_issues()
        upload_volunteers()
        print("Data initialization complete.")
    except Exception as e:
        print(f"Error initializing data: {e}")
