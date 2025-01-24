import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px

# Simulate data for all prototypes

# Patient Queue Data
patients = [
    {"Name": "John Doe", "Age": 30, "Condition": "Critical", "Bed Required": "ICU", "Status": "Waiting"},
    {"Name": "Jane Smith", "Age": 25, "Condition": "Stable", "Bed Required": "General", "Status": "Admitted"},
    {"Name": "Sam Brown", "Age": 60, "Condition": "Emergency", "Bed Required": "Emergency", "Status": "Waiting"},
    {"Name": "Anna Lee", "Age": 40, "Condition": "Critical", "Bed Required": "ICU", "Status": "Admitted"},
    {"Name": "Mike Green", "Age": 50, "Condition": "Stable", "Bed Required": "General", "Status": "Waiting"}
]

# Bed Allocation Data
beds = [
    {"Bed Type": "ICU", "Status": "Occupied"},
    {"Bed Type": "General", "Status": "Available"},
    {"Bed Type": "Emergency", "Status": "Occupied"},
    {"Bed Type": "General", "Status": "Occupied"},
    {"Bed Type": "ICU", "Status": "Available"}
]

# Medicine Inventory Data
medicines = [
    {"Name": "Aspirin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 10},
    {"Name": "Paracetamol", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 20},
    {"Name": "Ibuprofen", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 15},
    {"Name": "Amoxicillin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 25},
    {"Name": "Metformin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 30},
]

# Convert to DataFrames
patient_queue = pd.DataFrame(patients)
bed_allocation = pd.DataFrame(beds)
med_stock_status = pd.DataFrame(medicines)

# Apply logic to calculate stock status
med_stock_status['Status'] = med_stock_status.apply(
    lambda row: 'Low Stock' if row['Quantity'] <= row['Low Stock Threshold'] else 'Sufficient', axis=1
)

# Streamlit Dashboard Setup
st.title("Hospital Management Dashboard")

# Sidebar for navigation
option = st.sidebar.selectbox('Choose a Dashboard', ('Patient Queue Management', 'Bed Allocation', 'Medicine Inventory'))

# Patient Queue Management Dashboard
if option == 'Patient Queue Management':
    st.header("Patient Queue Overview")
    
    # Filter by condition or status
    patient_filter = st.selectbox("Filter by Status", patient_queue['Status'].unique())
    filtered_patients = patient_queue[patient_queue['Status'] == patient_filter]
    
    # Display the filtered patient queue
    st.write(filtered_patients)
    
    # Gantt Chart for Patient Flow (if needed)
    fig = px.timeline(filtered_patients, x_start="Age", x_end="Age", y="Name", color="Status")
    st.plotly_chart(fig)

# Bed Allocation Dashboard
elif option == 'Bed Allocation':
    st.header("Bed Allocation Overview")
    
    # Filter by Bed Type
    bed_filter = st.selectbox("Filter by Bed Type", bed_allocation['Bed Type'].unique())
    filtered_beds = bed_allocation[bed_allocation['Bed Type'] == bed_filter]
    
    # Display bed allocation status
    st.write(filtered_beds)
    
    # Visualize Bed Occupancy (Bar chart)
    bed_occupancy = bed_allocation['Status'].value_counts().reset_index()
    bed_occupancy.columns = ['Status', 'Count']
    st.bar_chart(bed_occupancy.set_index('Status'))

# Medicine Inventory Dashboard
elif option == 'Medicine Inventory':
    st.header("Medicine Inventory Overview")
    
    # Filter by Medicine Name
    medicine_filter = st.selectbox("Filter by Medicine", med_stock_status['Name'].unique())
    filtered_medicines = med_stock_status[med_stock_status['Name'] == medicine_filter]
    
    # Display filtered medicine data
    st.write(filtered_medicines)
    
    # Medicine Quantity Distribution (Bar Chart)
    st.subheader(f"Quantity Distribution for {medicine_filter}")
    st.bar_chart(filtered_medicines.set_index('Name')['Quantity'])
    
    # Status Summary (Low Stock vs Sufficient)
    st.subheader("Inventory Status Summary")
    status_summary = filtered_medicines['Status'].value_counts()
    st.write(status_summary)
    
    # Filter by Low Stock Threshold (Slider)
    low_stock_threshold = st.slider("Select Minimum Quantity", min_value=0, max_value=100, value=10)
    low_stock_data = med_stock_status[med_stock_status['Quantity'] <= low_stock_threshold]
    st.subheader(f"Medicines with Stock <= {low_stock_threshold}")
    st.write(low_stock_data)

