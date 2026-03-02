import streamlit as st
import pandas as pd
import plotly.express as px
import os
from components import (bar_chart_status, donut_chart_status, funnel_chart_conversion,
                       treemap_category, area_chart_revenue, histogram_order_amounts)

# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'dashboard_data.csv')

st.set_page_config(page_title="Orders - Admin Dashboard", layout="wide")

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_PATH)
    orders['timestamp'] = pd.to_datetime(orders['timestamp'])
    return orders

orders = load_data()

st.title("📋 Orders Dashboard")
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

# Order KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_orders = len(filtered_orders)
    st.metric("Total Orders", f"{total_orders:,}")
with col2:
    pending = len(filtered_orders[filtered_orders['status'] == 'pending'])
    st.metric("Pending Orders", f"{pending:,}")
with col3:
    delivered = len(filtered_orders[filtered_orders['status'] == 'delivered'])
    st.metric("Delivered Orders", f"{delivered:,}")
with col4:
    cancelled = len(filtered_orders[filtered_orders['status'] == 'cancelled'])
    st.metric("Cancelled Orders", f"{cancelled:,}")

st.markdown("---")

# Order Status Visualizations
st.header("📈 Order Status Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Order Status Distribution (Bar)")
    bar_chart_status(filtered_orders)

with col2:
    st.subheader("Order Status Breakdown (Donut)")
    donut_chart_status(filtered_orders)

# Order Conversion Funnel
st.subheader("🔄 Order Conversion Funnel")
funnel_chart_conversion(filtered_orders)

st.markdown("---")

# Order Timeline & Amount Analysis
st.header("⏰ Order Timeline Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cumulative Orders Over Time")
    area_chart_revenue(filtered_orders)

with col2:
    st.subheader("Order Amount Distribution")
    histogram_order_amounts(filtered_orders)

# Category & Status Treemap
st.subheader("📊 Category & Status Treemap")
treemap_category(filtered_orders)

st.markdown("---")

# Detailed Order Table with Filters
st.header("🔍 Detailed Order View")

# Additional filters for table
col1, col2, col3 = st.columns(3)
with col1:
    min_amount = st.number_input("Min Amount", min_value=0, value=0)
with col2:
    max_amount = st.number_input("Max Amount", min_value=0, value=int(filtered_orders['amount'].max()))
with col3:
    sort_by = st.selectbox("Sort By", ['timestamp', 'amount', 'order_id', 'customer_id'])

# Apply additional filters
table_orders = filtered_orders[
    (filtered_orders['amount'] >= min_amount) &
    (filtered_orders['amount'] <= max_amount)
]

# Sort
if sort_by == 'timestamp':
    table_orders = table_orders.sort_values('timestamp', ascending=False)
elif sort_by == 'amount':
    table_orders = table_orders.sort_values('amount', ascending=False)
else:
    table_orders = table_orders.sort_values(sort_by, ascending=False)

st.dataframe(
    table_orders[['order_id', 'timestamp', 'customer_id', 'amount', 'category', 'status']],
    use_container_width=True,
    height=400
)

# Order Statistics by Category
st.markdown("---")
st.header("📊 Order Statistics by Category")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Orders by Category")
    cat_orders = filtered_orders.groupby('category').size().reset_index(name='count')
    fig = px.bar(cat_orders, x='category', y='count', 
                 title='Number of Orders by Category',
                 color='count',
                 color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Average Order Value by Category")
    cat_avg = filtered_orders.groupby('category')['amount'].mean().reset_index()
    fig = px.bar(cat_avg, x='category', y='amount',
                 title='Average Order Value by Category',
                 color='amount',
                 color_continuous_scale='Greens')
    st.plotly_chart(fig, use_container_width=True)

# Recent Orders
st.markdown("---") 
st.header("🕐 Recent Orders")

recent = filtered_orders.tail(20)[['order_id', 'timestamp', 'customer_id', 'amount', 'category', 'status']]
st.dataframe(recent, use_container_width=True)

# Download filtered orders
st.markdown("---")
st.subheader("💾 Export Orders Data")
csv = filtered_orders.to_csv(index=False)
st.download_button(
    label="Download Orders as CSV",
    data=csv,
    file_name="orders_data.csv",
    mime="text/csv"
)
