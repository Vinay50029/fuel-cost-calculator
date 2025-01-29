def electric_vehicle_cost(distance, ev_efficiency, electricity_cost):
    """Calculate the energy consumption and cost for an electric vehicle."""
    energy_needed = distance / ev_efficiency  # kWh
    ev_cost = energy_needed * electricity_cost  # Total cost
    return energy_needed, ev_cost

def fuel_vehicle_cost(distance, fuel_efficiency, fuel_price):
    """Calculate the fuel consumption and cost for a fuel vehicle."""
    fuel_needed = distance / fuel_efficiency  # liters or kg
    fuel_cost = fuel_needed * fuel_price  # Total cost
    return fuel_needed, fuel_cost
    
def hybrid_vehicle_cost(distance, fuel_efficiency, fuel_price, ev_efficiency, electricity_cost, hybrid_split):
    """Calculate the fuel and energy consumption and cost for a hybrid vehicle."""
    fuel_distance = distance * (hybrid_split / 100)
    energy_distance = distance * ((100 - hybrid_split) / 100)

    fuel_needed = fuel_distance / fuel_efficiency  # liters or kg
    energy_needed = energy_distance / ev_efficiency  # kWh
    hybrid_cost = (fuel_needed * fuel_price) + (energy_needed * electricity_cost)  # Total cost

    return fuel_needed, energy_needed, hybrid_cost

def compare_costs():
    print("Welcome to the EV vs Fuel Vehicle Cost Calculator!\n")
    
    while True:
        try:
            distance = float(input("Enter the distance to be traveled (in kilometers): "))
            if distance <= 0:
                print("Distance must be a positive number. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numerical value for distance.")
    
    while True:
        vehicle_type = input("Is this an Electric Vehicle (EV), Fuel Vehicle (Petrol, Diesel, CNG), or Hybrid Vehicle? (Enter 'EV', 'Fuel', or 'Hybrid'): ").strip().lower()
        if vehicle_type in ['ev', 'fuel', 'hybrid']:
            break
        else:
            print("Invalid input. Please enter 'EV', 'Fuel', or 'Hybrid'.")
    
    if vehicle_type == 'ev':
        while True:
            try:
                ev_efficiency = float(input("How many kilometers does your EV travel per kWh (km per kWh)? "))
                if ev_efficiency <= 0:
                    print("Efficiency must be a positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for efficiency.")
        
        while True:
            try:
                electricity_cost = float(input("Enter the electricity cost per kWh (in your currency): "))
                if electricity_cost < 0:
                    print("Cost cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for electricity cost.")
        
        # Calculate energy consumption and cost
        energy_needed, ev_cost = electric_vehicle_cost(distance, ev_efficiency, electricity_cost)
        
        # Enhanced output
        print("\n==========================================")
        print("            Electric Vehicle Summary")
        print("==========================================")
        print(f"Distance Traveled:              {distance:.2f} km")
        print(f"Energy Consumed:                {energy_needed:.2f} kWh")
        print(f"Charging Cost:                   {ev_cost:.2f} currency units")
        print("==========================================")
    
    elif vehicle_type == 'fuel':
        while True:
            fuel_type = input("Enter the fuel type (Petrol, Diesel, CNG): ").strip().lower()
            if fuel_type in ['petrol', 'diesel', 'cng']:
                break
            else:
                print("Invalid fuel type. Please enter 'Petrol', 'Diesel', or 'CNG'.")
        
        while True:
            try:
                fuel_efficiency = float(input(f"How many kilometers does your {fuel_type.capitalize()} vehicle travel per liter? "))
                if fuel_efficiency <= 0:
                    print("Efficiency must be a positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for efficiency.")
        
        while True:
            try:
                fuel_price = float(input(f"Enter the current price of {fuel_type.capitalize()} (per liter or per kg for CNG): "))
                if fuel_price < 0:
                    print("Price cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for fuel price.")
        
        # Calculate fuel consumption and cost
        fuel_needed, fuel_cost = fuel_vehicle_cost(distance, fuel_efficiency, fuel_price)

        # Enhanced output
        print("\n==========================================")
        print(f"           {fuel_type.capitalize()} Vehicle Summary")
        print("==========================================")
        print(f"Distance Traveled:              {distance:.2f} km")
        print(f"Fuel Consumed:                  {fuel_needed:.2f} liters (or kg for CNG)")
        print(f"Total Fuel Cost:                {fuel_cost:.2f} currency units")
        print("==========================================")
    
    elif vehicle_type == 'hybrid':
        while True:
            fuel_type = input("Enter the fuel type (Petrol, Diesel, CNG): ").strip().lower()
            if fuel_type in ['petrol', 'diesel', 'cng']:
                break
            else:
                print("Invalid fuel type. Please enter 'Petrol', 'Diesel', or 'CNG'.")
        
        while True:
            try:
                fuel_efficiency = float(input(f"How many kilometers does your {fuel_type.capitalize()} vehicle travel per liter? "))
                if fuel_efficiency <= 0:
                    print("Efficiency must be a positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for efficiency.")
        
        while True:
            try:
                fuel_price = float(input(f"Enter the current price of {fuel_type.capitalize()} (per liter or per kg for CNG): "))
                if fuel_price < 0:
                    print("Price cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for fuel price.")
        
        while True:
            try:
                ev_efficiency = float(input("How many kilometers does your hybrid vehicle travel per kWh (km per kWh)? "))
                if ev_efficiency <= 0:
                    print("Efficiency must be a positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for efficiency.")
        
        while True:
            try:
                electricity_cost = float(input("Enter the electricity cost per kWh (in your currency): "))
                if electricity_cost < 0:
                    print("Cost cannot be negative. Please try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value for electricity cost.")
        
        while True:
            try:
                hybrid_split = float(input("Enter the percentage of distance driven on fuel vs electricity (0-100): "))
                if 0 <= hybrid_split <= 100:
                    break
                else:
                    print("Please enter a valid percentage between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numerical value for percentage.")
        
        # Calculate fuel and electricity consumption and cost for hybrid
        fuel_needed, energy_needed, hybrid_cost = hybrid_vehicle_cost(distance, fuel_efficiency, fuel_price, ev_efficiency, electricity_cost, hybrid_split)
        
        # Enhanced output
        print("\n==========================================")
        print("              Hybrid Vehicle Summary")
        print("==========================================")
        print(f"Total Distance Traveled:         {distance:.2f} km")
        print(f"Distance on Fuel:                {hybrid_split}% -> {distance * (hybrid_split / 100):.2f} km")
        print(f"Fuel Consumed:                   {fuel_needed:.2f} liters (or kg for CNG)")
        print(f"Distance on Electricity:          {100 - hybrid_split}% -> {distance * ((100 - hybrid_split) / 100):.2f} km")
        print(f"Energy Consumed:                 {energy_needed:.2f} kWh")
        print(f"Total Hybrid Cost:               {hybrid_cost:.2f} currency units")
        print("==========================================")
    
    else:
        print("Invalid vehicle type entered. Please enter 'EV', 'Fuel', or 'Hybrid'.")

# Run the calculator
compare_costs()
