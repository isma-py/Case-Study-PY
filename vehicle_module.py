# vehicle_module.py
"""
DFK50083 Python Programming - Case Study Module
Module Name: vehicle_module.py
Contains OOP Classes, Magic Methods, Overloading, and Modular Functions.
"""

import numpy as np
import pandas as pd


# ==============================================================================
# [RUBRIC SECTION: (b) Parent Class & (c) Magic Methods]
# - Class Vehicle with attributes and methods
# - Magic Methods: __init__(), __str__(), __add__()
# ==============================================================================

class Vehicle:
    """
    [RUBRIC SECTION: (b) Parent Class]
    Attributes: plate_number, brand, model, base_service_fee
    """

    def __init__(self, plate_number: str, brand: str, model: str, base_service_fee: float = 50.0):
        # [RUBRIC SECTION: (c) Magic Method - __init__()]
        self.plate_number = plate_number.upper().strip()
        self.brand = brand.strip()
        self.model = model.strip()
        self.base_service_fee = float(base_service_fee)

    def calculate_total_bill(self, selected_services_cost: float, discount: float = 0.0) -> float:
        """
        [RUBRIC SECTION: (b) Function Overloading using Default Parameters]
        Calculates total cost with base fee, selected services, and optional discount parameter.
        """
        subtotal = self.base_service_fee + selected_services_cost
        total = subtotal - (subtotal * (discount / 100.0))
        return round(total, 2)

    def get_info(self) -> str:
        """Standard vehicle details string."""
        return f"Vehicle Plate: {self.plate_number} | {self.brand} {self.model} (Standard Vehicle)"

    def __str__(self) -> str:
        # [RUBRIC SECTION: (c) Magic Method - __str__()]
        return f"[Vehicle Object] Plate: {self.plate_number}, Brand: {self.brand}, Model: {self.model}, Base Fee: RM {self.base_service_fee:.2f}"

    def __add__(self, other):
        # [RUBRIC SECTION: (b) & (c) Operator Overloading - __add__()]
        # Overloading '+' operator to add base service fees of two vehicle objects
        if isinstance(other, Vehicle):
            return self.base_service_fee + other.base_service_fee
        elif isinstance(other, (int, float)):
            return self.base_service_fee + float(other)
        return NotImplemented


# ==============================================================================
# [RUBRIC SECTION: (b) Subclass & OOP Inheritance]
# Subclass PremiumVehicle inheriting from parent class Vehicle
# ==============================================================================

class PremiumVehicle(Vehicle):
    """
    [RUBRIC SECTION: (b) Inheritance Implementation]
    Subclass inheriting attributes and methods from Vehicle parent class.
    Adds premium_surcharge attribute and overrides methods.
    """

    def __init__(self, plate_number: str, brand: str, model: str, base_service_fee: float = 100.0, premium_surcharge: float = 30.0):
        # Call Parent constructor using super()
        super().__init__(plate_number, brand, model, base_service_fee)
        self.premium_surcharge = float(premium_surcharge)

    def calculate_total_bill(self, selected_services_cost: float, discount: float = 0.0) -> float:
        """
        [METHOD OVERRIDING]
        Overrides parent calculate_total_bill to add mandatory premium surcharge.
        """
        subtotal = self.base_service_fee + self.premium_surcharge + selected_services_cost
        total = subtotal - (subtotal * (discount / 100.0))
        return round(total, 2)

    def get_info(self) -> str:
        """[METHOD OVERRIDING] Customized info for Premium Vehicles."""
        return f"Vehicle Plate: {self.plate_number} | {self.brand} {self.model} (PREMIUM - Surcharge: RM {self.premium_surcharge:.2f})"

    def __str__(self) -> str:
        # [RUBRIC SECTION: (c) Magic Method - __str__() Overridden]
        return f"[PremiumVehicle Object] Plate: {self.plate_number}, Brand: {self.brand}, Surcharge: RM {self.premium_surcharge:.2f}"


# ==============================================================================
# [RUBRIC SECTION: (a) Function Implementation]
# Three distinct functions as required by rubric (a):
# 1. register_customer_and_vehicle
# 2. calculate_service_charge
# 3. display_customer_and_vehicle_info
# ==============================================================================

def register_customer_and_vehicle(cust_name: str, phone: str, plate: str, brand: str, model: str, is_premium: bool = False):
    """
    [FUNCTION 1 - Customer & Vehicle Registration]
    Validates input and instantiates either standard Vehicle or PremiumVehicle object.
    """
    if not cust_name.strip() or not phone.strip() or not plate.strip():
        raise ValueError("Customer name, contact phone, and vehicle plate number are required.")

    if is_premium:
        vehicle_obj = PremiumVehicle(plate_number=plate, brand=brand, model=model)
    else:
        vehicle_obj = Vehicle(plate_number=plate, brand=brand, model=model)

    customer_info = {
        "Customer Name": cust_name.strip().title(),
        "Phone": phone.strip(),
        "Vehicle Object": vehicle_obj,
    }
    return customer_info


