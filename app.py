import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Executive Dashboard")

# ---------------------------
# CUSTOM DARK STYLE
# ---------------------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .metric-card {
        background-color: #1c1f26;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Executive Sales Dashboard")

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file is not None:

    # Load data
    df = pd.read_excel(uploaded_file, header=None)

    # Clean data
    df = df.iloc[11:]
    df.columns = ["Ignore", "Quarter", "Ignore2", "Ignore3", "Ignore4", "Ignore5",
                  "Ignore6", "Ignore7", "Ignore8", "Ignore9", "Estimate", "Actual"]

    df = df[["Quarter", "Estimate", "Actual"]].dropna()

    df["Estimate"] = pd.to_numeric(df["Estimate"], errors="coerce")
    df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce")

    # ---------------------------
    # SIDEBAR FILTER
    # ---------------------------
    st.sidebar.header("🔍 Filters")

    selected_quarter = st.sidebar.multiselect(
        "Select Quarter",
        df["Quarter"].unique(),
        default=df["Quarter"].unique()
    )

    df = df[df["Quarter"].isin(selected_quarter)]

    # ---------------------------
    # SMART KPIs
    # ---------------------------
    total_est = df["Estimate"].sum()
    total_act = df["Actual"].sum()
    variance = total_act - total_est
    performance = (total_act / total_est * 100) if total_est != 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Estimate", f"{total_est:,.0f}")
    col2.metric("💵 Actual", f"{total_act:,.0f}")
    col3.metric("📉 Variance", f"{variance:,.0f}")
    col4.metric("📊 Performance %", f"{performance:.1f}%")

    # ---------------------------
    # ROW 1
    # ---------------------------
    col5, col6 = st.columns(2)

    # Donut Chart
    with col5:
        donut = px.pie(df,
                       names="Quarter",
                       values="Actual",
                       hole=0.6,
                       title="Opportunity Breakdown")
        donut.update_layout(template="plotly_dark")
        st.plotly_chart(donut, use_container_width=True)

    # Bar Chart
    with col6:
        bar = px.bar(df,
                     x="Quarter",
                     y=["Estimate", "Actual"],
                     barmode="group",
                     title="Bookings QTD")
        bar.update_layout(template="plotly_dark")
        st.plotly_chart(bar, use_container_width=True)

    # ---------------------------
    # ROW 2
    # ---------------------------
    col7, col8 = st.columns(2)

    # Line Chart
    with col7:
        line = px.line(df,
                       x="Quarter",
                       y=["Estimate", "Actual"],
                       markers=True,
                       title="Trend Analysis")
        line.update_layout(template="plotly_dark")
        st.plotly_chart(line, use_container_width=True)

    # Map (Replace with real data later)
    with col8:
        map_data = pd.DataFrame({
            "Country": ["India", "USA", "Germany", "Brazil"],
            "Sales": [400, 500, 300, 200]
        })

        map_fig = px.choropleth(map_data,
                               locations="Country",
                               locationmode="country names",
                               color="Sales",
                               title="Regional Sales",
                               color_continuous_scale="Blues")

        map_fig.update_layout(template="plotly_dark")
        st.plotly_chart(map_fig, use_container_width=True)

else:
    st.warning("⬆️ Upload your Excel file to start")
    st.stop()