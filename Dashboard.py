import streamlit as st
import pandas as pd
import datetime as dt

# Dummy data

# Patient Queue Management System
patients = [
    {"id": 1, "name": "Alice", "age": 30, "condition": "Critical", "bed_requirement": "ICU"},
    {"id": 2, "name": "Bob", "age": 45, "condition": "Emergency", "bed_requirement": "Emergency"},
    {"id": 3, "name": "Charlie", "age": 20, "condition": "Stable", "bed_requirement": "General"},
]

# Bed Allocation System
beds = {
    "ICU": {"total": 10, "occupied": 7},
    "Emergency": {"total": 5, "occupied": 3},
    "General": {"total": 20, "occupied": 12},
}

# Medicine Inventory System
medicines = [
    {"name": "Paracetamol", "quantity": 50, "expiry_date": "2025-12-01", "low_stock_threshold": 20},
    {"name": "Aspirin", "quantity": 15, "expiry_date": "2024-05-10", "low_stock_threshold": 10},
    {"name": "Insulin", "quantity": 5, "expiry_date": "2025-03-01", "low_stock_threshold": 10},
]

# Streamlit Dashboard Setup
st.set_page_config(page_title="Hospital Management Dashboard", layout="wide")

# Dashboard Title
st.title("🏥 Hospital Management Dashboard")

# Section 1: Patient Queue Management
st.subheader("Patient Queue Management")
st.write("The following table shows the current patient queue in the hospital:")
patient_df = pd.DataFrame(patients)
st.table(patient_df)

# Section 2: Bed Allocation System
st.subheader("Bed Allocation System")
st.write("Real-time status of hospital bed availability:")

col1, col2, col3 = st.columns(3)

for category, bed_info in beds.items():
    with col1 if category == "ICU" else col2 if category == "Emergency" else col3:
        st.metric(
            label=category,
            value=f"{bed_info['occupied']}/{bed_info['total']} occupied",
            delta=bed_info['total'] - bed_info['occupied'],
        )

# Section 3: Medicine Inventory System
st.subheader("Medicine Inventory System")
st.write("Below is the current inventory of medicines in the hospital:")
medicine_df = pd.DataFrame(medicines)
medicine_df["status"] = medicine_df.apply(
    lambda x: "Low Stock" if x["quantity"] <= x["low_stock_threshold"] else "Sufficient", axis=1
)
st.table(medicine_df)

# Alerts for Low Stock Medicines
st.subheader("Alerts")
low_stock_meds = medicine_df[medicine_df["status"] == "Low Stock"]
if not low_stock_meds.empty:
    st.warning("Low Stock Alert for Medicines:")
    st.table(low_stock_meds)
else:
    st.success("All medicines are sufficiently stocked!")

# Section 4: Add New Medicine
st.subheader("Manage Inventory")
st.write("Use the form below to add new medicines to the inventory:")

with st.form("add_medicine"):
    med_name = st.text_input("Medicine Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    expiry_date = st.date_input("Expiry Date", min_value=dt.date.today())
    low_stock_threshold = st.number_input("Low Stock Threshold", min_value=0, step=1)
    submitted = st.form_submit_button("Add Medicine")
    if submitted:
        new_medicine = {
            "name": med_name,
            "quantity": quantity,
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "low_stock_threshold": low_stock_threshold,
        }
        medicines.append(new_medicine)
        st.success(f"Added new medicine: {med_name}")

# Footer
st.write("---")
st.caption("Developed for a hospital management system prototype.")

