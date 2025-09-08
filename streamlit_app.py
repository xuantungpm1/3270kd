import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.graph_objects as go

date = "07/09/2025"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"],
    scope
)

client = gspread.authorize(credentials)
sheet = client.open("KD3270 data sheet").sheet1

# Streamlit UI
st.title(f"KD3270 KVK stats {date}")
df = pd.DataFrame(sheet.get_all_records())

st.dataframe(df)

#KPI target
st.set_page_config(page_title="DKP Tables", layout="centered")

# --- TABLE 1: DKP-Deads ratio ---
st.markdown("<h2 style='text-align: center; color: white; background-color: black;'>DKP-Deads ratio</h2>", unsafe_allow_html=True)

deads_data = {
    "POWER RANGE": [
        "20.000.000 - 30.000.000",
        "30.000.001 - 40.000.000",
        "40.000.001 - 50.000.000",
        "50.000.001 - 60.000.000",
        "60.000.001 - 70.000.000",
        "70.000.001 - 80.000.000",
        "80.000.001 - 85.000.000",
        "85.000.001 - 90.000.000",
        "90.000.001 - 100.000.000",
        "100.000.001 - MORE"
    ],
    "GOAL": [
        "250.000",
        "300.000",
        "400.000",
        "550.000",
        "650.000",
        "750.000",
        "900.000",
        "1.250.000",
        "1.500.000",
        "2.000.000"
    ]
}
deads_df = pd.DataFrame(deads_data)
st.table(deads_df)

# --- TABLE 2: DKP-Power-ratio ---
st.markdown("<h2 style='text-align: center; color: white; background-color: black;'>DKP-Power-ratio</h2>", unsafe_allow_html=True)

power_data = {
    "POWER RANGE": [
        "1 - 49.999.999",
        "50.000.000 - 79.999.999",
        "80.000.000 - UPWARD"
    ],
    "% GOAL": [
        "15,0%",
        "20,0%",
        "35,0%"
    ],
    "CATEGORY": [
        "<span style='color:green'><b>ELITE</b></span>",
        "<span style='color:blue'><b>EPIC</b></span>",
        "<span style='color:orange'><b>LEGENDARY</b></span>"
    ]
}
power_df = pd.DataFrame(power_data)

# Render HTML table with colors
st.markdown("""
<table style='width:100%; border-collapse: collapse; text-align: center;'>
    <thead style='background-color: black; color: white;'>
        <tr>
            <th>POWER RANGE</th>
            <th>% GOAL</th>
            <th>CATEGORY</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1 - 49.999.999</td><td>15,0%</td><td><span style='color:green'><b>ELITE</b></span></td></tr>
        <tr><td>50.000.000 - 79.999.999</td><td>20,0%</td><td><span style='color:blue'><b>EPIC</b></span></td></tr>
        <tr><td>80.000.000 - UPWARD</td><td>35,0%</td><td><span style='color:orange'><b>LEGENDARY</b></span></td></tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

html_content = """
<div><b><font style="font-size: 36px;">So how to achieve DKP?&nbsp;</font></b><br></div>
<div><font style="font-size: 20px;" color="#81c784">- T4 kills: 1 point per troop<br></font></div>
<div><font style="font-size: 20px;" color="#81c784">- T5 kills: 2 points per troop</font></div>
<div><font style="font-size: 20px;" color="#81c784">- Dead troops: 3 points per T4/5 troop.&nbsp;</font></div>
<div><font style="font-size: 20px;"><br></font></div>
<div><font style="font-size: 20px;">No points for T3 troop or lower</font></div>
<div><font style="font-size: 20px;">Dead troops target (T4/5 only):</font></div>
<div><font style="font-size: 20px;"><i>You are required to get both kills and dead troops in order to meet your DKP. From the below calculation, you will know how many kills or dead troops will enable you to achieve your target:</i></font></div>
"""

st.markdown(html_content, unsafe_allow_html=True)

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
        right_cols = ["Target DKP", "Target Deads", "KP gained", "Deads gained", "T4 Kills gained", "T5 Kills gained", "Score", "Rank"]

        st.markdown(f"### 🧾 Result({date})")
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
            width=300,  # or any size in pixels
            height=200,
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
            width=300,  # or any size in pixels
            height=200,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor="#2c3e50",  # optional dark background
            font=dict(color="white")
        )

        # st.plotly_chart(fig1, use_container_width=False, key="deads_chart")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### DKP rate")
            st.plotly_chart(fig, use_container_width=True, key="dkp_chart")

        with col2:
            st.markdown("### Deads rate")
            st.plotly_chart(fig1, use_container_width=True, key="deads_chart")
    else:
        st.warning("❌ No matching ID found.")


