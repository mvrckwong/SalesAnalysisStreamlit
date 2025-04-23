import pandas as pd  
import streamlit as st
from pathlib import Path

from core.logging import APP_DIR, PROJ_DIR, DATA_DIR, \
    TEST_DIR, CONT_DIR

# Constants
DATA_PATH = Path("path/to/data")  # Change this to your actual data directory
DATA_FILE = DATA_DIR / 'supermarket_sales.csv'

# Page Config
st.set_page_config(
    page_title="Sales Dashboard", 
    page_icon="📊", 
    layout="centered"
)

@st.cache_data
def load_data(file_path):
    """Load and preprocess the sales data."""
    df = pd.read_csv(file_path)
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    return df

def sidebar_filters(df):
    """Generate sidebar filters and return filtered data."""
    city = st.sidebar.multiselect("Select the City:", options=df["City"].unique(), default=df["City"].unique())
    customer_type = st.sidebar.multiselect("Select the Customer Type:", options=df["Customer_type"].unique(), default=df["Customer_type"].unique())
    gender = st.sidebar.multiselect("Select the Gender:", options=df["Gender"].unique(), default=df["Gender"].unique())
    
    if not city: city = df["City"].unique()
    if not customer_type: customer_type = df["Customer_type"].unique()
    if not gender: gender = df["Gender"].unique()

    return df.query("City == @city & Customer_type == @customer_type & Gender == @gender")

def display_kpis(df):
    """Display the top KPIs."""
    total_sales = int(df["Total"].sum())
    average_rating = round(df["Rating"].mean(), 1)
    average_sale_by_transaction = round(df["Total"].mean(), 2)

    st.markdown("##")
    st.write("---")
    st.markdown("### **Key Performance Indicators**")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"US $ {total_sales:,}")
    col2.metric("Average Rating", f"{average_rating}")
    col3.metric("Avg Sales/Transaction", f"US $ {average_sale_by_transaction}")
    st.write("---")

def plot_bar_chart(df, group_by, title):
    """Plot and display a bar chart."""
    chart_data = df.groupby(by=[group_by]).sum()[["Total"]].sort_values(by="Total")
    st.subheader(title)
    st.bar_chart(chart_data, use_container_width=True)
    st.write(" ")

def main():
    # Load Data
    df = load_data(DATA_FILE)

    # Sidebar Filters
    df_filtered = sidebar_filters(df)

    # Main Page
    st.title("📊 Sales Dashboard")
    st.markdown("## Overview of Sales Performance")
    display_kpis(df_filtered)

    # Tabs for different charts
    tabs = st.tabs(["Product Line", "Hour", "Gender", "Customer Type", "City"])

    tab_titles = ["Sales by Product Line", "Sales by Hour", "Sales by Gender", "Sales by Customer Type", "Sales by City"]
    group_bys = ["Product line", "hour", "Gender", "Customer_type", "City"]

    for tab, title, group_by in zip(tabs, tab_titles, group_bys):
        with tab:
            plot_bar_chart(df_filtered, group_by, title)

if __name__ == "__main__":
    main()
