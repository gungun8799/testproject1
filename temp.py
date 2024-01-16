import streamlit as st
import pandas as pd
import plotly.express as px
from dateutil import parser
from datetime import datetime

def load_data():
    """Load the data from the CSV file"""
    try:
        df = pd.read_csv('Video_Performance_Over_Time.csv')
        df['Date'] = df['Date'].apply(lambda x: parser.parse(x) if pd.notnull(x) else None)
        return df, None
    except Exception as e:
        return None, e

# Load the data and error message
df, error = load_data()

# Streamlit UI
st.title('Video Performance Dashboard')

if df is not None:
    # Sidebar - Date and Length selection
    selected_date = st.sidebar.date_input("Select a Date", datetime.today())
    length_ranges = ["200-400", "400-800", "800-1600", "1600-2000"]
    selected_range = st.sidebar.selectbox("Select Video Length Range", length_ranges)

    # Parse the selected range
    min_length, max_length = map(int, selected_range.split('-'))

    # Filter based on date and length range
    filtered_df = df[(df['Date'] == pd.Timestamp(selected_date)) &
                     (df['Video Length'] >= min_length) &
                     (df['Video Length'] <= max_length)]

    # Pie Chart
    if not filtered_df.empty:
        fig = px.pie(filtered_df, names='Video Length', title='Video Length Distribution')
        st.plotly_chart(fig)

        st.write(f"Videos published on {selected_date} with length {selected_range}:")
        st.dataframe(filtered_df)
    else:
        st.write("No videos match the criteria.")
else:
    st.error(f"Failed to load data: {error}")
