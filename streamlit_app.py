import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


# Load JSON credentials from Streamlit secrets
creds_dict = st.secrets["gcp_service_account"]
creds_json = json.loads(json.dumps(creds_dict))  # convert to dict

# Set up credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)

client = gspread.authorize(credentials)

# Open your Google Sheet
sheet = client.open("KD3270 data sheet").sheet1

# Get all data
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Show it on Streamlit
st.title("KD 3270 KVK7 stats")
st.dataframe(df)

# Streamlit UI
st.title("🔍 Search by ID")

# Input field for ID
search_id = st.text_input("Enter ID")

# Check and display result
if search_id:
    # Convert to string for comparison
    match = df[df["ID"].astype(str) == search_id.strip()]
    
    if not match.empty:
        st.success("🎉 Match found!")
        st.dataframe(match)
    else:
        st.warning("⚠️ No match found.")