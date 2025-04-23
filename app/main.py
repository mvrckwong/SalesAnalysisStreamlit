import pandas as pd
import streamlit as st
from pathlib import Path

# Assuming 'core.logging' and DATA_DIR setup exists elsewhere
# from core.logging import APP_DIR, PROJ_DIR, DATA_DIR, \
#     TEST_DIR, CONT_DIR
# Using a placeholder for DATA_DIR if the import isn't fully represented
try:
    from core.logging import DATA_DIR
except ImportError:
    # Define DATA_DIR relative to the script if core.logging isn't found
    DATA_DIR = Path(__file__).parent / "data" # Adjust if needed
    DATA_DIR.mkdir(exist_ok=True) # Create if it doesn't exist


# Constants
# DATA_PATH = Path("path/to/data")  # This is unused, can be removed
DATA_FILE = DATA_DIR / 'supermarket_sales.csv' # Make sure this path is correct

# Page Config
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="centered"
)

@st.cache_data
def load_data(file_path):
    """Load and preprocess the sales data."""
    try:
        df = pd.read_csv(file_path)
        # Ensure 'Time' column exists before processing
        if "Time" in df.columns:
             # Handle potential errors during time conversion gracefully
            try:
                df["hour"] = pd.to_datetime(df["Time"], format="%H:%M", errors='coerce').dt.hour
                # Optional: Handle rows where time conversion failed (NaT)
                # df = df.dropna(subset=['hour']) # Drop rows with invalid times
                # df['hour'] = df['hour'].astype(int) # Convert to integer if needed
            except Exception as e:
                st.error(f"Error converting 'Time' column: {e}")
                # Create a dummy 'hour' column or handle as needed
                df["hour"] = 0 # Or some other default
        else:
             st.warning("Column 'Time' not found in the CSV. 'hour' column will not be created.")
             df["hour"] = 0 # Create a dummy 'hour' column
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file not found at {file_path}")
        st.warning("Please ensure 'supermarket_sales.csv' is in the 'data' directory relative to the script, or update the DATA_FILE path.")
        return pd.DataFrame() # Return empty DataFrame to prevent further errors
    except Exception as e:
        st.error(f"An error occurred loading data: {e}")
        return pd.DataFrame()


def sidebar_filters(df):
    """Generate sidebar filters and return filtered data using boolean indexing."""
    st.sidebar.header("Apply Filters:")
    city = st.sidebar.multiselect(
        "Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique()
    )
    customer_type = st.sidebar.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique()
    )
    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )

    # Start with the original DataFrame (or a copy)
    df_selection = df.copy()

    # Apply filters only if a selection has been made in the multiselect
    # If a multiselect is empty, it means the user doesn't want to filter by that criteria
    if city:
        df_selection = df_selection[df_selection["City"].isin(city)]
    # Add a check to prevent error if the initial df is empty
    if customer_type and not df_selection.empty:
        df_selection = df_selection[df_selection["Customer_type"].isin(customer_type)]
    if gender and not df_selection.empty:
        df_selection = df_selection[df_selection["Gender"].isin(gender)]

    # If all filters are deselected resulting in an empty intermediate df_selection,
    # it might be desired to show "No data" or the unfiltered df.
    # Current logic: returns an empty DataFrame if filters result in no matches.
    # If you prefer showing ALL data when filters result in no matches,
    # you might add a check at the end:
    # if df_selection.empty and (city or customer_type or gender):
    #     st.warning("No data matches the selected filters.")
    #     # return pd.DataFrame(columns=df.columns) # Return empty structure
    # elif not (city or customer_type or gender): # No filters selected at all
    #      return df # Return original unfiltered data

    return df_selection

def display_kpis(df):
    """Display the top KPIs. Handles potential division by zero if df is empty."""
    if df.empty:
        st.warning("No data available for the selected filters to calculate KPIs.")
        total_sales = 0
        average_rating = 0
        average_sale_by_transaction = 0
    else:
        total_sales = int(df["Total"].sum())
        average_rating = round(df["Rating"].mean(), 1)
        average_sale_by_transaction = round(df["Total"].mean(), 2)

    st.markdown("##")
    st.write("---")
    st.markdown("### **Key Performance Indicators**")
    #st.write("---") # Removed extra separator

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"US $ {total_sales:,}")
    col2.metric("Average Rating", f"{average_rating}")
    col3.metric("Avg Sales/Transaction", f"US $ {average_sale_by_transaction}")
    st.write("---")

def plot_bar_chart(df, group_by, title):
    """Plot and display a bar chart. Handles empty DataFrame."""
    st.subheader(title)
    if df.empty or group_by not in df.columns:
        st.warning(f"No data to display for '{title}'.")
        return

    # Ensure 'Total' column exists and is numeric
    if "Total" not in df.columns or not pd.api.types.is_numeric_dtype(df["Total"]):
         st.error(f"Cannot plot '{title}': 'Total' column is missing or not numeric.")
         return

    try:
        # Group by the specified column, sum the 'Total', handle potential missing groups
        chart_data = df.groupby(by=[group_by], observed=True).agg(Total=('Total', 'sum'))
        # Sort values for better visualization
        chart_data = chart_data.sort_values(by="Total")

        if chart_data.empty:
            st.warning(f"No data to display for '{title}' after grouping.")
        else:
            st.bar_chart(chart_data, use_container_width=True)

    except KeyError as e:
        st.error(f"Error plotting '{title}': Column '{e}' not found.")
    except Exception as e:
         st.error(f"An error occurred plotting '{title}': {e}")

    st.write(" ") # Add some spacing

def main():
    # Load Data
    df = load_data(DATA_FILE)

    # Check if data loading was successful
    if df.empty:
        st.stop() # Stop execution if data couldn't be loaded

    # Ensure required columns exist before proceeding
    required_cols = ["City", "Customer_type", "Gender", "Total", "Rating", "Product line", "hour"] # Add all needed columns
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"The following required columns are missing from the data: {', '.join(missing_cols)}")
        st.stop()


    # Sidebar Filters
    df_filtered = sidebar_filters(df)

    # Main Page
    st.title("📊 Sales Dashboard")
    st.markdown("## Overview of Sales Performance")

    # Display KPIs based on filtered data
    display_kpis(df_filtered)

    # Tabs for different charts
    # Define tabs, titles, and grouping columns
    tab_definitions = {
        "Product Line": "Product line",
        "Hour": "hour",
        "Gender": "Gender",
        "Customer Type": "Customer_type",
        "City": "City"
    }
    tab_names = list(tab_definitions.keys())
    tabs = st.tabs(tab_names)

    group_bys = list(tab_definitions.values())
    tab_titles = [f"Sales by {name}" for name in tab_names] # Generate titles dynamically

    # Iterate through tabs and plot charts
    for i, tab in enumerate(tabs):
        with tab:
            # Pass the filtered dataframe to the plotting function
            plot_bar_chart(df_filtered, group_bys[i], tab_titles[i])


if __name__ == "__main__":
    main()