"""
Module Name: main.py
Course: DFK50083 - Python Programming Case Study
Description: Streamlit GUI application featuring Customer Management,
             Exception Handling, NumPy/Pandas Analysis, and Matplotlib Visualizations.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import custom module (Requirement d)
import vehicle_module as vm

# Page Configuration
st.set_page_config(
    page_title="AutoCare Service Centre Management",
    layout="wide"
)

# Service Catalog Definition
SERVICE_CATALOG = {
    "Engine Oil Change": 120.0,
    "Oil Filter Replacement": 35.0,
    "Brake Pad Replacement": 180.0,
    "Wheel Alignment & Balancing": 90.0,
    "Aircond Servicing": 150.0,
    "Spark Plug Replacement": 85.0,
    "Full Vehicle Diagnostic Inspection": 100.0
}

st.title("AutoCare Service Centre Management & Analysis System")
st.caption("DFK50083: Python Programming Case Study - Sesi II 2025/2026")

tab1, tab2, tab3 = st.tabs([
    "Service Registration & Billing", 
    "Matrix & Data Analytics", 
    "OOP & Magic Method Demo"
])

# ==============================================================================
# TAB 1: GUI, Service Selection & Exception Handling
# ==============================================================================
with tab1:
    st.header("Customer & Vehicle Registration")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            owner_name = st.text_input("Customer Name", placeholder="e.g. Ahmad Razak")
            plate_number = st.text_input("Vehicle Plate Number", placeholder="e.g. WYY 8888")
            vehicle_type = st.selectbox("Vehicle Type", ["Sedan", "SUV", "Hatchback", "MPV", "4x4 Truck"])
        
        with col2:
            is_premium = st.checkbox("Apply Premium Membership (Includes Concierge Service)")
            discount_input = st.number_input("Discount Voucher (RM)", min_value=0.0, max_value=200.0, value=0.0, step=5.0)
            
            selected_services = st.multiselect(
                "Select Required Services",
                options=list(SERVICE_CATALOG.keys()),
                help="Individual service costs will be calculated dynamically."
            )
        
        # Live individual charges breakdown
        if selected_services:
            st.markdown("##### Selected Individual Service Charges:")
            charge_data = [{"Service": s, "Charge (RM)": f"RM {SERVICE_CATALOG[s]:.2f}"} for s in selected_services]
            st.dataframe(pd.DataFrame(charge_data), use_container_width=True)
            
        submit_btn = st.form_submit_button("Submit & Generate Invoice", type="primary")

    if submit_btn:
        # EXCEPTION HANDLING IMPLEMENTATION
        try:
            # 1. Validation for empty inputs
            if not owner_name.strip():
                raise ValueError("Customer Name cannot be empty.")
            if not plate_number.strip():
                raise ValueError("Vehicle Plate Number cannot be empty.")
            
            # 2. Validation for service selection range
            if not selected_services:
                raise ValueError("Please select at least ONE service from the checklist.")
                
            # 3. Validation for negative or extreme range errors
            if discount_input < 0 or discount_input > 200:
                raise ValueError("Discount must be between RM 0 and RM 200.")

            # Processing via module functions
            vehicle_obj = vm.register_customer_and_vehicle(
                name=owner_name.strip(),
                plate=plate_number.strip().upper(),
                v_type=vehicle_type,
                is_premium=is_premium
            )
            
            subtotal, final_total = vm.calculate_service_charge(
                vehicle_obj=vehicle_obj,
                selected_services=selected_services,
                service_catalog=SERVICE_CATALOG,
                discount=discount_input
            )
            
            summary = vm.display_customer_and_vehicle_info(
                vehicle_obj=vehicle_obj,
                selected_services=selected_services,
                service_catalog=SERVICE_CATALOG,
                total_charge=final_total
            )

            # Display Successful Invoice Output
            st.success("Service Registration & Invoice Generated Successfully.")
            st.subheader("Invoice Summary")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.write(f"**Customer Name:** {summary['Owner Name']}")
                st.write(f"**Plate Number:** {summary['Plate Number']}")
                st.write(f"**Vehicle Type:** {summary['Vehicle Type']}")
                st.write(f"**Membership Class:** {'Premium Class' if summary['Is Premium'] else 'Standard Class'}")
                st.caption(summary['Details'])
                
            with res_col2:
                st.write(f"**Services Cost Subtotal:** RM {subtotal:.2f}")
                st.write(f"**Base Entry Charge:** RM {vehicle_obj.base_charge:.2f}")
                if is_premium:
                    st.write(f"**Concierge Service Fee:** RM {vehicle_obj.concierge_fee:.2f}")
                st.write(f"**Discount Applied:** -RM {discount_input:.2f}")
                st.markdown(f"### **Total Final Charge: RM {final_total:.2f}**")

        except ValueError as ve:
            st.error(f"Input Error Validation: {ve}")
        except Exception as e:
            st.error(f"Unexpected Error Occurred: {e}")

# ==============================================================================
# TAB 2: Matrix Processing & Data Analysis (NumPy, Pandas, Matplotlib)
# ==============================================================================
with tab2:
    st.header("Service Center Analytics & Matrix Operations")
    
    # Generate Synthetic Dataset for Analysis
    data = {
        "Service_ID": [f"SRV-{1001+i}" for i in range(10)],
        "Service_Name": [
            "Engine Oil Change", "Oil Filter Replacement", "Brake Pad Replacement", 
            "Wheel Alignment", "Aircond Servicing", "Spark Plug Replacement", 
            "Diagnostic Inspection", "Battery Replacement", "Gearbox Fluid", "Coolant Flush"
        ],
        "Category": ["Maintenance", "Maintenance", "Brakes", "Tyres", "AC", "Engine", "Diagnostic", "Electrical", "Transmission", "Cooling"],
        "Base_Price_RM": [120, 35, 180, 90, 150, 85, 100, 250, 210, 110],
        "Labor_Hours": [1.0, 0.5, 1.5, 1.0, 2.0, 1.2, 1.0, 0.5, 1.8, 1.0],
        "Jobs_Completed": [45, 60, 30, 25, 20, 18, 40, 15, 12, 22]
    }
    
    df = pd.DataFrame(data)
    
    st.subheader("1. Pandas DataFrame Overview")
    st.dataframe(df, use_container_width=True)
    
    # DataFrame & NumPy Array Attributes
    price_array = np.array(df["Base_Price_RM"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("##### **Pandas DataFrame Attributes:**")
        st.write(f"- **Shape (Rows, Cols):** `{df.shape}`")
        st.write(f"- **Data Types:** \n{df.dtypes.to_dict()}")
        st.write(f"- **Size (Total Elements):** `{df.size}`")
        
    with col_b:
        st.markdown("##### **NumPy Array Attributes (`Base_Price_RM`):**")
        st.write(f"- **Array Shape:** `{price_array.shape}`")
        st.write(f"- **Array Dimensions (ndim):** `{price_array.ndim}`")
        st.write(f"- **Array Data Type (dtype):** `{price_array.dtype}`")
        st.write(f"- **Total Element Count:** `{price_array.size}`")
        
    st.divider()
    
    # Indexing & Slicing
    st.subheader("2. Indexing & Slicing Operations")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("**Slicing DataFrame (First 5 Rows, Selected Columns):**")
        st.dataframe(df.iloc[0:5, [0, 1, 3, 5]])
    with col_s2:
        st.markdown("**NumPy Array Slicing (Elements 2 to 7):**")
        st.code(f"Original Array: {price_array}\nSliced Array [2:7]: {price_array[2:7]}")
        
    st.divider()
    
    # Mathematical Analysis using NumPy
    st.subheader("3. Mathematical Analysis on Service Charges")
    
    # Vectorized Math Calculations
    total_revenue_per_service = price_array * np.array(df["Jobs_Completed"])
    df["Total_Revenue_RM"] = total_revenue_per_service
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Mean Price", f"RM {np.mean(price_array):.2f}")
    m_col2.metric("Max Price", f"RM {np.max(price_array):.2f}")
    m_col3.metric("Min Price", f"RM {np.min(price_array):.2f}")
    m_col4.metric("Total Revenue Generated", f"RM {np.sum(total_revenue_per_service):,.2f}")
    
    st.divider()
    
    # Filtering & Sorting
    st.subheader("4. Data Filtering & Sorting")
    filter_price = st.slider("Filter Services with Price > RM", min_value=30, max_value=250, value=100)
    filtered_df = df[df["Base_Price_RM"] > filter_price].sort_values(by="Base_Price_RM", ascending=False)
    st.dataframe(filtered_df, use_container_width=True)
    
    st.divider()
    
    # Matplotlib Graph Visualization
    st.subheader("5. Graphical Visualization (Matplotlib)")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(df["Service_Name"], df["Total_Revenue_RM"], color="#2b5c8f", edgecolor="#1a3754")
    
    ax.set_title("Total Revenue Generated by Service Type", fontsize=14, fontweight="bold")
    ax.set_xlabel("Service Name", fontsize=12)
    ax.set_ylabel("Revenue (RM)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Annotate bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'RM{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)
                    
    plt.tight_layout()
    st.pyplot(fig)

# ==============================================================================
# TAB 3: OOP, Magic Method & Operator Overloading Demonstration
# ==============================================================================
with tab3:
    st.header("Object-Oriented Programming (OOP) Demonstration")
    
    st.subheader("1. Class Instantiation & Output Display")
    v_std = vm.Vehicle("Ahmad", "VAA 1234", "Sedan", base_charge=50.0)
    v_prm = vm.PremiumVehicle("Siti", "WYY 8888", "SUV", concierge_fee=30.0, base_charge=80.0)
    
    st.write("**Standard Vehicle Info (`Vehicle` Base Class):**")
    st.info(v_std.display_info())
    
    st.write("**Premium Vehicle Info (`PremiumVehicle` Subclass):**")
    st.info(v_prm.display_info())
    
    st.divider()
    
    st.subheader("2. Magic Method (`__str__`) Implementation")
    st.code(f"str(v_std) output: {str(v_std)}\nstr(v_prm) output: {str(v_prm)}")
    
    st.divider()
    
    st.subheader("3. Operator Overloading (`__add__`) Demonstration")
    st.write("Adding the base charges of Standard Vehicle (RM 50.0) and Premium Vehicle (RM 80.0):")
    combined_charge = v_std + v_prm
    st.success(f"Result of `v_std + v_prm`: RM {combined_charge:.2f}")