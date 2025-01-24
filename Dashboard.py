import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Simulate data for all prototypes

# Patient Queue Data with Indian Names
patients = [
    {"Name": "Aarav Sharma", "Age": 30, "Condition": "Critical", "Bed Required": "ICU", "Status": "Waiting"},
    {"Name": "Priya Verma", "Age": 25, "Condition": "Stable", "Bed Required": "General", "Status": "Admitted"},
    {"Name": "Ravi Patel", "Age": 60, "Condition": "Emergency", "Bed Required": "Emergency", "Status": "Waiting"},
    {"Name": "Neha Gupta", "Age": 40, "Condition": "Critical", "Bed Required": "ICU", "Status": "Admitted"},
    {"Name": "Vikram Singh", "Age": 50, "Condition": "Stable", "Bed Required": "General", "Status": "Waiting"},
    {"Name": "Ishaan Yadav", "Age": 55, "Condition": "Critical", "Bed Required": "ICU", "Status": "Admitted"},
    {"Name": "Sanya Khanna", "Age": 28, "Condition": "Stable", "Bed Required": "General", "Status": "Admitted"},
    {"Name": "Rohit Mehta", "Age": 70, "Condition": "Emergency", "Bed Required": "Emergency", "Status": "Waiting"},
    {"Name": "Shivani Reddy", "Age": 45, "Condition": "Stable", "Bed Required": "General", "Status": "Admitted"},
    {"Name": "Aman Kapoor", "Age": 33, "Condition": "Critical", "Bed Required": "ICU", "Status": "Waiting"}
]

# Bed Allocation Data
beds = [
    {"Bed Type": "ICU", "Status": "Occupied"},
    {"Bed Type": "General", "Status": "Available"},
    {"Bed Type": "Emergency", "Status": "Occupied"},
    {"Bed Type": "General", "Status": "Occupied"},
    {"Bed Type": "ICU", "Status": "Available"}
]

