import pandas as pd
import streamlit as st
import random
from datetime import datetime, timedelta

# Generate dummy data for medicines
medicines = [
    {"Name": "Aspirin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 10},
    {"Name": "Paracetamol", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 20},
    {"Name": "Ibuprofen", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 15},
    {"Name": "Amoxicillin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 25},
    {"Name": "Metformin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 30},
]

# Convert to DataFrame
med_stock_status = pd.DataFrame(medicines)

# Apply the logic row-wise for comparing Quantity with Low Stock Threshold
med_stock_status['Status'] = med_stock_status.apply(
    lambda row: 'Low Stock' if row['Quantity'] <= row['Low Stock Threshold'] else 'Sufficient', axis=1
)

# Streamlit Dashboard Setup
st.title("Hospital Medicine Inventory Dashboard")

# Create a slicer for medicine name filter
medicine_filter = st.selectbox("Select Medicine", med_stock_status['Name'].unique())

# Filter data based on selected medicine
filtered_data = med_stock_status[med_stock_status['Name'] == medicine_filter]

# Display filtered data
st.subheader(f"Inventory for {medicine_filter}")
st.write(filtered_data)

# Create a bar chart for quantity distribution
st.subheader("Medicine Quantity Distribution")
st.bar_chart(filtered_data.set_index('Name')['Quantity'])

# Display a summary of the status
st.subheader("Inventory Status Summary")
status_summary = filtered_data['Status'].value_counts()
st.write(status_summary)

# Slicer to filter by quantity thresholds (for low stock)
low_stock_threshold = st.slider("Select Minimum Quantity", min_value=0, max_value=100, value=10)

# Filter based on low stock threshold
low_stock_data = med_stock_status[med_stock_status['Quantity'] <= low_stock_threshold]
st.subheader(f"Medicines with Stock <= {low_stock_threshold}")
st.write(low_stock_data)

