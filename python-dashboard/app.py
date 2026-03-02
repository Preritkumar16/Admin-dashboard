import streamlit as st
import pandas as pd
from components import (kpi_card, seaborn_revenue_trend, seaborn_category_sales, 
                      plotly_status_heatmap, correlation_heatmap,
                      pie_chart_category, scatter_plot_amount_customer, bar_chart_status,
                      area_chart_revenue, histogram_order_amounts, donut_chart_status,
                      treemap_category, box_plot_amount, funnel_chart_conversion,
                      sunburst_chart, polar_chart_category, time_series_decomposition,
                      monthly_trend, weekly_pattern, top_products)
import os

# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'dashboard_data.csv')

# Generate data if not exists
if not os.path.exists(DATA_PATH):
    from data_generator import generate_admin_data
    generate_admin_data()

st.set_page_config(page_title="Admin Dashboard", layout="wide")

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_PATH)
    orders['timestamp'] = pd.to_datetime(orders['timestamp'])
    return orders

orders = load_data()

# Sidebar Filters
st.sidebar.title("Filters")

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

# Apply filters
filtered_orders = orders[
    (orders['timestamp'].dt.date >= date_range[0]) &
    (orders['timestamp'].dt.date <= date_range[1]) &
    (orders['category'].isin(category_filter)) &
    (orders['status'].isin(status_filter))
]

# Export to Power BI
st.sidebar.markdown("---")
st.sidebar.header("Export for Power BI")

csv = filtered_orders.to_csv(index=False)
st.sidebar.download_button(
    label="📥 Download CSV for Power BI",
    data=csv,
    file_name="powerbi_export.csv",
    mime="text/csv",
    type="primary"
)


# TOP NAVIGATION using Tabs
st.title("Admin Dashboard 📊")
st.markdown("Powered by Seaborn + Plotly + Streamlit")

# Create tabs for navigation at the top
tab_home, tab_analytics, tab_orders, tab_users = st.tabs(["🏠 Home", "📈 Analytics", "📦 Orders", "👥 Users"])

# ============ HOME TAB ============
with tab_home:
    st.markdown(f"### Showing {len(filtered_orders):,} orders")

    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        total_rev = filtered_orders['amount'].sum()
        kpi_card("Total Revenue", f"₹{total_rev:,.0f}", "+12.5%", "#10B981")
    with col2: 
        kpi_card("Total Orders", f"{len(filtered_orders):,}", "+8.2%", "#3B82F6")
    with col3: 
        kpi_card("Avg Order", f"₹{filtered_orders['amount'].mean():.0f}", "+3.1%", "#8B5CF6")
    with col4: 
        kpi_card("Conversion", f"{(filtered_orders['status']=='delivered').mean()*100:.1f}%", "+2.3%", "#F59E0B")
    with col5: 
        kpi_card("Pending", len(filtered_orders[filtered_orders['status']=='pending']), "-15%", "#EF4444")

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue Trend")
        seaborn_revenue_trend(filtered_orders.tail(30))

    with col2:
        st.subheader("Category Sales")
        seaborn_category_sales(filtered_orders)

    # Charts Row 2
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Order Status Heatmap")
        plotly_status_heatmap(filtered_orders.tail(100), key="heatmap_home")

    with col2:
        st.subheader("Correlations")
        correlation_heatmap(filtered_orders)

    # Additional Charts
    st.markdown("---")
    st.header("Additional Visualizations")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Category Distribution (Pie)")
        pie_chart_category(filtered_orders, key="pie_home")
    
    with col2:
        st.subheader("Status Distribution (Bar)")
        bar_chart_status(filtered_orders, key="bar_home")

    # More Visualizations
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cumulative Revenue")
        area_chart_revenue(filtered_orders, key="area_home")
    
    with col2:
        st.subheader("Order Amount Histogram")
        histogram_order_amounts(filtered_orders, key="hist_home")

    # Advanced Visualizations
    st.markdown("---")
    st.header("Advanced Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Status Breakdown (Donut)")
        donut_chart_status(filtered_orders, key="donut_home")
    
    with col2:
        st.subheader("Category & Status Treemap")
        treemap_category(filtered_orders, key="treemap_home")

    # More Advanced
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Amount by Category (Box Plot)")
        box_plot_amount(filtered_orders, key="box_home")
    
    with col2:
        st.subheader("Conversion Funnel")
        funnel_chart_conversion(filtered_orders, key="funnel_home")

    # Hierarchical Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sunburst Chart")
        sunburst_chart(filtered_orders, key="sunburst_home")
    
    with col2:
        st.subheader("Polar Chart")
        polar_chart_category(filtered_orders, key="polar_home")

    # Scatter Plot
    st.subheader("Customer vs Amount Scatter")
    scatter_plot_amount_customer(filtered_orders, key="scatter_home")

    # Time Series
    st.subheader("Time Series with Moving Averages")
    time_series_decomposition(filtered_orders, key="timeseries_home")

    # Recent Orders
    st.markdown("---")
    st.subheader("Recent Orders")
    st.dataframe(filtered_orders[['order_id', 'timestamp', 'amount', 'status', 'category']].tail(10))

# ============ ANALYTICS TAB ============
with tab_analytics:
    st.markdown("## Detailed Analytics")
    
    st.subheader("Time Series Analysis")
    time_series_decomposition(filtered_orders, key="timeseries_analytics")
    
    st.subheader("Monthly Revenue Trend")
    monthly_trend(filtered_orders, key="monthly_analytics")
    
    st.subheader("Weekly Revenue Pattern")
    weekly_pattern(filtered_orders, key="weekly_analytics")
    
    st.subheader("Top Categories by Revenue")
    top_products(filtered_orders, key="top_analytics")

# ============ ORDERS TAB ============
with tab_orders:
    st.markdown("## Order Management")
    
    st.subheader("Order Status Overview")
    plotly_status_heatmap(filtered_orders, key="heatmap_orders")
    
    st.subheader("Order Conversion Funnel")
    funnel_chart_conversion(filtered_orders, key="funnel_orders")
    
    st.subheader("Order Status Breakdown")
    donut_chart_status(filtered_orders, key="donut_orders")
    
    # Full Orders Table with search
    st.markdown("---")
    st.subheader("All Orders")
    
    search = st.text_input("Search Order ID", "")
    if search:
        orders_display = filtered_orders[filtered_orders['order_id'].astype(str).str.contains(search)]
    else:
        orders_display = filtered_orders
    
    st.dataframe(orders_display[['order_id', 'timestamp', 'amount', 'status', 'category']])

# ============ USERS TAB ============
with tab_users:
    st.markdown("## Customer Analysis")
    
    st.subheader("Customer vs Amount Analysis")
    scatter_plot_amount_customer(filtered_orders, key="scatter_users")
    
    st.subheader("Order Amount Distribution")
    box_plot_amount(filtered_orders, key="box_users")
    
    st.subheader("Order Amount Histogram")
    histogram_order_amounts(filtered_orders, key="hist_users")
    
    # Summary Stats
    st.markdown("---")
    st.subheader("Customer Summary")
    col1, col2 = st.columns(2)
    
    with col1:
        total_customers = filtered_orders['customer_id'].nunique()
        kpi_card("Total Customers", f"{total_customers:,}", "+5.2%", "#3B82F6")
    
    with col2:
        avg_per_customer = filtered_orders.groupby('customer_id')['amount'].sum().mean()
        kpi_card("Avg Spending per Customer", f"₹{avg_per_customer:,.0f}", "+2.8%", "#8B5CF6")
