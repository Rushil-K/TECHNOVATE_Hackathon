import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

# Load and preprocess the data
@st.cache_data
def load_data():
    df = pd.read_csv('merge-csv.com__67939d8414c50.csv', skiprows=2)
    
    # Clean patient data
    patient_columns = ['Name', 'Age', 'Status', 'Category', 'Date']
    patient_data = df[df.columns[:len(patient_columns)]]
    patient_data.columns = patient_columns
    patient_data['Date'] = pd.to_datetime(patient_data['Date'])
    
    # Clean bed data
    bed_data = df[df['Bed ID'].str.contains('Bed-', na=False)]
    
    # Clean medical equipment data
    equipment_data = df[(df['Bed ID'] == 'Ventilator') | 
                        (df['Bed ID'] == 'ECG Machine') | 
                        (df['Bed ID'] == 'Defibrillator') | 
                        (df['Bed ID'] == 'Syringe Pump') | 
                        (df['Bed ID'] == 'Infusion Pump') | 
                        (df['Bed ID'] == 'X-Ray Machine')]
    
    # Clean medication data
    medication_columns = df.columns[0:3]
    medication_data = df[medication_columns]
    medication_data.columns = ['Medication', 'Quantity', 'Expiry Date']
    medication_data['Expiry Date'] = pd.to_datetime(medication_data['Expiry Date'])
    
    return patient_data, bed_data, equipment_data, medication_data

# Main dashboard function
def hospital_dashboard():
    # Set page configuration
    st.set_page_config(page_title="Hospital Management Dashboard", 
                       page_icon=":hospital:", 
                       layout="wide")
    
    # Load data
    patient_data, bed_data, equipment_data, medication_data = load_data()
    
    # Dashboard Title
    st.title("🏥 Comprehensive Hospital Management Dashboard")
    
    # Sidebar for filters
    st.sidebar.header("Dashboard Filters")
    
    # Patient Status Filter
    status_filter = st.sidebar.multiselect(
        "Select Patient Status:",
        options=patient_data['Status'].unique(),
        default=patient_data['Status'].unique()
    )
    
    # Category Filter
    category_filter = st.sidebar.multiselect(
        "Select Patient Category:",
        options=patient_data['Category'].unique(),
        default=patient_data['Category'].unique()
    )
    
    # Date Range Filter
    date_range = st.sidebar.date_input(
        "Select Date Range:",
        [patient_data['Date'].min(), patient_data['Date'].max()]
    )
    
    # Apply Filters
    filtered_patient_data = patient_data[
        (patient_data['Status'].isin(status_filter)) &
        (patient_data['Category'].isin(category_filter)) &
        (patient_data['Date'].dt.date >= date_range[0]) &
        (patient_data['Date'].dt.date <= date_range[1])
    ]
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Patients", 
            value=len(filtered_patient_data),
            delta=f"{len(filtered_patient_data) - len(patient_data)}",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="Critical Patients", 
            value=len(filtered_patient_data[filtered_patient_data['Status'] == 'Critical']),
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Available Beds", 
            value=len(bed_data[bed_data['Status'] == 'Available']),
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            label="Functional Equipment", 
            value=len(equipment_data[equipment_data['Category'] == 'Functional']),
            delta_color="normal"
        )
    
    # Visualization Row
    col1, col2 = st.columns(2)
    
    with col1:
        # Patient Status Distribution
        st.subheader("Patient Status Distribution")
        status_counts = filtered_patient_data['Status'].value_counts()
        fig_status = px.pie(
            names=status_counts.index, 
            values=status_counts.values, 
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Patient Category Distribution
        st.subheader("Patient Category Distribution")
        category_counts = filtered_patient_data['Category'].value_counts()
        fig_category = px.bar(
            x=category_counts.index, 
            y=category_counts.values,
            labels={'x': 'Category', 'y': 'Number of Patients'},
            color=category_counts.index,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Detailed Tables
    st.header("Detailed Hospital Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bed Occupancy
        st.subheader("Bed Occupancy")
        bed_occupancy = bed_data['Category'].value_counts()
        st.dataframe(bed_occupancy)
    
    with col2:
        # Equipment Status
        st.subheader("Medical Equipment Status")
        equipment_status = equipment_data.groupby(['Bed ID', 'Category']).size().reset_index(name='Count')
        st.dataframe(equipment_status)
    
    # Medication Inventory
    st.subheader("Medication Inventory")
    st.dataframe(medication_data)

# Run the dashboard
if __name__ == "__main__":
    hospital_dashboard()
