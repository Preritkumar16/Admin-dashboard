# Admin Dashboard

A powerful admin dashboard built with Streamlit, Plotly, and Seaborn for data visualization and analytics.

## Features
**Home Tab**: KPI cards, revenue trends, category sales, order status heatmap, correlation heatmap, pie/bar/area charts, histograms, donut charts, treemaps, box plots, funnel charts, sunburst/polar charts, scatter plots, and time series
**Analytics Tab**: Time series analysis, monthly/weekly trends, top products, revenue breakdown
**Orders Tab**: Order management with status overview, conversion funnel, and searchable order table
**Users Tab**: Customer analysis with segmentation, top customers, and retention analysis

## Local Setup
1. Install dependencies:
```
bash
pip install -r requirements.txt
```
2. Run the app:
```
bash
streamlit run app.py
```

## Deployment to Streamlit Community Cloud
1. **Push your code to GitHub**:
   - Create a new repository on GitHub
   - Push the `python-dashboard` folder contents to the repository
2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch, and main file path (`app.py`)
   - Click "Deploy"
Your app will be deployed and accessible via a public URL!

## Requirements
- streamlit
- plotly
- seaborn
- pandas
- numpy
- streamlit-aggrid
