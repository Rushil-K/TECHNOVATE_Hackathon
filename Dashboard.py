import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
import plotly.express as px
import matplotlib.pyplot as plt

# Dummy Data Creation

# Medicine Inventory Data
medicines_data = pd.DataFrame({
    'Name': ['Paracetamol', 'Ibuprofen', 'Aspirin', 'Amoxicillin', 'Metformin'],
    'Quantity': [random.randint(5, 50) for _ in range(5)],
    'Expiry Date': [datetime(2025, random.randint(1, 12), random.randint(1, 28)).strftime('%Y-%m-%d') for _ in range(5)],
    'Low Stock Threshold': [10, 10, 15, 5, 20],
})

# Patient Queue Data
patients_data = pd.DataFrame({
    'Patient ID': [f'P{1001 + i}' for i in range(5)],
    'Name': ['John Doe', 'Jane Smith', 'Alice Brown', 'Bob Johnson', 'Emily Davis'],
    'Condition': ['Critical', 'Routine', 'Emergency', 'Routine', 'Critical'],
    'Bed Required': ['ICU', 'General', 'Emergency', 'General', 'ICU'],
    'Priority': [1, 3, 2, 3, 1],
})

# Bed Allocation Data
bed_data = pd.DataFrame({
    'Bed ID': [f'B{101 + i}' for i in range(5)],
    'Unit': ['ICU', 'General', 'Emergency', 'General', 'ICU'],
    'Occupied': [random.choice([True, False]) for _ in range(5)],
})

# Streamlit Page Configuration
st.set_page_config(page_title="Hospital Management Dashboard", layout="wide")

# Dashboard Header
st.title("🏥 Hospital Management Dashboard")
st.markdown("Manage patient queues, bed allocation, and medicine inventory seamlessly.")

# Medicine Inventory Section
st.header("Medicine Inventory Management")
st.subheader("Filter Medicine Data")

# Filters (Slicers)
medicine_name_filter = st.selectbox("Filter by Medicine Name", ['All'] + medicines_data['Name'].tolist())
quantity_filter = st.slider("Filter by Quantity", min_value=0, max_value=50, value=(0, 50))

# Filter the data based on slicers
filtered_medicines = medicines_data[
    (medicines_data['Name'].str.contains(medicine_name_filter, case=False) | (medicine_name_filter == 'All')) &
    (medicines_data['Quantity'].between(quantity_filter[0], quantity_filter[1]))
]

# Medicine Stock Status Pie Chart
med_stock_status = filtered_medicines.copy()
med_stock_status['Status'] = med_stock_status['Quantity'].apply(lambda x: 'Low Stock' if x <= med_stock_status['Low Stock Threshold'] else 'Sufficient')

# Plotting Pie Chart for Medicine Stock Status
fig = px.pie(med_stock_status, names='Status', title='Medicine Stock Status', color='Status', 
             color_discrete_map={'Low Stock': 'red', 'Sufficient': 'green'})
st.plotly_chart(fig)

# Display filtered medicines table
st.dataframe(filtered_medicines)

# Patient Queue Section
st.header("Patient Queue Management")
st.subheader("Filter Patient Queue")

# Filters (Slicers)
condition_filter = st.selectbox("Filter by Condition", ['All'] + patients_data['Condition'].unique().tolist())
priority_filter = st.slider("Filter by Priority", min_value=1, max_value=3, value=(1, 3))

# Filter the data based on slicers
filtered_patients = patients_data[
    (patients_data['Condition'].str.contains(condition_filter, case=False) | (condition_filter == 'All')) &
    (patients_data['Priority'].between(priority_filter[0], priority_filter[1]))
]

# Display filtered patients table
st.dataframe(filtered_patients)

# Bed Allocation Section
st.header("Bed Allocation Management")
st.subheader("Filter Bed Data")

# Filters (Slicers)
unit_filter = st.selectbox("Filter by Unit", ['All'] + bed_data['Unit'].unique().tolist())
status_filter = st.selectbox("Filter by Status", ['All', 'Occupied', 'Available'])

# Filter the data based on slicers
filtered_beds = bed_data[
    (bed_data['Unit'].str.contains(unit_filter, case=False) | (unit_filter == 'All')) &
    ((bed_data['Occupied'] == (status_filter == 'Occupied')) | (status_filter == 'All'))
]

# Bed Availability Bar Chart
bed_availability = filtered_beds.groupby('Unit')['Occupied'].value_counts().unstack().fillna(0)
bed_availability_plot = bed_availability.plot(kind='bar', stacked=True, color=['#ff4d4d', '#4dff4d'], figsize=(10, 6))
bed_availability_plot.set_ylabel('Count of Beds')
bed_availability_plot.set_title('Bed Availability by Unit')

# Display the bar chart
st.pyplot(bed_availability_plot)

# Display filtered bed data table
st.dataframe(filtered_beds)

