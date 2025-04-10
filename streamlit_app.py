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
sheet = client.open("KD3270 data sheet").sheet1

# Streamlit UI
st.title("KD3270 KVK7 stats")
df = pd.DataFrame(sheet.get_all_records())

st.dataframe(df)

# Streamlit UI
st.title("🔍 Search by ID")

# Input field for ID
input_id = st.text_input("Enter ID")

# --- Filter and Show Specific Columns ---
if input_id:
    result = df[df["ID"].astype(str) == input_id]
    if not result.empty:
        row = result.iloc[0]

        # 🎯 Only show these columns
        columns_to_display = ["ID", "Name", "Alliance", "Power", "Target DKP", "Target Deads", "Score", "Rank"]

        st.markdown("### 🧾 Result")
        cols = st.columns(2)
        for col in columns_to_display:
            st.markdown(f"**{col}**: {row[col]}")
    else:
        st.warning("❌ No matching ID found.")