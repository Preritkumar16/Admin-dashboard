import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from components import (time_series_decomposition, monthly_trend, weekly_pattern, 
                       top_products, revenue_breakdown, pie_chart_category,
                       scatter_plot_amount_customer, box_plot_amount, 
                       sunburst_chart, polar_chart_category)

# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'dashboard_data.csv')

st.set_page_config(page_title="Analytics - Admin Dashboard", layout="wide")

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_PATH)
    orders['timestamp'] = pd.to_datetime(orders['timestamp'])
    return orders

orders = load_data()

st.title("📈 Analytics Dashboard")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(orders['timestamp'].min().date(), orders['timestamp'].max().date())
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=orders['category'].unique(),
    default=orders['category'].unique()
)

status_filter = st.sidebar.multiselect(
    "Select Status",
    options=orders['status'].unique(),
    default=orders['status'].unique()
)

# Apply Filters
filtered_orders = orders[
    (orders['timestamp'].dt.date >= date_range[0]) &
    (orders['timestamp'].dt.date <= date_range[1]) &
    (orders['category'].isin(category_filter)) &
    (orders['status'].isin(status_filter))
]

st.markdown(f"### 📊 Showing {len(filtered_orders):,} orders")

# KPI Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_rev = filtered_orders['amount'].sum()
    st.metric("Total Revenue", f"₹{total_rev:,.0f}")
with col2:
    avg_order = filtered_orders['amount'].mean()
    st.metric("Avg Order Value", f"₹{avg_order:,.0f}")
with col3:
    total_orders = len(filtered_orders)
    st.metric("Total Orders", f"{total_orders:,}")
with col4:
    delivery_rate = (filtered_orders['status'] == 'delivered').mean() * 100
    st.metric("Delivery Rate", f"{delivery_rate:.1f}%")

st.markdown("---")

# Time Series Analysis
st.header("⏰ Time Series Analysis")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue Trend with Moving Averages")
    time_series_decomposition(filtered_orders)

with col2:
    st.subheader("Monthly Revenue Trend")
    monthly_trend(filtered_orders)

# Weekly Pattern
st.subheader("📅 Weekly Revenue Pattern")
weekly_pattern(filtered_orders)

st.markdown("---")

# Top Products & Revenue Breakdown
st.header("🏆 Top Products & Revenue")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Categories by Revenue")
    top_products(filtered_orders)

with col2:
    st.subheader("Category Distribution")
    pie_chart_category(filtered_orders)

st.markdown("---")

# Advanced Analytics
st.header("🔍 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Amount vs Customer Analysis")
    scatter_plot_amount_customer(filtered_orders)

with col2:
    st.subheader("Order Amount Distribution by Category")
    box_plot_amount(filtered_orders)

# Revenue Breakdown
st.subheader("💰 Revenue Breakdown")
revenue_breakdown(filtered_orders)

# Hierarchical Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Category to Status Sunburst")
    sunburst_chart(filtered_orders)

with col2:
    st.subheader("Category Comparison (Polar)")
    polar_chart_category(filtered_orders)

st.markdown("---")

# Statistics Table
st.header("📋 Summary Statistics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Category Statistics")
    cat_stats = filtered_orders.groupby('category').agg({
        'amount': ['sum', 'mean', 'count', 'std'],
        'order_id': 'count'
    }).round(2)
    cat_stats.columns = ['Total Revenue', 'Avg Amount', 'Order Count', 'Std Dev', 'Orders']
    st.dataframe(cat_stats, use_container_width=True)

with col2:
    st.subheader("Status Statistics")
    status_stats = filtered_orders.groupby('status').agg({
        'amount': ['sum', 'mean', 'count'],
        'order_id': 'count'
    }).round(2)
    status_stats.columns = ['Total Revenue', 'Avg Amount', 'Order Count', 'Orders']
    st.dataframe(status_stats, use_container_width=True)

# Download filtered data
st.markdown("---")
st.subheader("💾 Export Data")
csv = filtered_orders.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_orders.csv",
    mime="text/csv"
)
