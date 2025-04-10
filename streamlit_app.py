import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.graph_objects as go

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
        
        # Example DKP value
        dkp_rate = row['DKP rate']  # Replace with your actual value

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=dkp_rate,
            title={'text': "DKP rate"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00CC96"},
                'bgcolor': "darkgray",
                'borderwidth': 1,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': "#FF4B4B"},
                    {'range': [50, 80], 'color': "#FFA500"},
                    {'range': [80, 100], 'color': "#00CC96"}
                ],
            }
        ))

        fig.update_layout(
            width=200,  # or any size in pixels
            height=100,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="#2c3e50",  # optional dark background
            font=dict(color="white")
        )

        st.plotly_chart(fig)
    else:
        st.warning("❌ No matching ID found.")


