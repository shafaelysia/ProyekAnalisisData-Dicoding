# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

# Set seaborn style
sns.set(style='dark')

# Function to create rents over time data frame
def create_rents_over_time(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    monthly_df = df.resample('M', on='dteday').sum()
    return monthly_df

# Function to aggregate bike rentals by season data frame
def by_season(df):
    season_agg = df.groupby("season_x").agg({
        "instant_x": "nunique",
        "cnt_x": ["max", "min"]
    })
    return season_agg

# Function to aggregate bike rentals by month data frame
def by_month(df):
    monthly_agg = df.groupby("mnth_x").agg({
        "instant_x": "nunique",
        "cnt_x": ["max", "min"]
    })
    return monthly_agg

# Function to aggregate bike rentals by day data frame
def by_day(df):
    weekday_agg = df.groupby("weekday_x").agg({
        "instant_x": "nunique",
        "cnt_x": ["max", "min"]
    })
    return weekday_agg

# Function to aggregate bike rentals by hour data frame
def by_hour(df):
    hourly_agg = df.groupby("hr").agg({
        "instant_y": "nunique",
        "cnt_y": ["max", "min"]
    })
    return hourly_agg


# Load csv files
main_df = pd.read_csv("main_data.csv")
datetime_columns = ["dteday"]
main_df.sort_values(by="dteday", inplace=True)
main_df.reset_index(inplace=True)

for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])

# Streamlit Sidebar
with st.sidebar:
    # Add Header
    st.header("Proyek Analisis Data")
    st.header("Dashboard Bike-Sharing")

# Create Dataframes
rents_over_time_df = create_rents_over_time(main_df)
byseason_df = by_season(main_df)
bymonth_df = by_month(main_df)
byday_df = by_day(main_df)
byhour_df = by_hour(main_df)

# Bike Rentals Over Time (Aggregated by Month) Visualization
st.subheader("Bike Rentals Over Time")
plt.figure(figsize=(10, 6))
plt.plot(rents_over_time_df.index, rents_over_time_df['cnt_x'])
plt.xlabel('Month')
plt.ylabel('Number of Bike Rentals')
plt.title('Bike Rentals Over Time (Aggregated by Month)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Bike Rentals by Season Visualization
st.subheader("Bike Rentals by Season")
plt.figure(figsize=(10, 6))
x = byseason_df.index
y_max = byseason_df[('cnt_x', 'max')]
y_min = byseason_df[('cnt_x', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='lightblue')
plt.bar(x, y_min, label='Min Rentals', color='lightgreen')
season_labels = ['1', '2', '3', '4']
plt.xticks(x, season_labels)
plt.xlabel('Season')
plt.ylabel('Number of Bike Rentals')
plt.title('Max and Min Bike Rentals by Season')
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i+1, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i+1, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Bike Rentals by Month Visualization
st.subheader("Bike Rentals by Month")
plt.figure(figsize=(10, 7))
y = np.arange(len(bymonth_df.index))
y_max = bymonth_df[('cnt_x', 'max')]
y_min = bymonth_df[('cnt_x', 'min')]
bar_width = 0.5
plt.barh(y, y_max, height=bar_width, label='Max Rentals', color='lightblue')
plt.barh(y, y_min, height=bar_width, label='Min Rentals', color='lightgreen')
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.yticks(y + bar_width / 2, month_labels)
plt.xlabel('Number of Bike Rentals')
plt.ylabel('Month')
plt.title('Max and Min Bike Rentals by Month')
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(max_val, i, str(max_val), ha='left', va='center', fontweight='bold')
    plt.text(min_val, i + bar_width, str(min_val), ha='left', va='center', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Bike Rentals by Day Visualization
st.subheader("Bike Rentals by Day in a Week")
plt.figure(figsize=(10, 6))
x = byday_df.index
y_max = byday_df[('cnt_x', 'max')]
y_min = byday_df[('cnt_x', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='lightblue')
plt.bar(x, y_min, label='Min Rentals', color='lightgreen')
plt.xlabel('Weekday')
plt.ylabel('Number of Bike Rentals')
plt.title('Max and Min Bike Rentals by Weekday')
plt.xticks(rotation=0)
plt.legend()
for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Bike Rentals by Hour Visualization
st.subheader("Bike Rentals by Hour")
plt.figure(figsize=(10, 6))
x = byhour_df.index
y_max = byhour_df[('cnt_y', 'max')]
y_min = byhour_df[('cnt_y', 'min')]
plt.bar(x, y_max, label='Max Rentals', color='lightblue')
plt.bar(x, y_min, label='Min Rentals', color='lightgreen')
plt.xlabel('Hour')
plt.ylabel('Number of Bike Rentals')
plt.title('Max and Min Bike Rentals by Hour')
hour_labels = [str(i) for i in x]
plt.xticks(x, hour_labels)
plt.legend()

for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)