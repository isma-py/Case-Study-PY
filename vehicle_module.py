"""
Module Name: vehicle_module.py
Course: DFK50083 - Python Programming Case Study
Description: Defines Vehicle & PremiumVehicle classes, Magic Methods,
             Operator Overloading, and Core Utility Functions.
"""

class Vehicle:
    def __init__(self, owner_name, plate_number, vehicle_type, base_charge=50.0):
        """
        Magic Method: __init__
        Initializes base Vehicle attributes.
        """
        self.owner_name = owner_name
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.base_charge = base_charge

    def calculate_total_charge(self, service_cost=0.0, discount=0.0):
        """
        Demonstrates Function Overloading concept using default parameters.
        Calculates total charge considering base charge, selected services, and potential discount.
        """
        total = self.base_charge + service_cost - discount
        return max(0.0, total)

    def display_info(self):
        """Returns structured vehicle information string."""
        return f"Owner: {self.owner_name} | Plate: {self.plate_number} | Type: {self.vehicle_type}"

    def __str__(self):
        """Magic Method: __str__ for human-readable object representation."""
        return f"Vehicle({self.owner_name}, {self.plate_number}, {self.vehicle_type})"

    def __add__(self, other):
        """
        Magic Method & Operator Overloading: __add__ (+)
        Adds base charges of two Vehicle instances.
        """
        if isinstance(other, Vehicle):
            return self.base_charge + other.base_charge
        elif isinstance(other, (int, float)):
            return self.base_charge + other
        return NotImplemented


# --- THREE (3) REQUIRED STANDALONE FUNCTIONS ---

def register_customer_and_vehicle(name, plate, v_type, is_premium=False):
    """Function 1: Creates and returns a Vehicle or PremiumVehicle object."""
    if is_premium:
        return PremiumVehicle(owner_name=name, plate_number=plate, vehicle_type=v_type)
    return Vehicle(owner_name=name, plate_number=plate, vehicle_type=v_type)


def calculate_service_charge(vehicle_obj, selected_services, service_catalog, discount=0.0):
    """Function 2: Computes subtotal, base charges, and final total."""
    subtotal = sum(service_catalog[s] for s in selected_services if s in service_catalog)
    total_charge = vehicle_obj.calculate_total_charge(service_cost=subtotal, discount=discount)
    return subtotal, total_charge


def display_customer_and_vehicle_info(vehicle_obj, selected_services, service_catalog, total_charge):
    """Function 3: Formats comprehensive summary dictionary for UI display."""
    service_breakdown = {s: service_catalog[s] for s in selected_services if s in service_catalog}
    return {
        "Owner Name": vehicle_obj.owner_name,
        "Plate Number": vehicle_obj.plate_number,
        "Vehicle Type": vehicle_obj.vehicle_type,
        "Is Premium": isinstance(vehicle_obj, PremiumVehicle),
        "Details": vehicle_obj.display_info(),
        "Selected Services": service_breakdown,
        "Total Final Charge": total_charge
    }


class PremiumVehicle(Vehicle):
    """Subclass inheriting from Vehicle to demonstrate Inheritance."""
    
    def __init__(self, owner_name, plate_number, vehicle_type, concierge_fee=30.0, base_charge=80.0):
        super().__init__(owner_name, plate_number, vehicle_type, base_charge)
        self.concierge_fee = concierge_fee

    def calculate_total_charge(self, service_cost=0.0, discount=0.0):
        """Overridden method including premium concierge service fee."""
        base_total = super().calculate_total_charge(service_cost, discount)
        return base_total + self.concierge_fee

    def display_info(self):
        """Extends parent display_info method."""
        parent_info = super().display_info()
        return f"{parent_info} | Premium Concierge Fee: RM{self.concierge_fee:.2f}"