# Medicine Inventory Data with Indian Medicines
medicines = [
    {"Name": "Paracetamol", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 10},
    {"Name": "Aspirin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 20},
    {"Name": "Ibuprofen", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 15},
    {"Name": "Amoxicillin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 25},
    {"Name": "Metformin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 30},
    {"Name": "Azithromycin", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 15},
    {"Name": "Cetirizine", "Quantity": random.randint(1, 100), "Expiry Date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"), "Low Stock Threshold": 10}
]

# Hospital Equipment Inventory
equipment = [
    {"Name": "Defibrillator", "Quantity": random.randint(1, 20), "Condition": "Good"},
    {"Name": "Ventilator", "Quantity": random.randint(1, 20), "Condition": "Good"},
    {"Name": "ECG Machine", "Quantity": random.randint(1, 20), "Condition": "Fair"},
    {"Name": "X-Ray Machine", "Quantity": random.randint(1, 10), "Condition": "Good"},
    {"Name": "Blood Pressure Monitor", "Quantity": random.randint(1, 50), "Condition": "Excellent"}
]

# Convert to DataFrames
patient_queue = pd.DataFrame(patients)
bed_allocation = pd.DataFrame(beds)
med_stock_status = pd.DataFrame(medicines)
equipment_inventory = pd.DataFrame(equipment)

# Apply logic to calculate stock status
med_stock_status['Status'] = med_stock_status.apply(
    lambda row: 'Low Stock' if row['Quantity'] <= row['Low Stock Threshold'] else 'Sufficient', axis=1
)

# Streamlit Dashboard Setup
st.title("Hospital Management Dashboard")

# Sidebar for navigation
option = st.sidebar.selectbox('Choose a Dashboard', ('Patient Queue Management', 'Bed Allocation', 'Medicine Inventory', 'Hospital Equipment'))

# Patient Queue Management Dashboard
if option == 'Patient Queue Management':
    st.header("Patient Queue Overview")
    
    # Filter by condition or status
    patient_filter = st.selectbox("Filter by Status", patient_queue['Status'].unique())
    filtered_patients = patient_queue[patient_queue['Status'] == patient_filter]
    
    # Display the filtered patient queue
    st.write(filtered_patients)
    
    # Ribbon Chart (Stacked Bar Chart) for Patient Flow (Queue Visualization)
    status_dist = filtered_patients['Status'].value_counts().reset_index()
    status_dist.columns = ['Status', 'Count']
    fig = px.bar(status_dist, x='Status', y='Count', color='Status', title="Patient Queue Status Distribution")
    st.plotly_chart(fig)

# Bed Allocation Dashboard
elif option == 'Bed Allocation':
    st.header("Bed Allocation Overview")
    
    # Filter by Bed Type
    bed_filter = st.selectbox("Filter by Bed Type", bed_allocation['Bed Type'].unique())
    filtered_beds = bed_allocation[bed_allocation['Bed Type'] == bed_filter]
    
    # Display bed allocation status
    st.write(filtered_beds)
    
    # Visualize Bed Occupancy (Pie chart)
    bed_occupancy = bed_allocation['Status'].value_counts()
    fig = px.pie(values=bed_occupancy, names=bed_occupancy.index, title="Bed Occupancy Status")
    st.plotly_chart(fig)

# Medicine Inventory Dashboard
elif option == 'Medicine Inventory':
    st.header("Medicine Inventory Overview")
    
    # Filter by Medicine Name
    medicine_filter = st.selectbox("Filter by Medicine", med_stock_status['Name'].unique())
    filtered_medicines = med_stock_status[med_stock_status['Name'] == medicine_filter]
    
    # Display filtered medicine data
    st.write(filtered_medicines)
    
    # Bar Chart for Quantity Distribution
    st.subheader(f"Quantity Distribution for {medicine_filter}")
    st.bar_chart(filtered_medicines.set_index('Name')['Quantity'])
    
    # Status Summary (Low Stock vs Sufficient - Pie Chart)
    st.subheader("Inventory Status Summary")
    status_summary = filtered_medicines['Status'].value_counts()
    fig = px.pie(values=status_summary, names=status_summary.index, title="Stock Status Summary")
    st.plotly_chart(fig)
    
    # Visualize Low Stock Threshold for Medicines with Bullet Chart
    st.subheader("Low Stock Threshold Visualization")
    
    for _, row in filtered_medicines.iterrows():
        # Bullet chart to display low stock threshold against the current stock
        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta",
            value=row['Quantity'],
            delta={'reference': row['Low Stock Threshold'], 'position': "top", 'valueformat': ".0f"},
            gauge={
                'shape': "bullet",
                'axis': {'range': [0, row['Low Stock Threshold'] * 2]},
                'steps': [
                    {'range': [0, row['Low Stock Threshold']], 'color': "red"},
                    {'range': [row['Low Stock Threshold'], row['Low Stock Threshold'] * 2], 'color': "green"}
                ],
            },
            title={'text': f"{row['Name']} Stock Level"}
        ))
        st.plotly_chart(fig)
    
    # Filter by Low Stock Threshold (Slider)
    low_stock_threshold = st.slider("Select Minimum Quantity", min_value=0, max_value=100, value=10)
    low_stock_data = med_stock_status[med_stock_status['Quantity'] <= low_stock_threshold]
    st.subheader(f"Medicines with Stock <= {low_stock_threshold}")
    st.write(low_stock_data)

# Hospital Equipment Inventory Dashboard
elif option == 'Hospital Equipment':
    st.header("Hospital Equipment Inventory Overview")
    
    # Filter by Equipment Condition
    equipment_filter = st.selectbox("Filter by Equipment Condition", equipment_inventory['Condition'].unique())
    filtered_equipment = equipment_inventory[equipment_inventory['Condition'] == equipment_filter]
    
    # Display filtered equipment data
    st.write(filtered_equipment)
    
    # Pie chart for Equipment Condition distribution
    equipment_condition_dist = filtered_equipment['Condition'].value_counts()
    fig = px.pie(values=equipment_condition_dist, names=equipment_condition_dist.index, title="Equipment Condition Distribution")
    st.plotly_chart(fig)
