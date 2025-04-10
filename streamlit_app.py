import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

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