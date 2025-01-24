import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime
import plotly.express as px

# 1. Generate 500 Patients Data (Indian Names, Conditions, and Bed Requirements)
indian_names = [
    "Rajesh Kumar", "Aarti Sharma", "Suresh Patel", "Priya Singh", "Manish Gupta", "Neha Verma", "Deepak Reddy", "Rina Mehta",
    "Vikram Chauhan", "Simran Kaur"
]
conditions = ['Critical', 'Non-Critical', 'Stable', 'Emergency']
bed_categories = ['ICU', 'General', 'Emergency']

# Generate random data for 500 patients
patients = []
for i in range(500):
    name = random.choice(indian_names)
    age = random.randint(20, 75)
    condition = random.choice(conditions)
    bed_required = random.choice(bed_categories)
    admitted_date = datetime.now() - pd.to_timedelta(np.random.randint(0, 7), unit='D')  # Random admission date within the last week
    patients.append([name, age, condition, bed_required, admitted_date])

patients_df = pd.DataFrame(patients, columns=["Name", "Age", "Condition", "Bed Required", "Admission Date"])

# 2. Medicine Inventory Data (Indian Medicines)
medicines = [
    "Paracetamol", "Amoxicillin", "Ibuprofen", "Dolo 650", "Aspirin", "Ciprofloxacin", "Clavam", "Azithromycin",
    "Losartan", "Metformin"
]

med_inventory = []
for med in medicines:
    quantity = random.randint(10, 200)
    expiry_date = datetime.now() + pd.to_timedelta(np.random.randint(30, 365), unit='D')  # Random expiry date
    low_stock_threshold = random.randint(20, 50)
    added_date = datetime.now() - pd.to_timedelta(np.random.randint(0, 7), unit='D')  # Random added date within the last week
    med_inventory.append([med, quantity, expiry_date, low_stock_threshold, added_date])

med_inventory_df = pd.DataFrame(med_inventory, columns=["Medicine Name", "Quantity", "Expiry Date", "Low Stock Threshold", "Added Date"])
med_inventory_df['Status'] = med_inventory_df['Quantity'].apply(lambda x: 'Low Stock' if x <= med_inventory_df['Low Stock Threshold'] else 'Sufficient')

# 3. Medical Equipment Data (Indian Brands and Status)
equipment_types = ['Ventilator', 'ECG Machine', 'Defibrillator', 'Syringe Pump', 'Infusion Pump', 'X-Ray Machine']
equipment_brands = ['BPL', 'Siemens', 'GE Healthcare', 'Philips', 'Medtronic']

equipment_inventory = []
for equip in equipment_types:
    status = random.choice(['Functional', 'Under Repair'])
    brand = random.choice(equipment_brands)
    equipment_inventory.append([equip, brand, status])

equipment_df = pd.DataFrame(equipment_inventory, columns=["Equipment Name", "Brand", "Status"])

# 4. Bed Allocation Data (Bed Status for Various Categories)
bed_status = []
for i in range(1, 21):  # 20 beds for each category
    bed_status.append([f"Bed-{i}", 'Occupied' if random.random() > 0.5 else 'Available', random.choice(bed_categories)])

bed_status_df = pd.DataFrame(bed_status, columns=["Bed ID", "Status", "Category"])

# --- Streamlit Dashboard ---
st.title("Hospital Management Dashboard (Tailored for Indian Hospitals)")

# Patient Queue Management
st.subheader("Patient Queue Management")
patients_status_chart = px.bar(patients_df['Condition'].value_counts(), title="Patient Conditions Breakdown")
st.plotly_chart(patients_status_chart)

# Filter Patient Data by Bed Category
bed_filter = st.selectbox("Filter Patients by Bed Category", ['All'] + bed_categories)
if bed_filter != 'All':
    patients_df = patients_df[patients_df['Bed Required'] == bed_filter]
st.dataframe(patients_df)

# Medicine Inventory System
st.subheader("Medicine Inventory")
med_inventory_chart = px.pie(med_inventory_df, names='Status', title="Medicine Stock Status Distribution")
st.plotly_chart(med_inventory_chart)

# Filter Medicines by Low Stock
low_stock_filter = st.selectbox("Filter by Stock Status", ['All', 'Low Stock', 'Sufficient'])
if low_stock_filter != 'All':
    med_inventory_df = med_inventory_df[med_inventory_df['Status'] == low_stock_filter]
st.dataframe(med_inventory_df)

# Medical Equipment Inventory
st.subheader("Medical Equipment Inventory")
equip_status_chart = px.pie(equipment_df, names='Status', title="Equipment Status (Functional vs Under Repair)")
st.plotly_chart(equip_status_chart)

# Filter Equipment by Status
equip_status_filter = st.selectbox("Filter Equipment by Status", ['All', 'Functional', 'Under Repair'])
if equip_status_filter != 'All':
    equipment_df = equipment_df[equipment_df['Status'] == equip_status_filter]
st.dataframe(equipment_df)

# Bed Allocation
st.subheader("Bed Allocation Overview")
bed_status_chart = px.bar(bed_status_df.groupby("Category")['Status'].value_counts().unstack(), barmode='stack', title="Bed Occupancy Status by Category")
st.plotly_chart(bed_status_chart)

# Filter Beds by Category
bed_category_filter = st.selectbox("Filter Beds by Category", ['All'] + bed_categories)
if bed_category_filter != 'All':
    bed_status_df = bed_status_df[bed_status_df['Category'] == bed_category_filter]
st.dataframe(bed_status_df)

# Footer
st.write("Hospital Management System Dashboard tailored for Indian hospitals with dynamic data visualization and real-time updates.")

