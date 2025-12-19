import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Bank Customer Churn Dashboard",
    layout="wide"
)

# Title
st.title("🏦 Bank Customer Churn Dashboard")

# Load data
df = pd.read_csv("data/Bank Customer Churn Prediction.csv")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

country = st.sidebar.multiselect(
    "Pilih Negara",
    df["country"].unique(),
    default=df["country"].unique()
)

age_range = st.sidebar.slider(
    "Range Umur",
    int(df["age"].min()),
    int(df["age"].max()),
    (25, 60)
)

churn_status = st.sidebar.selectbox(
    "Status Churn",
    ["All", "Churn", "Not Churn"]
)

active_only = st.sidebar.checkbox("Hanya Active Member")

# Data filtering
filtered_df = df[
    (df["country"].isin(country)) &
    (df["age"].between(age_range[0], age_range[1]))
]

if churn_status == "Churn":
    filtered_df = filtered_df[filtered_df["churn"] == 1]
elif churn_status == "Not Churn":
    filtered_df = filtered_df[filtered_df["churn"] == 0]

if active_only:
    filtered_df = filtered_df[filtered_df["active_member"] == 1]

# Metrics
total_customer = len(filtered_df)
churn_rate = round(filtered_df["churn"].mean() * 100, 2) if total_customer > 0 else 0
avg_balance = round(filtered_df["balance"].mean(), 2) if total_customer > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Customer", total_customer)
col2.metric("Churn Rate (%)", churn_rate)
col3.metric("Avg Balance", avg_balance)

# Visualization 1: Churn by Country
fig1 = px.bar(
    filtered_df.groupby("country")["churn"].mean().reset_index(),
    x="country",
    y="churn",
    title="Churn Rate by Country",
    labels={"churn": "Churn Rate"}
)

# Visualization 2: Age Distribution
fig2 = px.histogram(
    filtered_df,
    x="age",
    color="churn",
    nbins=20,
    title="Age Distribution by Churn Status"
)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Raw data
if st.checkbox("📄 Tampilkan Data Mentah"):
    st.dataframe(filtered_df)

# Button
if st.button("🔄 Refresh Dashboard"):
    st.experimental_rerun()