def calculate_service_charge(vehicle_obj: Vehicle, selected_services: dict, discount_percent: float = 0.0) -> tuple:
    """
    [FUNCTION 2 - Calculate Service Charge]
    Calculates individual service costs and total bill using vehicle object method.
    """
    if not selected_services:
        raise ValueError("At least one vehicle service must be selected.")

    services_subtotal = sum(selected_services.values())
    total_bill = vehicle_obj.calculate_total_bill(services_subtotal, discount=discount_percent)

    return services_subtotal, total_bill


def display_customer_and_vehicle_info(customer_info: dict, selected_services: dict, total_bill: float) -> str:
    """
    [FUNCTION 3 - Display Customer & Vehicle Information]
    Formats all details into a clean summary output string.
    """
    v_obj = customer_info["Vehicle Object"]
    output = f"""
    ==================================================
              AUTOCARE SERVICE CENTRE RECEIPT         
    ==================================================
    Customer Name : {customer_info['Customer Name']}
    Phone Number  : {customer_info['Phone']}
    Vehicle Info  : {v_obj.get_info()}
    Object Details: {str(v_obj)}
    --------------------------------------------------
    SELECTED SERVICES & INDIVIDUAL CHARGES:
    """
    for s_name, s_price in selected_services.items():
        output += f"\n    - {s_name:<30} : RM {s_price:>7.2f}"

    output += f"""
    --------------------------------------------------
    Base Inspection Fee        : RM {v_obj.base_service_fee:>7.2f}
    """
    if isinstance(v_obj, PremiumVehicle):
        output += f"    Premium Service Surcharge  : RM {v_obj.premium_surcharge:>7.2f}\n"

    output += f"""    TOTAL SERVICE CHARGE       : RM {total_bill:>7.2f}
    ==================================================
    """
    return output


# ==============================================================================
# [RUBRIC SECTION: (f) Matrix Processing and Data Analysis Helpers]
# NumPy and Pandas analysis algorithms
# ==============================================================================

def perform_matrix_data_analysis():
    """
    [RUBRIC SECTION: (f) Matrix Processing using NumPy & Pandas]
    - Creates NumPy Array & Pandas DataFrame
    - Displays Array Attributes (shape, ndim, dtype, size)
    - Demonstrates Indexing and Slicing
    - Performs Mathematical Analysis
    - Performs Filtering and Sorting
    """
    # 1. Create Sample Service Charges Matrix (NumPy 2D Array: Rows = Vehicles, Cols = [Oil, Brakes, Battery, Tuning])
    service_matrix = np.array([
        [150.0, 220.0, 180.0, 300.0],
        [150.0, 0.0,   180.0, 250.0],
        [200.0, 350.0, 0.0,   450.0],
        [150.0, 220.0, 0.0,   250.0],
        [250.0, 400.0, 220.0, 500.0],
    ])

    # Array Attributes
    attrs = {
        "Shape": service_matrix.shape,
        "Dimensions (ndim)": service_matrix.ndim,
        "Data Type (dtype)": str(service_matrix.dtype),
        "Total Elements (size)": service_matrix.size,
    }

    # Indexing and Slicing Example
    sliced_sample = service_matrix[0:3, 1:3]  # First 3 vehicles, Brakes & Battery services

    # Mathematical Analysis using NumPy
    total_revenue_per_service = np.sum(service_matrix, axis=0)
    avg_charge_per_vehicle = np.mean(service_matrix, axis=1)
    max_charge = np.max(service_matrix)

    # 2. Pandas DataFrame Creation
    data = {
        "Plate Number": ["VAA1010", "WYY8899", "BCC3322", "PJJ5544", "PXX9900"],
        "Vehicle Type": ["Standard", "Standard", "Premium", "Standard", "Premium"],
        "Engine Oil": service_matrix[:, 0],
        "Brake Service": service_matrix[:, 1],
        "Battery Replacement": service_matrix[:, 2],
        "Engine Tuning": service_matrix[:, 3],
        "Total Charge (RM)": np.sum(service_matrix, axis=1),
    }

    df = pd.DataFrame(data)

    # Filtering & Sorting in Pandas
    premium_vehicles_df = df[df["Vehicle Type"] == "Premium"]  # Filtering
    sorted_df = df.sort_values(by="Total Charge (RM)", ascending=False)  # Sorting

    return {
        "matrix": service_matrix,
        "attributes": attrs,
        "sliced": sliced_sample,
        "total_per_service": total_revenue_per_service,
        "avg_per_vehicle": avg_charge_per_vehicle,
        "max_charge": max_charge,
        "df": df,
        "filtered_df": premium_vehicles_df,
        "sorted_df": sorted_df,
    }