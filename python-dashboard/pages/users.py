import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'dashboard_data.csv')

st.set_page_config(page_title="Users - Admin Dashboard", layout="wide")

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_PATH)
    orders['timestamp'] = pd.to_datetime(orders['timestamp'])
    return orders

orders = load_data()

st.title("👥 Users Dashboard")
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

st.markdown(f"### 📊 Analyzing {len(filtered_orders):,} orders from {filtered_orders['customer_id'].nunique():,} unique customers")

# User KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    unique_customers = filtered_orders['customer_id'].nunique()
    st.metric("Unique Customers", f"{unique_customers:,}")
with col2:
    avg_orders_per_customer = len(filtered_orders) / unique_customers if unique_customers > 0 else 0
    st.metric("Avg Orders/Customer", f"{avg_orders_per_customer:.1f}")
with col3:
    avg_revenue_per_customer = filtered_orders['amount'].sum() / unique_customers if unique_customers > 0 else 0
    st.metric("Avg Revenue/Customer", f"₹{avg_revenue_per_customer:,.0f}")
with col4:
    repeat_rate = (filtered_orders.groupby('customer_id').size() > 1).mean() * 100
    st.metric("Repeat Customer Rate", f"{repeat_rate:.1f}%")

st.markdown("---")

# Customer Segmentation
st.header("🎯 Customer Segmentation")

# Customer metrics
customer_metrics = filtered_orders.groupby('customer_id').agg({
    'order_id': 'count',
    'amount': ['sum', 'mean'],
    'category': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A',
    'status': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'N/A'
}).reset_index()

customer_metrics.columns = ['customer_id', 'total_orders', 'total_revenue', 'avg_order_value', 'preferred_category', 'preferred_status']

# Segment customers
def segment_customer(orders_count, total_revenue):
    if orders_count >= 5 and total_revenue >= 5000:
        return 'VIP'
    elif orders_count >= 3 and total_revenue >= 2000:
        return 'Premium'
    elif orders_count >= 1 and total_revenue >= 500:
        return 'Regular'
    else:
        return 'New'

customer_metrics['segment'] = customer_metrics.apply(
    lambda x: segment_customer(x['total_orders'], x['total_revenue']), axis=1
)

