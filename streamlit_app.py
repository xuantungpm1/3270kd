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
        left_cols = ["ID", "Name", "Alliance", "Power"]
        right_cols = ["Target DKP", "Target Deads", "Score", "Rank"]

        st.markdown("### 🧾 Result")
        # cols = st.columns(2)
        # for col in columns_to_display:
        #     st.markdown(f"**{col}**: {row[col]}")

        col1, col2 = st.columns(2)
        with col1:
            for col in left_cols:
                st.markdown(f"**{col}**: {row[col]}")
        
        with col2:
            for col in right_cols:
                st.markdown(f"**{col}**: {row[col]}")
        
        # Example DKP value
        dkp_rate = row['DKP rate']  # Replace with your actual value

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=dkp_rate,
            title={'text': "DKP rate"},
            gauge={
                'axis': {'range': [0, 200]},
                'bar': {'color': "#00CC96"},
                'bgcolor': "darkgray",
                'borderwidth': 1,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 80], 'color': "#FF4B4B"},
                    {'range': [80, 100], 'color': "#FFA500"},
                    {'range': [100, 200], 'color': "#00CC96"}
                ],
            }
        ))

        fig.update_layout(
            width=400,  # or any size in pixels
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="#2c3e50",  # optional dark background
            font=dict(color="white")
        )
        # st.plotly_chart(fig, use_container_width=False, key="dkp_chart")

        # Example DKP value
        deads_rate = row['Deads rate']  # Replace with your actual value

        fig1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=deads_rate,
            title={'text': "Deads rate"},
            gauge={
                'axis': {'range': [0, 200]},
                'bar': {'color': "#00CC96"},
                'bgcolor': "darkgray",
                'borderwidth': 1,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 80], 'color': "#FF4B4B"},
                    {'range': [80, 100], 'color': "#FFA500"},
                    {'range': [100, 200], 'color': "#00CC96"}
                ],
            }
        ))

        fig1.update_layout(
            width=400,  # or any size in pixels
            height=300,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="#2c3e50",  # optional dark background
            font=dict(color="white")
        )

        # st.plotly_chart(fig1, use_container_width=False, key="deads_chart")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("### DKP rate")
            st.plotly_chart(fig, use_container_width=True, key="dkp_chart")

        with col4:
            st.markdown("### Deads rate")
            st.plotly_chart(fig1, use_container_width=True, key="deads_chart")
    else:
        st.warning("❌ No matching ID found.")


