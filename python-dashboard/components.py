import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set seaborn style globally
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')

def kpi_card(title, value, change, color="blue"):
    """KPI cards"""
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="font-size: 0.875rem; color: #6B7280;">{title}</div>
        <div style="font-size: 2rem; font-weight: 700; color: #111827;">{value}</div>
        <div style="font-size: 0.875rem; color: {color}; font-weight: 600;">{change}</div>
    </div>
    """, unsafe_allow_html=True)

def seaborn_revenue_trend(df):
    """Seaborn lineplot"""
    fig, ax = plt.subplots(figsize=(10, 6))
    daily_rev = df.groupby(df['timestamp'].dt.date)['amount'].sum().reset_index()
    
    sns.lineplot(data=daily_rev, x='timestamp', y='amount', 
                marker='o', linewidth=3, markersize=8, ax=ax)
    ax.set_title("Revenue Trend", fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    
    st.pyplot(fig)
    plt.close()

def seaborn_category_sales(df):
    """Seaborn barplot with statistical annotations"""
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_sales = df.groupby('category')['amount'].sum().reset_index()
    
    sns.barplot(data=cat_sales, x='category', y='amount', ax=ax, palette='viridis', hue='category', legend=False)
    ax.set_title("Sales by Category", fontsize=16, fontweight='bold')
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'₹{height:,.0f}', (p.get_x() + p.get_width()/2, height),
                   ha='center', va='bottom', fontsize=12)
    
    plt.xticks(rotation=45)
    st.pyplot(fig)
    plt.close()

def plotly_status_heatmap(df, key=None):
    """Plotly heatmap for order status over time"""
    df = df.copy()
    df['date'] = df['timestamp'].dt.date
    pivot = df.groupby(['date', 'status']).size().unstack(fill_value=0)
    
    fig = px.imshow(pivot.values, 
                   x=pivot.columns, y=pivot.index,
                   aspect="auto", color_continuous_scale='RdYlGn_r',
                   title="Order Status Heatmap")
    st.plotly_chart(fig, width='stretch', key=key)

def correlation_heatmap(df):
    """Seaborn correlation matrix"""
    numeric_cols = ['amount', 'customer_id']
    corr_df = df[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', center=0,
               square=True, ax=ax, cbar_kws={'shrink': 0.8})
    ax.set_title("Feature Correlation", fontsize=14, fontweight='bold')
    st.pyplot(fig)
    plt.close()

# Chart functions with unique keys
def pie_chart_category(df, key=None):
    """Pie chart for category distribution"""
    cat_sales = df.groupby('category')['amount'].sum().reset_index()
    
    fig = px.pie(cat_sales, values='amount', names='category',
                 title='Category Distribution',
                 color_discrete_sequence=px.colors.qualitative.Set3,
                 hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, width='stretch', key=key)

def scatter_plot_amount_customer(df, key=None):
    """Scatter plot for amount vs customer analysis"""
    fig = px.scatter(df, x='customer_id', y='amount', 
                     color='status', size='amount',
                     title='Amount vs Customer Analysis',
                     color_discrete_sequence=px.colors.qualitative.Set1,
                     hover_data=['order_id', 'timestamp'])
    st.plotly_chart(fig, width='stretch', key=key)

def bar_chart_status(df, key=None):
    """Bar chart for order status distribution"""
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    fig = px.bar(status_counts, x='status', y='count',
                 title='Order Status Distribution',
                 color='status',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig, width='stretch', key=key)

def area_chart_revenue(df, key=None):
    """Area chart for cumulative revenue over time"""
    daily_rev = df.groupby(df['timestamp'].dt.date)['amount'].sum().reset_index()
    daily_rev = daily_rev.sort_values('timestamp')
    daily_rev['cumulative'] = daily_rev['amount'].cumsum()
    
    fig = px.area(daily_rev, x='timestamp', y='cumulative',
                  title='Cumulative Revenue Over Time',
                  color_discrete_sequence=['#10B981'],
                  labels={'cumulative': 'Cumulative Revenue', 'timestamp': 'Date'})
    fig.update_layout(yaxis_title="Revenue (₹)")
    st.plotly_chart(fig, width='stretch', key=key)

def histogram_order_amounts(df, key=None):
    """Histogram for order amount distribution"""
    fig = px.histogram(df, x='amount', nbins=20,
                       title='Order Amount Distribution',
                       color_discrete_sequence=['#6366F1'],
                       labels={'amount': 'Order Amount (₹)', 'count': 'Frequency'})
    fig.update_traces(marker_line_width=1, marker_line_color='white')
    st.plotly_chart(fig, width='stretch', key=key)

def donut_chart_status(df, key=None):
    """Donut chart for order status breakdown"""
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    fig = px.pie(status_counts, values='count', names='status',
                 title='Order Status Breakdown',
                 color='status',
                 color_discrete_map={
                     'delivered': '#10B981',
                     'pending': '#F59E0B',
                     'cancelled': '#EF4444',
                     'processing': '#3B82F6'
                 },
                 hole=0.5)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, width='stretch', key=key)

def treemap_category(df, key=None):
    """Treemap for hierarchical category analysis"""
    cat_data = df.groupby(['category', 'status'])['amount'].sum().reset_index()
    
    fig = px.treemap(cat_data, path=['category', 'status'], values='amount',
                     title='Category & Status Treemap',
                     color='amount',
                     color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, width='stretch', key=key)

def box_plot_amount(df, key=None):
    """Box plot for amount distribution by category"""
    fig = px.box(df, x='category', y='amount', color='category',
                 title='Order Amount Distribution by Category',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_traces(quartilemethod="exclusive")
    st.plotly_chart(fig, width='stretch', key=key)

def funnel_chart_conversion(df, key=None):
    """Funnel chart for order conversion"""
    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    status_counts = status_counts.sort_values('count', ascending=False)
    
    fig = px.funnel(status_counts, x='count', y='status',
                    title='Order Conversion Funnel',
                    color='status',
                    color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, width='stretch', key=key)

def sunburst_chart(df, key=None):
    """Sunburst chart for hierarchical data"""
    sunburst_data = df.groupby(['category', 'status'])['amount'].sum().reset_index()
    
    fig = px.sunburst(sunburst_data, path=['category', 'status'], values='amount',
                      title='Category to Status Sunburst',
                      color='amount',
                      color_continuous_scale='Viridis')
    st.plotly_chart(fig, width='stretch', key=key)

def polar_chart_category(df, key=None):
    """Polar chart for category comparison"""
    cat_sales = df.groupby('category')['amount'].sum().reset_index()
    
    fig = px.bar_polar(cat_sales, r='amount', theta='category',
                       title='Category Comparison (Polar)',
                       color='amount',
                       color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, width='stretch', key=key)

def time_series_decomposition(df, key=None):
    """Time series trend with moving averages"""
    daily = df.groupby(df['timestamp'].dt.date)['amount'].sum().reset_index()
    daily.columns = ['date', 'amount']
    daily['date'] = pd.to_datetime(daily['date'])
    daily = daily.set_index('date')
    
    daily['MA7'] = daily['amount'].rolling(window=7).mean()
    daily['MA30'] = daily['amount'].rolling(window=30).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily.index, y=daily['amount'], 
                             mode='lines+markers', name='Daily Revenue',
                             line=dict(color='#3B82F6', width=2)))
    fig.add_trace(go.Scatter(x=daily.index, y=daily['MA7'], 
                             mode='lines', name='7-Day MA',
                             line=dict(color='#10B981', width=2)))
    fig.add_trace(go.Scatter(x=daily.index, y=daily['MA30'], 
                             mode='lines', name='30-Day MA',
                             line=dict(color='#F59E0B', width=2)))
    
    fig.update_layout(title='Revenue Time Series with Moving Averages',
                      xaxis_title='Date', yaxis_title='Revenue (₹)',
                      hovermode='x unified')
    st.plotly_chart(fig, width='stretch', key=key)

def monthly_trend(df, key=None):
    """Monthly revenue trend analysis"""
    df = df.copy()
    df['month'] = df['timestamp'].dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum().reset_index()
    monthly['month'] = monthly['month'].astype(str)
    
    fig = px.bar(monthly, x='month', y='amount',
                 title='Monthly Revenue Trend',
                 color='amount',
                 color_continuous_scale='Blues',
                 text='amount')
    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig.update_layout(xaxis_title='Month', yaxis_title='Revenue (₹)')
    st.plotly_chart(fig, width='stretch', key=key)

def weekly_pattern(df, key=None):
    """Weekly pattern analysis"""
    df = df.copy()
    df['day_of_week'] = df['timestamp'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly = df.groupby('day_of_week')['amount'].agg(['sum', 'mean', 'count']).reset_index()
    weekly = weekly.set_index('day_of_week').reindex(day_order).reset_index()
    
    fig = px.bar(weekly, x='day_of_week', y='sum',
                 title='Weekly Revenue Pattern',
                 color='sum',
                 color_continuous_scale='Tealgrn',
                 text='count')
    fig.update_traces(texttemplate='₹%{y:,.0f}', textposition='outside')
    fig.update_layout(xaxis_title='Day of Week', yaxis_title='Total Revenue (₹)')
    st.plotly_chart(fig, width='stretch', key=key)

def top_products(df, key=None):
    """Top categories by revenue"""
    top = df.groupby('category')['amount'].sum().reset_index()
    top = top.sort_values('amount', ascending=False).head(10)
    
    fig = px.bar(top, x='amount', y='category', orientation='h',
                 title='Top Categories by Revenue',
                 color='amount',
                 color_continuous_scale='Greens',
                 text='amount')
    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='inside')
    fig.update_layout(yaxis_title='Category', xaxis_title='Revenue (₹)')
    st.plotly_chart(fig, width='stretch', key=key)

def revenue_breakdown(df, key=None):
    """Revenue breakdown by category and status"""
    # Category breakdown
    cat_rev = df.groupby('category')['amount'].sum().reset_index()
    cat_rev = cat_rev.sort_values('amount', ascending=False)
    
    fig1 = px.bar(cat_rev, x='category', y='amount',
                   title='Revenue by Category',
                   color='amount',
                   color_continuous_scale='Viridis',
                   text='amount')
    fig1.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig1.update_layout(xaxis_title='Category', yaxis_title='Revenue (₹)')
    st.plotly_chart(fig1, width='stretch', key=f"{key}_cat" if key else None)
    
    # Status breakdown
    status_rev = df.groupby('status')['amount'].sum().reset_index()
    status_rev = status_rev.sort_values('amount', ascending=False)
    
    fig2 = px.bar(status_rev, x='status', y='amount',
                   title='Revenue by Status',
                   color='status',
                   color_discrete_sequence=px.colors.qualitative.Set2,
                   text='amount')
    fig2.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig2.update_layout(xaxis_title='Status', yaxis_title='Revenue (₹)')
    st.plotly_chart(fig2, width='stretch', key=f"{key}_status" if key else None)
