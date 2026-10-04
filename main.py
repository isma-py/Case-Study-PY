# main.py
"""
DFK50083 Python Programming - Case Study Main GUI
Main GUI Application using Streamlit, OpenCV/Matplotlib visualization, and Exception Handling.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# [RUBRIC SECTION: (d) Modules Implementation]
# Importing custom functions, classes, and helper routines from vehicle_module.py
# ==============================================================================
try:
    from vehicle_module import (
        Vehicle,
        PremiumVehicle,
        register_customer_and_vehicle,
        calculate_service_charge,
        display_customer_and_vehicle_info,
        perform_matrix_data_analysis,
    )
except ImportError as err:
    st.error(f"Critical System Error: Custom module 'vehicle_module.py' not found. Details: {err}")
    st.stop()


# ==============================================================================
# [RUBRIC SECTION: (e) GUI Design using Streamlit]
# Streamlit Page Config & Custom Styling
# ==============================================================================
st.set_page_config(
    page_title="AutoCare Service Centre Management System",
    page_icon="🚗",
    layout="wide",
)

st.title("🚗 AutoCare Service Centre Management & Analysis System")
st.write("DFK50083 Python Programming Case Study Solution")
st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📋 Service Registration & Billing",
    "🧪 OOP & Operator Overloading Demo",
    "📊 Matrix Processing & Data Analysis",
])

# Available Services catalog with pricing
SERVICE_CATALOG = {
    "Standard Engine Oil Change": 150.00,
    "Fully Synthetic Oil Change": 250.00,
    "Brake Pad Replacement & Service": 220.00,
    "Battery Replacement": 180.00,
    "Engine Diagnostics & Tuning": 300.00,
    "Wheel Alignment & Balancing": 90.00,
    "Aircond Filter & Gas Refill": 120.00,
}


# ==============================================================================
# TAB 1: SERVICE REGISTRATION & BILLING (GUI & Exception Handling)
# ==============================================================================
with tab1:
    st.header("Customer & Vehicle Registration")

    # [RUBRIC SECTION: (e) Streamlit Input Fields]
    col_cust, col_veh = st.columns(2)

    with col_cust:
        st.subheader("Customer Details")
        cust_name_input = st.text_input("Customer Full Name:", placeholder="e.g. Ahmad Albab")
        cust_phone_input = st.text_input("Contact Phone Number:", placeholder="e.g. 012-3456789")

    with col_veh:
        st.subheader("Vehicle Details")
        veh_plate_input = st.text_input("Vehicle Plate Number:", placeholder="e.g. PBP 1234")
        veh_brand_input = st.selectbox("Vehicle Brand:", ["Proton", "Perodua", "Toyota", "Honda", "BMW", "Mercedes", "Other"])
        veh_model_input = st.text_input("Vehicle Model:", placeholder="e.g. Civic / Myvi / X70")
        is_premium_check = st.checkbox("Register as Premium Vehicle Package (Includes Priority Lane & Surcharge)")

    st.markdown("---")
    st.subheader("Select Required Vehicle Services")

    # Dynamic Selection & Automatic Individual Charge Display
    selected_services_dict = {}
    col_serv1, col_serv2 = st.columns(2)

    # [RUBRIC SECTION: (e) Automatic Service Charge Display]
    for idx, (s_name, s_price) in enumerate(SERVICE_CATALOG.items()):
        target_col = col_serv1 if idx % 2 == 0 else col_serv2
        with target_col:
            if st.checkbox(f"{s_name} (RM {s_price:.2f})", key=f"chk_{idx}"):
                selected_services_dict[s_name] = s_price

    # Real-time subtotal calculation display
    current_subtotal = sum(selected_services_dict.values())
    st.info(f"**Current Selected Services Subtotal:** RM {current_subtotal:.2f}")

    discount_input = st.number_input("Member Discount Percentage (%):", min_value=0.0, max_value=50.0, value=0.0, step=5.0)

    st.markdown("---")

    # Process Button
    if st.button("Generate Billing Receipt & Process Registration"):
        # ==============================================================================
        # [RUBRIC SECTION: (e) Exception Handling with try-except]
        # Handles empty strings, range errors, missing selections
        # ==============================================================================
        try:
            # 1. Call Function 1: Register Customer & Vehicle
            customer_data = register_customer_and_vehicle(
                cust_name=cust_name_input,
                phone=cust_phone_input,
                plate=veh_plate_input,
                brand=veh_brand_input,
                model=veh_model_input,
                is_premium=is_premium_check,
            )

            # 2. Call Function 2: Calculate Service Charge
            vehicle_obj = customer_data["Vehicle Object"]
            services_subtotal, total_bill = calculate_service_charge(
                vehicle_obj=vehicle_obj,
                selected_services=selected_services_dict,
                discount_percent=discount_input,
            )

            # 3. Call Function 3: Display Customer and Vehicle Information
            receipt_text = display_customer_and_vehicle_info(
                customer_info=customer_data,
                selected_services=selected_services_dict,
                total_bill=total_bill,
            )

            st.success("Vehicle Registration and Billing Processed Successfully!")

            # Output Presentation
            st.code(receipt_text, language="text")

            # Metrics Summary Display
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Selected Services Cost", f"RM {services_subtotal:.2f}")
            m_col2.metric("Base / Surcharge Fee", f"RM {(total_bill - services_subtotal):.2f}")
            m_col3.metric("Final Total Charge", f"RM {total_bill:.2f}")

        except ValueError as val_err:
            st.error(f"Input Validation Error: {val_err}")
        except Exception as general_err:
            st.error(f"System Error: An unexpected error occurred: {general_err}")


# ==============================================================================
# TAB 2: OOP & OPERATOR OVERLOADING DEMO
# ==============================================================================
with tab2:
    st.header("Object-Oriented Programming (OOP) Demonstration")
    st.write("Demonstrating Class vs Subclass, Function Overloading, Magic Methods, and Operator Overloading.")

    col_demo1, col_demo2 = st.columns(2)

    with col_demo1:
        st.subheader("1. Standard Vehicle Instance")
        v_std = Vehicle(plate_number="PBB1122", brand="Proton", model="Saga", base_service_fee=50.0)
        st.write(f"**Class Type:** `{type(v_std).__name__}`")
        st.write(f"**`get_info()` Method Output:** {v_std.get_info()}")
        st.write(f"**`__str__()` Magic Method:** `{str(v_std)}`")
        
        # Function Overloading Demo
        bill_no_disc = v_std.calculate_total_bill(selected_services_cost=200.0)
        bill_with_disc = v_std.calculate_total_bill(selected_services_cost=200.0, discount=10.0)
        st.write(f"**Overloading Test (No Discount Default):** RM {bill_no_disc:.2f}")
        st.write(f"**Overloading Test (10% Discount Param):** RM {bill_with_disc:.2f}")

    with col_demo2:
        st.subheader("2. Premium Vehicle Subclass Instance")
        v_prem = PremiumVehicle(plate_number="PMM9999", brand="BMW", model="330i", base_service_fee=100.0, premium_surcharge=50.0)
        st.write(f"**Class Type:** `{type(v_prem).__name__}`")
        st.write(f"**`get_info()` Method Output:** {v_prem.get_info()}")
        st.write(f"**`__str__()` Magic Method:** `{str(v_prem)}`")
        
        bill_prem = v_prem.calculate_total_bill(selected_services_cost=200.0)
        st.write(f"**Overridden Calculation (with RM50 Surcharge):** RM {bill_prem:.2f}")

    st.markdown("---")
    st.subheader("3. Operator Overloading (`__add__`) Demonstration")
    st.write("Overloading the `+` operator to combine base fees between two vehicle objects.")

    combined_base_fee = v_std + v_prem  # Calls v_std.__add__(v_prem)
    st.code(
        f"""
        # Python Code Execution:
        v_std = Vehicle("PBB1122", "Proton", "Saga", base_service_fee=50.0)
        v_prem = PremiumVehicle("PMM9999", "BMW", "330i", base_service_fee=100.0)

        total_combined_base = v_std + v_prem
        # Result = RM {combined_base_fee:.2f}
        """,
        language="python",
    )
    st.success(f"Combined Base Inspection Fee (`v_std + v_prem`): **RM {combined_base_fee:.2f}**")


# ==============================================================================
# TAB 3: MATRIX PROCESSING & DATA ANALYSIS (NumPy, Pandas, Matplotlib)
# ==============================================================================
with tab3:
    st.header("Matrix Processing and Data Analysis")
    st.write("Automated analysis using NumPy array processing, Pandas DataFrame operations, and Matplotlib graph generation.")

    # Execute Analysis from module
    analysis = perform_matrix_data_analysis()

    col_mat1, col_mat2 = st.columns(2)

    with col_mat1:
        st.subheader("1. NumPy Array & Attributes")
        st.write("2D NumPy Array representing service charges across 5 vehicles:")
        st.write(analysis["matrix"])
        
        st.write("**NumPy Array Attributes:**")
        st.json(analysis["attributes"])

    with col_mat2:
        st.subheader("2. Indexing, Slicing & Mathematical Analysis")
        st.write("**Array Slicing (`[0:3, 1:3]` - Vehicles 1-3, Services 2-3):**")
        st.write(analysis["sliced"])
        
        st.write("**Mathematical Analysis Results:**")
        st.write(f"- Total Revenue per Service Column: `{analysis['total_per_service']}`")
        st.write(f"- Average Charge per Vehicle: `{analysis['avg_per_vehicle']}`")
        st.write(f"- Maximum Single Service Charge: **RM {analysis['max_charge']:.2f}**")

    st.markdown("---")
    st.subheader("3. Pandas DataFrame Slicing, Filtering & Sorting")

    df_col1, df_col2 = st.columns(2)
    with df_col1:
        st.write("**Full Vehicle Service DataFrame:**")
        st.dataframe(analysis["df"], use_container_width=True)

    with df_col2:
        st.write("**Filtered DataFrame (Premium Vehicles Only):**")
        st.dataframe(analysis["filtered_df"], use_container_width=True)
        
        st.write("**Sorted DataFrame (By Total Charge Descending):**")
        st.dataframe(analysis["sorted_df"], use_container_width=True)

    st.markdown("---")
    # ==============================================================================
    # [RUBRIC SECTION: (f) Matplotlib Graph Display]
    # ==============================================================================
    st.subheader("4. Data Visualization using Matplotlib")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    df = analysis["df"]
    
    services = ["Engine Oil", "Brake Service", "Battery Replacement", "Engine Tuning"]
    total_revenues = [df[s].sum() for s in services]
    
    colors = ["#4F46E5", "#06B6D4", "#10B981", "#F59E0B"]
    bars = ax.bar(services, total_revenues, color=colors, width=0.5)

    ax.set_title("AutoCare Service Centre - Total Revenue per Service Category (RM)", fontsize=12, fontweight="bold")
    ax.set_ylabel("Revenue (RM)", fontsize=10)
    ax.set_ylim(0, max(total_revenues) * 1.2)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Value Labels on top of bars
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 20, f"RM {yval:.2f}", ha="center", va="bottom", fontweight="bold")

    st.pyplot(fig)