# Customer Segment Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Segments")
    segment_counts = customer_metrics['segment'].value_counts().reset_index()
    segment_counts.columns = ['segment', 'count']
    
    fig = px.pie(segment_counts, values='count', names='segment',
                 title='Customer Segment Distribution',
                 color='segment',
                 color_discrete_map={
                     'VIP': '#FFD700',
                     'Premium': '#C0C0C0',
                     'Regular': '#CD7F32',
                     'New': '#10B981'
                 },
                 hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Segment")
    segment_revenue = customer_metrics.groupby('segment')['total_revenue'].sum().reset_index()
    
    fig = px.bar(segment_revenue, x='segment', y='total_revenue',
                 title='Total Revenue by Customer Segment',
                 color='segment',
                 color_discrete_map={
                     'VIP': '#FFD700',
                     'Premium': '#C0C0C0',
                     'Regular': '#CD7F32',
                     'New': '#10B981'
                 })
    fig.update_traces(texttemplate='₹%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Top Customers Analysis
st.header("🏆 Top Customers")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Customers by Revenue")
    top_customers = customer_metrics.nlargest(10, 'total_revenue')
    
    fig = px.bar(top_customers, x='total_revenue', y='customer_id', orientation='h',
                 title='Top 10 Customers by Revenue',
                 color='total_revenue',
                 color_continuous_scale='Greens')
    fig.update_traces(texttemplate='₹%{x:,.0f}', textposition='inside')
    fig.update_layout(yaxis_title='Customer ID', xaxis_title='Total Revenue (₹)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Customers by Orders")
    top_by_orders = customer_metrics.nlargest(10, 'total_orders')
    
    fig = px.bar(top_by_orders, x='total_orders', y='customer_id', orientation='h',
                 title='Top 10 Customers by Orders',
                 color='total_orders',
                 color_continuous_scale='Blues')
    fig.update_traces(texttemplate='%{x}', textposition='inside')
    fig.update_layout(yaxis_title='Customer ID', xaxis_title='Total Orders')
    st.plotly_chart(fig, use_container_width=True)

# Customer Activity Analysis
st.markdown("---")
st.header("📊 Customer Activity Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Orders per Customer Distribution")
    order_counts = customer_metrics['total_orders'].value_counts().sort_index().reset_index()
    order_counts.columns = ['orders', 'customers']
    
    fig = px.bar(order_counts, x='orders', y='customers',
                 title='Distribution of Orders per Customer',
                 color='customers',
                 color_continuous_scale='Viridis')
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Customer Value Distribution")
    fig = px.histogram(customer_metrics, x='total_revenue', nbins=20,
                       title='Distribution of Customer Total Revenue',
                       color_discrete_sequence=['#6366F1'])
    fig.update_layout(xaxis_title='Total Revenue (₹)', yaxis_title='Number of Customers')
    st.plotly_chart(fig, use_container_width=True)

# Customer Preferences
st.markdown("---")
st.header("🎨 Customer Preferences")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Preferred Categories by Segment")
    pref_category = customer_metrics.groupby(['segment', 'preferred_category']).size().reset_index(name='count')
    
    fig = px.bar(pref_category, x='segment', y='count', color='preferred_category',
                 title='Preferred Category by Customer Segment',
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Preferred Status by Segment")
    pref_status = customer_metrics.groupby(['segment', 'preferred_status']).size().reset_index(name='count')
    
    fig = px.bar(pref_status, x='segment', y='count', color='preferred_status',
                 title='Preferred Order Status by Customer Segment',
                 barmode='group')
    st.plotly_chart(fig, use_container_width=True)

# Customer Table
st.markdown("---")
st.header("👥 Customer Details")

# Filter customers by segment
segment_filter = st.multiselect(
    "Filter by Segment",
    options=customer_metrics['segment'].unique(),
    default=customer_metrics['segment'].unique()
)

filtered_customers = customer_metrics[customer_metrics['segment'].isin(segment_filter)]

st.dataframe(
    filtered_customers[['customer_id', 'total_orders', 'total_revenue', 'avg_order_value', 'preferred_category', 'preferred_status', 'segment']],
    use_container_width=True,
    height=400
)

# Customer Retention Analysis
st.markdown("---")
st.header("🔄 Customer Retention")

# Calculate order dates per customer
customer_orders = filtered_orders.groupby('customer_id')['timestamp'].agg(['min', 'max', 'count']).reset_index()
customer_orders.columns = ['customer_id', 'first_order', 'last_order', 'order_count']

# Days since last order
customer_orders['days_since_last_order'] = (filtered_orders['timestamp'].max() - customer_orders['last_order']).dt.days

# Churn analysis
customer_orders['churn_risk'] = customer_orders['days_since_last_order'].apply(
    lambda x: 'High Risk' if x > 30 else ('Medium Risk' if x > 14 else 'Active')
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Churn Risk")
    churn = customer_orders['churn_risk'].value_counts().reset_index()
    churn.columns = ['risk', 'count']
    
    fig = px.pie(churn, values='count', names='risk',
                 title='Customer Churn Risk Distribution',
                 color='risk',
                 color_discrete_map={
                     'Active': '#10B981',
                     'Medium Risk': '#F59E0B',
                     'High Risk': '#EF4444'
                 },
                 hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Days Since Last Order")
    fig = px.histogram(customer_orders, x='days_since_last_order', nbins=20,
                      title='Distribution of Days Since Last Order',
                      color_discrete_sequence=['#3B82F6'])
    fig.update_layout(xaxis_title='Days', yaxis_title='Number of Customers')
    st.plotly_chart(fig, use_container_width=True)

# Export Customer Data
st.markdown("---")
st.subheader("💾 Export Customer Data")
csv = customer_metrics.to_csv(index=False)
st.download_button(
    label="Download Customer Data as CSV",
    data=csv,
    file_name="customer_data.csv",
    mime="text/csv"
)
