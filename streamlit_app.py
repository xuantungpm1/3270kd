import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scope
)

client = gspread.authorize(credentials)
sheet = client.open("Your Google Sheet Name").sheet1
df = pd.DataFrame(sheet.get_all_records())

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