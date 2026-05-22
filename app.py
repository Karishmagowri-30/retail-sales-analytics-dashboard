import streamlit as st
import pandas as pd
import plotly.express as px

# Dashboard title
st.title("Sales Dashboard")

# Load dataset
df = pd.read_csv(r"D:\Sales_Dashboard_Project\sales_dataset.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Convert order_date safely
df["order_date"] = pd.to_datetime(df["order_date"], format="mixed", errors="coerce")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Date filter
start_date = st.sidebar.date_input(
    "Select Start Date", 
    df["order_date"].min()
)
end_date = st.sidebar.date_input(
    "Select End Date", 
    df["order_date"].max()
)

# Region filter

region_filter = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)


# Filter the DataFrame

df = df[(df["region"].isin(region_filter)) & (df["category"].isin(category_filter))]

# Handle empty dataset
if df.empty:
    st.warning("No data available for the selected filters")

# -----------------------------
# KPI Metrics
# -----------------------------
total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
total_orders = df["order_id"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", total_orders)

# -----------------------------
# Sales by Category
# -----------------------------
category_sales = df.groupby("category")["sales"].sum().reset_index()

fig1 = px.bar(
    category_sales,
    x="category",
    y="sales",
    title="Sales by Category"
)
st.subheader("Sales by Category")
st.plotly_chart(fig1)

# -----------------------------
# Sales by Region
# -----------------------------
region_sales = df.groupby("region")["sales"].sum().reset_index()

fig2 = px.pie(
    region_sales,
    values="sales",
    names="region",
    title="Sales by Region"
)
st.subheader("Sales by Region")
st.plotly_chart(fig2)

# -----------------------------
# Sales Trend
# -----------------------------
sales_trend = df.groupby("order_date")["sales"].sum().reset_index()
sales_trend = sales_trend.sort_values("order_date")

fig3 = px.line(
    sales_trend,
    x="order_date",
    y="sales",
    title="Sales Trend Over Time"
)
st.subheader("Sales Trend Over Time")
st.plotly_chart(fig3)

# -----------------------------
# Top 10 Products by Sales
# -----------------------------
top_products = df.groupby("product")["sales"].sum().reset_index()
top_products = top_products.sort_values(by="sales", ascending=False).head(10)

fig4 = px.bar(
    top_products,
    x="product",
    y="sales",
    title="Top 10 Products by Sales"
)
st.subheader("Top 10 Products by Sales")
st.plotly_chart(fig4)

# -----------------------------
# Profit by Category
# -----------------------------
profit_category = df.groupby("category")["profit"].sum().reset_index()

fig5 = px.bar(
    profit_category,
    x="category",
    y="profit",
    title="Profit by Category"
)
st.subheader("Profit by Category")
st.plotly_chart(fig5)

# -----------------------------
# Show dataset
# -----------------------------
if st.button("Save Filtered Data"):
    df.to_csv("filtered_sales.csv", index=False)
    st.success("Filtered data saved!")